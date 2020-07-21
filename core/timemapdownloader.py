import requests


class TimeMapDownloader:
    """
        This class is for finding deleted tweets of a Twitter handle.

        Note:
            Always run memgator server
            Command: memgator --contimeout=10s --agent=msiddiqu@cs.odu.edu server
            Docker Command: docker run -p 1208:1208 ibnesayeed/memgator --contimeout=10s --agent=msiddiqu@cs.odu.edu
            server

        Attributes:
            __thandle (str): Twitter Handle
            __constants (Constants): For constants
            __logger (Logger): For logging supports debug, error, and access logs
            __dmanager (DataManager): Allows Data Management

    """
    def __init__(self, thandle, constants, dmanager, logger):
        """
        This is constructor for TimeMapDownloader class.

        Parameters:
            thandle (str): Twitter Handle
            constants (Constants): For constants
            dmanager (DataManager): Allows Data Management
            logger (Logger): For logging supports debug, error, and access logs

        """
        self.__thandle = thandle
        self.__constants = constants
        self.__dmanager = dmanager
        self.__logger = logger

    def __write_debug_log(self, message):
        """
        This function is to write debug logs.

        Parameters:
            message (str): Debug Message
        """
        if self.__logger.debug_log:
            self.__logger.debug_log.debug(message)

    def fetch_timemap(self, turl):
        """
        This function is to fetch TimeMap

        Returns:
            (bool): True on Success and False on Failure
        """
        command = self.__constants.MEMGATOR_URL + self.__constants.MEMGATOR_FORMAT + self.__constants.FSLASH + turl
        try:
            response = requests.get(command)
            if response.status_code == 200:
                self.__dmanager.write_timemap(turl, response.content.decode('ascii'))
                self.__write_debug_log("fetch_timemap: " + str(response.status_code))
                return True
            else:
                self.__write_debug_log("fetch_timemap: " + str(response.status_code))
                self.__write_debug_log("fetch_timemap: No timemap found: " + turl)
        except Exception as err:
            self.__logger.error_log.debug("Fetch Timemap: Error: " + str(err))
        return False
