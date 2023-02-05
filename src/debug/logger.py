import os
import logging
APP_LOGGER_NAME = 'PipeSwarmSim'

def setup_logger(logger_name=APP_LOGGER_NAME, file_name='%(name)s.log', level='DEBUG'):
    # Gets or creates a logger
    logger = logging.getLogger(logger_name)

    # set log level
    logger.setLevel(level)

    # set log format
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

    # set stream handler
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)

    # add handlers to the logger
    logger.handlers.clear()
    logger.addHandler(sh)

    if file_name:
        # check if file handler already exists
        for handler in logger.handlers:
            if isinstance(handler, logging.FileHandler):
                logger.removeHandler(handler)
        #check if file exists, remove if it does and create new file
        if os.path.exists(file_name):
            os.remove(file_name)
        # create directory if it doesn't exist
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        # set file handler
        fh = logging.FileHandler(file_name)
        fh.setFormatter(formatter)

        # add handlers to the logger
        logger.addHandler(fh)

    return logger

def get_logger(module_name):
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)
