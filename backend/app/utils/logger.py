import logging


def setup_logger(name: str = "phishguard") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


logger = setup_logger()
