import logging

def setup_logging(verbosity=0):
    """
    Sets up the basic logging configuration.

    Args:
        verbosity (int): Configures the log level which defaults to WARNING.
            A `verbosity` of `0` maps to WARNING, `1` -> INFO, and `2` (or more)
            -> DEBUG. Defaults to `0`.
    """
    log_level = logging.WARNING
    if verbosity == 1:
        log_level = logging.INFO
    elif verbosity >= 2:
        log_level = logging.DEBUG

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )