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
        formatter = logging.Formatter('[%(levelname)s][%(asctime)s][%(module)s.%(funcName)s][line:%(lineno)d] : %('
                                      'message)s')
        handler.setFormatter(formatter)
        # This way nothing is logged twice
        logger.handlers = [handler]
        return logger
