import time
import ast
import requests
import sys
import concurrent.futures
from fch.core.utils.util_functions import Utils
from fch.follower.followerparser import FollowerParser


class MementoDownloader:
    def __init__(self, thandle, turl, constants, dmanager, conf_reader):
        self.__thandle = thandle
        self.__turl = turl
        self.__dmanager = dmanager
        self.__constants = constants
        self.__conf_reader = conf_reader
        self.__parse_memento = FollowerParser(thandle, constants, dmanager, conf_reader)

    '''
    Function gets URIMs and fetches mementos using concurrent threads and writes to database
    '''

    def get_memento(self):
        todo_frontier = self.__parse_timemap()
        if self.__conf_reader.debug: sys.stdout.write("fetch_mementos:  Frontier: " + str(todo_frontier) + "\n")
        if todo_frontier:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                for frontier_list in todo_frontier:
                    future_result = {executor.submit(self.__download_memento, url):
                                         url for url in frontier_list["urims"]}
                    for future in concurrent.futures.as_completed(future_result):
                        if self.__conf_reader.debug: sys.stdout.write("fetch_mementos: result: " + str(future.result()) + "\n")

    '''
    Parses the CDXJ format of memento list and downloads only the mementos above the timestamp of the 3200 recent tweets
    fetched from live Twitter
    '''

    def __parse_timemap(self):

        todo_frontier = []

        '''
        List to count mementos
        Index 0: Total Urls
        Index 1: Already downloaded mementos
        Index 2: To be downloaded mementos
        '''
        mcount = [0, 0, 0]
        mintime, maxtime = Utils.get_timerange(self.__constants, self.__conf_reader)
        if self.__conf_reader.debug: sys.stdout.write("__parse_timemap:  Minimum Live Timestamp: {} Maximum Live Timestamp: {}".format
                               (mintime, maxtime) + "\n")
        timemap_content = Utils.parse_timemap(self.__dmanager, self.__constants, self.__turl, self.__conf_reader, mintime, maxtime)
        if self.__conf_reader.debug: sys.stdout.write("__parse_timemap: " + str(timemap_content) + "\n")
        for memento in timemap_content:
            response = Utils.get_murl_info(memento, self.__thandle)
            # If archive.is mementos then skip it, as we do not parse them
            # Added to remove wayback.archive.it
            if response["archive"] not in ["archive.is", "archive.md"]:
                if response["timestamp"].isdigit():
                    if mintime <= int(response["timestamp"]) <= maxtime:
                        # Count total number of mementos for twitter handle within the time range
                        mcount[0] += 1
                        memento_present = self.__dmanager.lookup_memento(memento)
                        if memento_present:
                            mcount[1] += 1
                        else:
                            mcount[2] += 1
                            frontier_present = False
                            for entry in todo_frontier:
                                if entry["archive"] == response["archive"]:
                                    frontier_present = True
                                    entry["urims"].append(memento["uri"])
                                    entry["count"] += 1
                                    break
                            if not frontier_present:
                                json_object = {"archive": response["archive"], "count": 1,
                                               "urims": [memento["uri"]]}
                                todo_frontier.append(json_object)
        # Write logs for each user
        if self.__conf_reader.debug: sys.stdout.write("fetch_mementos: Twitter Handle: " + self.__thandle + "\n")
        if self.__conf_reader.debug: sys.stdout.write("fetch_mementos: Date-Time: " + str(time.strftime("%b %d %Y %H:%M:%S", time.gmtime())) + "\n")
        if self.__conf_reader.debug: sys.stdout.write("fetch_mementos: Total Memento URLs: " + str(mcount[0]) + "\n")
        if self.__conf_reader.debug: sys.stdout.write("fetch_mementos: Number of Mementos already downloaded: " + str(mcount[1]) + "\n")
        if self.__conf_reader.debug: sys.stdout.write("fetch_mementos: Number of Mementos for consideration: " + str(mcount[2]) + "\n")
        return todo_frontier

    '''
    Function to fetch Mementos, send response for parsing and write the response
    '''

    def __download_memento(self, murl):
        if self.__conf_reader.debug: sys.stdout.write("__download_memento:" + murl + "\n")
        try:
            self.__dmanager.write_memento(murl)
        except requests.exceptions.ConnectionError as err:
            sys.stderr.write("__download_memento: ConnectionError: " + murl + " " + str(err) + "\n")
        except Exception as err:
            sys.stderr.write("__download_memento: " + murl + " " + str(err) + "\n")
