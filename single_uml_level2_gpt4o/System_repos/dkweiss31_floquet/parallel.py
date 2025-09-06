import multiprocessing

def parallel_map(num_cpus, func, parameters):
    """
    Apply a function to each item in an iterable in parallel using multiple CPU cores for improved performance.
    """
    with multiprocessing.Pool(num_cpus) as pool:
        result = pool.map(func, parameters)
    return result