```python
import numpy as np

class ChiacToAmp:
    def __init__(self, H0, H1, state_indices, omega_d_values):
        self.H0 = H0
        self.H1 = H1
        self.state_indices = state_indices
        self.omega_d_linspace = omega_d_values

    def amplitudes_for_omega_d(self, chi_ac_linspace):
        return 2 * np.sqrt(chi_ac_linspace / self.H0)

    def chi_ell(self, energies, H1, E_osc, ell):
        chi_ell_ellp_sum = sum(self.chi_ell_ellp(energies, H1, E_osc, ell, ellp) for ellp in range(len(energies)))
        chi_ellp_ell_sum = sum(self.chi_ell_ellp(energies, H1, E_osc, ellp, ell) for ellp in range(len(energies)))
        return chi_ell_ellp_sum - chi_ellp_ell_sum

    def chi_ell_ellp(self, energies, H1, E_osc, ell, ellp):
        return np.abs(H1[ell, ellp]) ** 2 / (energies[ell] - energies[ellp] + E_osc)

    def compute_chis_for_omega_d(self):
        return self.chi_ell(self.H0, self.H1, self.omega_d_linspace, self.state_indices[0]) - \
               self.chi_ell(self.H0, self.H1, self.omega_d_linspace, self.state_indices[1])


class XiSqToAmp:
    def __init__(self, H0, H1, state_indices, omega_d_linspace):
        self.H0 = H0
        self.H1 = H1
        self.state_indices = state_indices
        self.omega_d_linspace = omega_d_linspace

    def amplitudes_for_omega_d(self, xi_sq_linspace):
        return 2 * np.sqrt(xi_sq_linspace / self.H0)
```