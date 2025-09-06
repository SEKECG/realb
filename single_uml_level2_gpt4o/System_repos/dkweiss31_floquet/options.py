# options.py

class Options:
    def __init__(self, fit_range_fraction=1.0, floquet_sampling_time_fraction=0.0, fit_cutoff=4, overlap_cutoff=0.8, nsteps=30000, num_cpus=1, save_floquet_modes=False):
        self.fit_range_fraction = fit_range_fraction
        self.floquet_sampling_time_fraction = floquet_sampling_time_fraction
        self.fit_cutoff = fit_cutoff
        self.overlap_cutoff = overlap_cutoff
        self.nsteps = nsteps
        self.num_cpus = num_cpus
        self.save_floquet_modes = save_floquet_modes