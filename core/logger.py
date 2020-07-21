import logging
import os
from core.datamanager import DataManager


class Logger:
    """
    This is a class for Logging.

    Attributes:
        __config (ConfigurationReader): For Configuration
        error_log (Logger): For Error Logging
        debug_log (Logger): For Debug Logging
        access_log (Logger): For Common Logging
    """
    def __init__(self, config):
        self.error_log = None
        self.debug_log = None
        self.access_log = None
        self.__config = config

    '''
    Function to set up logging handle and return it
    '''
    @classmethod
    def __set_up_logger(cls, name, log_file, level=logging.DEBUG):
        """
        This is a function to set up logging objects.

        Parameters:
            name (str): Log Level
            log_file (str): File Name
            level (Logging): Logging level

        Returns:
             logger (Logging): Logging object
        """
        handler = logging.FileHandler(log_file, mode="w")
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        return logger

    '''
    Function to create logging objects
    '''

    def create_logging_instances(self, log_type):
        """
        This function is for creating different logging instances.

        Parameters:
            log_type (str): Category of Logs
        """
        flog = log_type + "Common.log"
        self.access_log = self.__set_up_logger('ACCESS_LOGS', os.path.join(self.__config.log_dir, flog))
        flog = log_type + "Error.log"
        self.error_log = self.__set_up_logger('ERROR_LOGS', os.path.join(self.__config.log_dir, flog))
        if self.__config.debug:
            flog = log_type + "Debug.log"
            self.debug_log = self.__set_up_logger('DEBUG_LOGS', os.path.join(self.__config.log_dir, flog))
