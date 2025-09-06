import torch
import torch.distributed as dist
from torch.optim.optimizer import Optimizer
from typing import Any


def zeropower_via_newtonschulz5(G, steps) -> torch.Tensor:
    """
    Newton-Schulz iteration to compute the zeroth power / orthogonalization of G. We opt to use a
    quintic iteration whose coefficients are selected to maximize the slope at zero. For the purpose
    of minimizing steps, it turns out to be empirically effective to keep increasing the slope at
    zero even beyond the point where the iteration no longer converges all the way to one everywhere
    on the interval. This iteration therefore does not produce UV^T but rather something like US'V^T
    where S' is diagonal with S_{ii}' ~ Uniform(0.5, 1.5), which turns out not to hurt model
    performance at all relative to UV^T, where USV^T = G is the SVD.
    """
    X = G
    for _ in range(steps):
        XTX = X.transpose(-2, -1) @ X
        X = X @ (1.875 * torch.eye(X.size(-1), device=X.device, dtype=X.dtype) - 
                 1.25 * XTX + 
                 0.375 * XTX @ XTX)
    return X


class Muon(Optimizer):
    """
    Muon - MomentUm Orthogonalized by Newton-schulz

    https://kellerjordan.github.io/posts/muon/

    Muon internally runs standard SGD-momentum, and then performs an orthogonalization post-
    processing step, in which each 2D parameter's update is replaced with the nearest orthogonal
    matrix. To efficiently orthogonalize each update, we use a Newton-Schulz iteration, which has
    the advantage that it can be stably run in bfloat16 on the GPU.

    Some warnings:
    - This optimizer should not be used for the embedding layer, the final fully connected layer,
    or any {0,1}-D parameters; those should all be optimized by a standard method (e.g., AdamW).
    - To use it with 4D convolutional filters, it works well to just flatten their last 3 dimensions.

    Arguments:
        lr: The learning rate used by the internal SGD.
        momentum: The momentum used by the internal SGD.
        nesterov: Whether to use Nesterov-style momentum in the internal SGD. (recommended)
        ns_steps: The number of Newton-Schulz iteration steps to use.
    """

    def __init__(self, params, lr, weight_decay=0, momentum=0, nesterov=False, ns_steps=5, rank=0, world_size=1):
        if lr < 0.0:
            raise ValueError(f"Invalid learning rate: {lr}")
        if weight_decay < 0.0:
            raise ValueError(f"Invalid weight_decay value: {weight_decay}")
        if momentum < 0.0:
            raise ValueError(f"Invalid momentum value: {momentum}")
        if ns_steps < 1:
            raise ValueError(f"Invalid ns_steps value: {ns_steps}")

        defaults = dict(lr=lr, weight_decay=weight_decay, momentum=momentum, 
                       nesterov=nesterov, ns_steps=ns_steps)
        super().__init__(params, defaults)
        
        self.rank = rank
        self.world_size = world_size

    def step(self) -> None:
        """
        Perform a distributed optimization step with momentum, weight decay, and Nesterov acceleration, 
        utilizing asynchronous all-gather operations for efficient parameter updates across multiple processes.
        """
        for group in self.param_groups:
            weight_decay = group['weight_decay']
            momentum = group['momentum']
            nesterov = group['nesterov']
            lr = group['lr']
            ns_steps = group['ns_steps']

            for p in group['params']:
                if p.grad is None:
                    continue

                grad = p.grad.data
                state = self.state[p]

                # Initialize state if needed
                if 'momentum_buffer' not in state:
                    state['momentum_buffer'] = torch.zeros_like(p.data)

                buf = state['momentum_buffer']

                # Apply weight decay
                if weight_decay != 0:
                    grad = grad.add(p.data, alpha=weight_decay)

                # Update momentum buffer
                if momentum != 0:
                    buf.mul_(momentum).add_(grad)
                    if nesterov:
                        grad = grad.add(buf, alpha=momentum)
                    else:
                        grad = buf
                else:
                    buf = grad

                # For 2D parameters, apply orthogonalization
                if p.data.dim() == 2:
                    # All-gather gradients across processes if distributed
                    if self.world_size > 1:
                        grad_list = [torch.empty_like(grad) for _ in range(self.world_size)]
                        dist.all_gather(grad_list, grad)
                        grad = torch.cat(grad_list, dim=0)

                    # Apply Newton-Schulz orthogonalization
                    orthogonal_grad = zeropower_via_newtonschulz5(grad, ns_steps)
                    
                    # Scatter back if distributed
                    if self.world_size > 1:
                        chunk_size = orthogonal_grad.size(0) // self.world_size
                        orthogonal_grad = orthogonal_grad[self.rank * chunk_size:(self.rank + 1) * chunk_size]
                    
                    # Update parameter
                    p.data.add_(orthogonal_grad, alpha=-lr)
                else:
                    # Standard SGD update for non-2D parameters
                    p.data.add_(grad, alpha=-lr)