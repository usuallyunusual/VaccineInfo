import logging
import sys


class Logging:
    """
    Project wide logger setup
    """

    def get_logger(self):
        """
        Returns a project wide instance of the same logger
        """
        logger = logging.getLogger("Vaccine")
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
