from core.timemapdownloader import TimeMapDownloader
from core.mementodownloader import MementoDownloader
from follower.followeranalysis import FollowerAnalysis
from follower.followerparser import FollowerParser

import os
import subprocess

class FollowerCount:
    def __init__(self, thandle, conf_reader, constants, dmanager):
        self.__thandle = thandle
        self.__conf_reader = conf_reader
        self.__constants = constants
        self.__dmanager = dmanager

    def get_follower_count(self):
        self.__cleanup_files()
        turl  = self.__constants.TWITTER_URL + self.__thandle
        print("Start: (main)" + turl)
        self.__dmanager.set_twitter_handle(self.__thandle)
        tm_object = TimeMapDownloader(self.__thandle, self.__constants, self.__dmanager)
        tm_status = tm_object.fetch_timemap(turl)
        print("Start: (main): Fetching timemap done: " + turl)
        if tm_status:
            mobject = MementoDownloader(self.__thandle, turl, self.__constants, self.__dmanager)
            mobject.get_memento(self.__conf_reader)
            print("Start: (main): Fetching mementos")
            fparser = FollowerParser(self.__thandle, self.__constants, self.__dmanager)
            fparser.parse_mementos(self.__conf_reader, turl)
            print("Start: (main): Parsing mementos")


    def get_follower_analysis(self):
        fanalysis = FollowerAnalysis(self.__thandle, self.__conf_reader, self.__constants, self.__dmanager)
        fanalysis.relative_analysis()

    def plot_graph(self):
        Rcall = "Rscript --vanilla ../followerCount.R " + self.__thandle + "_analysis"
        subprocess.call("docker container run -it --rm -u $(id -u):$(id -g) -v $PWD:$PWD -w $PWD r-base bash", shell=True)
        subprocess.call(Rcall, shell=True)

    def __cleanup_files(self):
        if os.path.exists(os.path.join(os.getcwd(), "follower", "data", "NonParsedMementos.txt")):
            os.remove(os.path.join(os.getcwd(), "follower", "data", "NonParsedMementos.txt"))
        if os.path.exists(os.path.join(os.getcwd(), "follower", "data", "mementos.txt")):
            os.remove(os.path.join(os.getcwd(), "follower", "data", "mementos.txt"))