import time
import ast
import requests
import concurrent.futures
from core.utils.util_functions import Utils
from follower.followerparser import FollowerParser


class MementoDownloader:
    def __init__(self, thandle, turl, constants, dmanager):
        self.__thandle = thandle
        self.__turl = turl
        self.__dmanager = dmanager
        self.__constants = constants
        self.__parse_memento = FollowerParser(thandle, constants, dmanager)

    '''
    Function gets URIMs and fetches mementos using concurrent threads and writes to database
    '''

    def get_memento(self, config):
        todo_frontier = self.__parse_timemap(config)
        print("fetch_mementos:  Frontier: " + str(todo_frontier))
        if todo_frontier:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(todo_frontier)) as executor:
                for frontier_list in todo_frontier:
                    future_result = {executor.submit(self.__download_memento, url):
                                         url for url in frontier_list["urims"]}
                    for future in concurrent.futures.as_completed(future_result):
                        print("fetch_mementos: result: " + str(future.result()))
                        
    '''
    Parses the CDXJ format of memento list and downloads only the mementos above the timestamp of the 3200 recent tweets
    fetched from live Twitter
    '''

    def __parse_timemap(self, config):

        todo_frontier = []

        '''
        List to count mementos
        Index 0: Total Urls
        Index 1: Already downloaded mementos
        Index 2: To be downloaded mementos
        '''
        mcount = [0, 0, 0]
        mintime, maxtime = Utils.get_timerange(self.__constants, config)
        print("fetch_mementos:  Minimum Live Timestamp: {} Maximum Live Timestamp: {}".format
                               (mintime, maxtime))
        timemap_content = Utils.parse_timemap(self.__dmanager, self.__constants, self.__turl, config, mintime, maxtime)
        print("fetch_mementos: " + str(timemap_content))
        for memento in timemap_content:
            response = Utils.get_murl_info(memento["uri"], self.__thandle)
            # If archive.is mementos then skip it, as we do not parse them
            # Added to remove wayback.archive.it
            if response["archive"] not in ["archive.is", "archive.md"]:
                if response["timestamp"].isdigit():
                    if mintime <= int(response["timestamp"]) <= maxtime:
                        # Count total number of mementos for twitter handle within the time range
                        mcount[0] += 1 
                        memento_present = self.__dmanager.lookup_memento(memento["uri"])
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
        print("fetch_mementos: Twitter Handle: " + self.__thandle)
        print("fetch_mementos: Date-Time: " + str(time.strftime("%b %d %Y %H:%M:%S", time.gmtime())))
        print("fetch_mementos: Total Memento URLs: " + str(mcount[0]))
        print("fetch_mementos: Number of Mementos already downloaded: " + str(mcount[1]))
        print("fetch_mementos: Number of Mementos for consideration: " + str(mcount[2]))
        return todo_frontier

    '''
    Function to fetch Mementos, send response for parsing and write the response
    '''

    def __download_memento(self, murl):
        self.__write_debug_log("__download_memento:" + murl)
        try:
            self.__dmanager.write_memento(murl)
        except requests.exceptions.ConnectionError as err:
            print("make_network_request: ConnectionError: " + murl + " " + str(err))
        except Exception as err:
            print("make_network_request: " + murl + " " + str(err))
