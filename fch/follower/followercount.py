from fch.core.timemapdownloader import TimeMapDownloader
from fch.core.mementodownloader import MementoDownloader
from fch.follower.followeranalysis import FollowerAnalysis
from fch.follower.followerparser import FollowerParser

import os
import sys
import subprocess

class FollowerCount:
    '''
        This class is for finding historical Twitter follower count.

        Attributes:
            __thandle (string): Twitter Handle
            __conf_reader (JSON): Configuration object
            __constants (Constants): Constants object
            __dmanager (DataManager): DataManager object
    '''
    def __init__(self, thandle, conf_reader, constants, dmanager):
        """
            The constructor of FollowerCount class.

            Parameters:
                thandle (string): Twitter Handle
                conf_reader (ConfigurationReader): Configuration object
                constants (Constants): For constants
                datamanager (DataManager): Data manager object
        """
        self.__thandle = thandle
        self.__conf_reader = conf_reader
        self.__constants = constants
        self.__dmanager = dmanager

    def get_follower_count(self):
        """
            Function to calculate historical Twitter follower count

            Parameters:

            Returns:
        """
        self.__cleanup_files()
        turl  = self.__constants.TWITTER_URL + self.__thandle
        if self.__conf_reader.debug: sys.stdout.write("Start: (main)" + turl + "\n")
        self.__dmanager.set_twitter_handle(self.__thandle)
        tm_object = TimeMapDownloader(self.__thandle, self.__constants, self.__dmanager, self.__conf_reader)
        tm_status = tm_object.fetch_timemap(turl)
        if self.__conf_reader.debug: sys.stdout.write("Start: (main): Fetching timemap done: " + turl + "\n")
        if tm_status:
            mobject = MementoDownloader(self.__thandle, turl, self.__constants, self.__dmanager, self.__conf_reader)
            mobject.get_memento()
            if self.__conf_reader.debug: sys.stdout.write("Start: (main): Fetching mementos" + "\n")
            fparser = FollowerParser(self.__thandle, self.__constants, self.__dmanager, self.__conf_reader)
            lfollower = fparser.parse_mementos(turl)
            if self.__conf_reader.debug: sys.stdout.write("Start: (main): Parsing mementos" + "\n")
            fanalysis = FollowerAnalysis(self.__thandle, self.__conf_reader, self.__constants, self.__dmanager)
            fanalysis.relative_analysis(lfollower)
            if self.__conf_reader.debug: sys.stdout.write("Start: (main): Follower Analysis" + "\n")

    def __cleanup_files(self):
        if os.path.exists(os.path.join(os.getcwd(), "NonParsedMementos.txt")):
            os.remove(os.path.join(os.getcwd(), "NonParsedMementos.txt"))
        if os.path.exists(os.path.join(os.getcwd(), "mementos.txt")):
            os.remove(os.path.join(os.getcwd(), "mementos.txt"))
