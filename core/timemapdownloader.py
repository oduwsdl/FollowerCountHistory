import requests
import sys
import subprocess

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
            __dmanager (DataManager): Allows Data Management
            __conf_reader (ConfigReader): ConfigReader object

    """
    def __init__(self, thandle, constants, dmanager, config_reader):
        """
        This is constructor for TimeMapDownloader class.

        Parameters:
            thandle (str): Twitter Handle
            constants (Constants): For constants
            dmanager (DataManager): Allows Data Management
            config_reader (ConfigReader): ConfigReader object

        """
        self.__thandle = thandle
        self.__constants = constants
        self.__dmanager = dmanager
        self.__conf_reader = config_reader

    def fetch_timemap(self, turl):
        """
        This function is to fetch TimeMap

        Returns:
            (bool): True on Success and False on Failure
        """
        # command = self.__constants.MEMGATOR_URL + self.__constants.MEMGATOR_FORMAT + self.__constants.FSLASH + turl
        command = "https://memgator.cs.odu.edu/timemap/cdxj/" + turl
        try:
            response = requests.get(command)
            # result = subprocess.run("docker container run -it --rm oduwsdl/memgator --format=cdxj --contact=msidd003@odu.edu --contimeout=10s https://twitter.com/m_nsiddique", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            if response.status_code == 200:
                self.__dmanager.write_timemap(turl, response.content.decode('ascii'))
                if self.__conf_reader.debug: sys.stdout.write("fetch_timemap: " + str(response.status_code) + "\n")
                return True
            else:
                if self.__conf_reader.debug: sys.stdout.write("fetch_timemap: " + str(response.status_code) + "\n")
                if self.__conf_reader.debug: sys.stdout.write("fetch_timemap: No timemap found: " + turl + "\n")
        except Exception as err:
            sys.stderr.write("Fetch Timemap: Error: "+ turl + "   " + str(err) + "\n")
        return False
