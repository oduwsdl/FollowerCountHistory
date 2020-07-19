import time
import ast
import requests
import concurrent.futures
import threading
import inspect
from core.utils.util_functions import Utils
from deletedtweets.mementoparser import MementoParser
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
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        self.__module = mod.__name__
        if self.__module == "deletedtweets.deletedtweetfinder":
            self.__parse_memento = MementoParser(thandle, constants, dmanager, crud_atweet, crud_memento, logger)
        elif self.__module == "follower.followercount":
            self.__parse_memento = FollowerParser(thandle, constants, dmanager, logger)
        else:
            self.__parse_memento = None
            print(self.__module)
            exit()

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
        todo_frontier, done_frontier = self.__parse_timemap(config, ltweets_db)
        self.__write_debug_log("fetch_mementos:  Frontier: " + str(todo_frontier))
        print("get_memento: Frontier List created")
        if todo_frontier:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(todo_frontier)) as executor:
                for frontier_list in todo_frontier:
                    future_result = {executor.submit(self.__download_memento, url, qtweet,
                                                     qmemento):
                                         url for url in frontier_list["urims"]}
                    for future in concurrent.futures.as_completed(future_result):
                        self.__write_debug_log("fetch_mementos: result: " + str(future.result()))

        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            future_result = {executor.submit(self.__reparse_tweets, url, qtweet,
                                                                qmemento): url for url in
                                    done_frontier}
            for future in concurrent.futures.as_completed(future_result):
                self.__write_debug_log("fetch_mementos: result completed: " + str(future.result()))
        if self.__module == "deletedtweets.deletedtweetfinder":
            qtweet.join()
            qmemento.join()
            qtweet.put(None)
            qmemento.put(None)
        # self.__test_database_entry(db_archive, db_memento)
            self.__write_debug_log("Running threads: " + str(threading.active_count()))
            self.__write_debug_log(threading.enumerate())

    '''
    Parses the CDXJ format of memento list and downloads only the mementos above the timestamp of the 3200 recent tweets
    fetched from live Twitter
    '''

    def __parse_timemap(self, config, ltweets_db):

        todo_frontier = []
        done_frontier = []
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
                if response["archive"] not in ["archive.is", "archive.md", "wayback.archive-it.org"]:
                    if response["timestamp"].isdigit():
                        if mintime <= int(response["timestamp"]) <= maxtime:
                            # Count total number of mementos for twitter handle within the time range
                            mcount[0] += 1
                            memento = ast.literal_eval(line_split[1]) 
                            memento_present = self.__dmanager.lookup_memento(memento["uri"])
                            if memento_present:
                                mcount[1] += 1
                                done_frontier.append(memento["uri"])
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
        return todo_frontier, done_frontier

    '''
    Testing database entry function
    '''

    def __test_database_entry(self, collection_archive, collection_memento):
        if self.__logger.debug_log is not None:
            file_log = open(self.__constants.DIRECTORY_LOGS + "ArchiveDatabaseLogs.txt", "a+")
            query = collection_archive.find()
            count = 0
            for row in query:
                file_log.write(str(row) + "\n")
                count += 1
            query = collection_memento.find()
            count_q = 0
            for row in query:
                file_log.write(str(row) + "\n")
                count_q += 1
            file_log.write("Archive Database Count: " + str(count) + "\n")
            file_log.write("Memento Database Count: " + str(count_q) + "\n")

    '''
    Function to fetch Mementos, send response for parsing and write the response
    '''

    def __download_memento(self, murl, qtweet=None, qmemento=None):
        self.__write_debug_log("__download_memento:" + murl)
        try:
            if self.__dmanager.write_memento(murl):
                mcontent = self.__dmanager.read_memento(murl)
                if mcontent:
                    if self.__module == "deletedtweets.deletedtweetfinder":
                        self.__parse_memento.parse_memento(mcontent, qtweet, qmemento, murl)
                    elif self.__module == "follower.followercount":
                        self.__parse_memento.parse_memento(mcontent, murl)
        except requests.exceptions.ConnectionError as err:
            self.__logger.error_log.debug("make_network_request: ConnectionError: " + murl + " " + str(err))
        except Exception as err:
            self.__logger.error_log.debug("make_network_request: " + murl + " " + str(err))

    '''
    Function to set up parsing for already present mementos
    '''

    def __reparse_tweets(self, murl, qtweet, qmemento):
        self.__write_debug_log("__reparse_tweets: " + murl)
        if self.__module == "follower.followercount":
            self.__write_debug_log("Follower Count Reparse Tweets: " + murl)
            self.__parse_memento.parse_memento(self.__dmanager.read_memento(murl), murl)
        elif not self.__dmanager.lookup_parsed_memento(murl):
            self.__write_debug_log("__send_for_parsing: " + murl)
            if self.__parse_memento:
                if self.__module == "deletedtweets.deletedtweetfinder":
                    self.__parse_memento.parse_memento(self.__dmanager.read_memento(murl), qtweet, qmemento, murl)
