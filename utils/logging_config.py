import logging
import os


def config_logging():
    if "RENDER" in os.environ:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG)
