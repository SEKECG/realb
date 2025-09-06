import numpy as np
import qutip as qt
import itertools

class Model:
    def __init__(self, H0, H1, omega_d_values, drive_amplitudes):
        self.H0 = H0
        self.H1 = H1
        self.omega_d_values = np.array(omega_d_values)
        self.drive_amplitudes = np.array(drive_amplitudes)
        if self.drive_amplitudes.ndim == 1:
            self.drive_amplitudes = np.tile(self.drive_amplitudes, (len(self.omega_d_values), 1))

    def amp_to_idx(self, amp, omega_d):
        omega_d_idx = self.omega_d_to_idx(omega_d)
        return np.argmin(np.abs(self.drive_amplitudes[omega_d_idx] - amp))

    def hamiltonian(self, omega_d_amp):
        omega_d, amp = omega_d_amp
        return [self.H0, [self.H1, f'{amp}*cos({omega_d}*t)']]

    def omega_d_amp_params(self, amp_idxs):
        return itertools.chain.from_iterable(
            [(omega_d, self.drive_amplitudes[omega_d_idx][amp_idx]) for amp_idx in amp_idxs]
            for omega_d_idx, omega_d in enumerate(self.omega_d_values)
        )

    def omega_d_to_idx(self, omega_d):
        return np.argmin(np.abs(self.omega_d_values - omega_d))