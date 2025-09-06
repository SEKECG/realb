import numpy as np
import qutip as qt
from scipy.optimize import curve_fit

class DisplacedState:
    def __init__(self, hilbert_dim, model, state_indices, options):
        self.hilbert_dim = hilbert_dim
        self.model = model
        self.state_indices = state_indices
        self.options = options
        self.exponent_pair_idx_map = self._create_exponent_pair_idx_map()

    def _coefficient_for_state(self, xydata, state_idx_coefficients, bare_same):
        return np.polyval(state_idx_coefficients, xydata)

    def _create_exponent_pair_idx_map(self):
        exponent_pair_idx_map = {}
        order = self.options.fit_cutoff
        idx = 0
        for i in range(order + 1):
            for j in range(order + 1):
                if i + j > 0:
                    exponent_pair_idx_map[(i, j)] = idx
                    idx += 1
        return exponent_pair_idx_map

    def _fit_coefficients_factory(self, XYdata, Zdata, p0, bare_same):
        try:
            popt, _ = curve_fit(self._coefficient_for_state, XYdata, Zdata, p0=p0)
        except RuntimeError:
            popt = np.zeros_like(p0)
        return popt

    def _fit_coefficients_for_component(self, omega_d_amp_filtered, floquet_component_filtered, bare_same):
        XYdata = np.array(omega_d_amp_filtered)
        Zdata = np.array(floquet_component_filtered)
        p0 = np.zeros(len(self.exponent_pair_idx_map))
        return self._fit_coefficients_factory(XYdata, Zdata, p0, bare_same)

    def bare_state_coefficients(self, state_idx):
        coefficients = np.zeros(len(self.exponent_pair_idx_map))
        coefficients[0] = 1.0
        return coefficients

    def displaced_state(self, omega_d, amp, state_idx, coefficients):
        state = qt.Qobj(np.zeros(self.hilbert_dim))
        for (i, j), idx in self.exponent_pair_idx_map.items():
            state += coefficients[idx] * (omega_d ** i) * (amp ** j)
        return state

    def displaced_states_fit(self, omega_d_amp_slice, ovlp_with_bare_states, floquet_modes):
        coefficients = []
        for state_idx in self.state_indices:
            mask = ovlp_with_bare_states[:, :, state_idx] >= self.options.overlap_cutoff
            omega_d_amp_filtered = omega_d_amp_slice[mask]
            floquet_component_filtered = floquet_modes[mask, :, state_idx]
            coeffs = self._fit_coefficients_for_component(omega_d_amp_filtered, floquet_component_filtered, False)
            coefficients.append(coeffs)
        return np.array(coefficients)

    def overlap_with_bare_states(self, amp_idx_0, coefficients, floquet_modes):
        overlaps = np.zeros((len(self.model.omega_d_values), len(self.model.drive_amplitudes), len(self.state_indices)))
        for i, omega_d in enumerate(self.model.omega_d_values):
            for j, amp in enumerate(self.model.drive_amplitudes):
                for k, state_idx in enumerate(self.state_indices):
                    bare_state = self.displaced_state(omega_d, amp, state_idx, coefficients[k])
                    overlaps[i, j, k] = np.abs((bare_state.dag() * floquet_modes[i, j, :, state_idx]).full()[0, 0])
        return overlaps

    def overlap_with_displaced_states(self, amp_idxs, coefficients, floquet_modes):
        overlaps = np.zeros((len(self.model.omega_d_values), len(amp_idxs), len(self.state_indices)))
        for i, omega_d in enumerate(self.model.omega_d_values):
            for j, amp_idx in enumerate(amp_idxs):
                amp = self.model.drive_amplitudes[amp_idx]
                for k, state_idx in enumerate(self.state_indices):
                    displaced_state = self.displaced_state(omega_d, amp, state_idx, coefficients[k])
                    overlaps[i, j, k] = np.abs((displaced_state.dag() * floquet_modes[i, amp_idx, :, state_idx]).full()[0, 0])
        return overlaps