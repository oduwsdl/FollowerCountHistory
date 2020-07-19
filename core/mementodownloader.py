import time
import ast
import requests
import concurrent.futures
from core.utils.util_functions import Utils
from follower.mementoparser import FollowerParser


class MementoDownloader:
    def __init__(self, thandle, turl, constants, dmanager, logger, crud_memento=None, crud_atweet=None):
        self.__thandle = thandle
        self.__turl = turl
        self.__dmanager = dmanager
        self.__logger = logger
        self.__constants = constants
        self.__crud_memento = crud_memento
        self.__crud_atweet = crud_atweet
        self.__parse_memento = FollowerParser(thandle, constants, dmanager, logger)

    '''
    Function to write debug logs
    '''
    def __write_debug_log(self, message):
        if self.__logger.debug_log:
            self.__logger.debug_log.debug(message)

    '''
    Function gets URIMs and fetches mementos using concurrent threads and writes to database
    '''

    def get_memento(self, config, ltweets_db=None, qtweet=None, qmemento=None):
        todo_frontier = self.__parse_timemap(config, ltweets_db)
        self.__write_debug_log("fetch_mementos:  Frontier: " + str(todo_frontier))
        if todo_frontier:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(todo_frontier)) as executor:
                for frontier_list in todo_frontier:
                    future_result = {executor.submit(self.__download_memento, url, qtweet,
                                                     qmemento):
                                         url for url in frontier_list["urims"]}
                    for future in concurrent.futures.as_completed(future_result):
                        self.__write_debug_log("fetch_mementos: result: " + str(future.result()))

    '''
    Parses the CDXJ format of memento list and downloads only the mementos above the timestamp of the 3200 recent tweets
    fetched from live Twitter
    '''

    def __parse_timemap(self, config, ltweets_db):

        todo_frontier = []

        '''
        List to count mementos
        Index 0: Total Urls
        Index 1: Already downloaded mementos
        Index 2: To be downloaded mementos
        '''
        mcount = [0, 0, 0]
        mintime, maxtime = Utils.get_timerange(self.__constants, config, ltweets_db)
        self.__write_debug_log("fetch_mementos:  Minimum Live Timestamp: {} Maximum Live Timestamp: {}".format
                               (mintime, maxtime))
        timemap_content = self.__dmanager.read_timemap(self.__turl)
        for line in timemap_content:
            if self.__constants.ERROR404 in line:
                self.__write_debug_log("fetch_mementos: " + self.__constants.ERROR404)
                return False
            elif not line.startswith("@") and line.rstrip():
                line_split = line.split(" ", 1)
                response = Utils.get_murl_info(line_split[1], self.__thandle)
                # If archive.is mementos then skip it, as we do not parse them
                # Added to remove wayback.archive.it
                if response["archive"] not in ["archive.is", "archive.md"]:
                    if response["timestamp"].isdigit():
                        if mintime <= int(response["timestamp"]) <= maxtime:
                            # Count total number of mementos for twitter handle within the time range
                            mcount[0] += 1
                            memento = ast.literal_eval(line_split[1]) 
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
        self.__write_debug_log("fetch_mementos: Twitter Handle: " + self.__thandle)
        self.__write_debug_log("fetch_mementos: Date-Time: " + str(time.strftime("%b %d %Y %H:%M:%S", time.gmtime())))
        self.__write_debug_log("fetch_mementos: Total Memento URLs: " + str(mcount[0]))
        self.__write_debug_log("fetch_mementos: Number of Mementos already downloaded: " + str(mcount[1]))
        self.__write_debug_log("fetch_mementos: Number of Mementos for consideration: " + str(mcount[2]))
        return todo_frontier

    '''
    Function to fetch Mementos, send response for parsing and write the response
    '''

    def __download_memento(self, murl, qtweet=None, qmemento=None):
        self.__write_debug_log("__download_memento:" + murl)
        try:
            self.__dmanager.write_memento(murl)
        except requests.exceptions.ConnectionError as err:
            self.__logger.error_log.debug("make_network_request: ConnectionError: " + murl + " " + str(err))
        except Exception as err:
            self.__logger.error_log.debug("make_network_request: " + murl + " " + str(err))
