import os
from warcio.warcwriter import WARCWriter
from warcio.statusandheaders import StatusAndHeaders
from warcio.archiveiterator import ArchiveIterator
import requests
import json
import csv
from core.utils.util_functions import Utils
import time


class DataManager:
    """
        This class is for Data Management.

        Attributes:
            __data_dir (str): Default Output Directory
            __config (ConfigurationReader): Configuration object
            __constants (Constants): For constants
            __memento_dir (str): Memento Directory
            __timemap_dir (str): TimeMap Directory
            __pmemento_dir (str): Parsed Memento Directory
            __dtweet_dir (str): Deleted Tweets Directory
            __json_dir (str): Json files Directory
            __fcount_dir (str): Follower Count Directory

    """
    def __init__(self, config, constants, logger):
        """
            The constructor of DataManager class.

            Parameters:
                config (ConfigurationReader): Configuration object
                constants (Constants): For constants
                logger (Logger): Logger Object
        """
        self.__config = config
        self.__data_dir = config.out_dir
        self.__logger = logger
        self.__constants = constants
        self.__memento_dir = os.path.join(self.__data_dir, "Mementos")
        self.__timemap_dir = os.path.join(self.__data_dir, "TimeMap")
        self.__pmemento_dir = os.path.join(self.__data_dir, "ParsedMementos")
        self.__dtweet_dir = os.path.join(self.__data_dir, "DeletedTweets")
        self.__json_dir = os.path.join(self.__data_dir, "JsonOutputs")
        self.__fcount_dir = os.path.join(self.__data_dir, "FollowerCount")

    def __write_error_logs(self, message):
        """
        This function is to write error logs
        :param message:
        :return:
        """
        self.__logger.error_logger.debug(message)

    def __write_debug_logs(self, message):
        self.__logger.debug_logger.debug(message)

    def write_memento(self, murl=None):
        """
        This is function to write memento in WARC format.

        Parameters:
            murl (str): URI-M

        Returns:
            (bool): True on Success and False on Failure
        """
        if self.lookup_memento(murl):
            return True
        else:
            response = Utils.get_murl_info(murl)
            mpath = self.__memento_dir
            if not os.path.exists(mpath):
                os.mkdir(mpath)
            mpath = os.path.join(mpath, response["handle"].lower())
            if not os.path.exists(mpath):
                os.mkdir(mpath)
            mpath = os.path.join(mpath, response["domain"])
            if not os.path.exists(mpath):
                os.mkdir(mpath)
            mpath = os.path.join(mpath, response["archive"])
            if not os.path.exists(mpath):
                os.mkdir(mpath)
            mpath = os.path.join(mpath, response["wrep"] + response["lang"])
            if not os.path.exists(mpath):
                os.mkdir(mpath)
            try:
                mpath = os.path.join(mpath, str(response["timestamp"]) + self.__constants.WARC_EXT)
                with open(mpath, "wb") as output:
                    writer = WARCWriter(output, gzip=True)
                    resp = requests.get(murl,
                                        headers={'Accept-Encoding': 'identity'},
                                        stream=True, timeout=120)

                    # get raw headers from urllib3
                    headers_list = resp.raw.headers.items()
                    http_headers = StatusAndHeaders('200 OK', headers_list, protocol='HTTP/1.1')
                    record = writer.create_warc_record(mpath, 'response',
                                                       payload=resp.raw,
                                                       http_headers=http_headers)
                    writer.write_record(record)
                return True
            except requests.exceptions.TooManyRedirects as err:
                with open("/home/msiddique/WSDL_Work/CongressionalTweetsAnalysis/TooMany.txt", "a+") as fobj:
                    fobj.write(murl + "\n")
            except requests.exceptions.ConnectTimeout as err:
                print(murl + "Connection Timeout")
                with open("/home/msiddique/WSDL_Work/CongressionalTweetsAnalysis/TooMany.txt", "a+") as fobj:
                    fobj.write(murl + "\n")
            except Exception as e:
                self.__write_error_logs("Memento Write Error: " + str(e) + "URL:" + murl)
        return False

    def read_memento(self, murl=None):
        """
        This function is for reading memento content.

        Parameters:
            murl (str):URI-M

        Returns:
            (str): Content on Success and None on Failure
        """
        mpath = self.lookup_memento(murl)
        if mpath:
            if self.__constants.WARC_EXT in mpath:
                try:
                    with open(mpath, 'rb') as stream:
                        for record in ArchiveIterator(stream):
                            if record.rec_type == 'response':
                                return record.content_stream().read()
                except Exception as e:
                    self.__write_error_logs("Memento Read Error: " + str(e))
            elif ".html" in mpath:
                try:
                    with open(mpath, "r") as stream:
                        return stream.read()
                except Exception as e:
                    self.__write_error_logs("Memento Read Error: " + str(e))
        return None

    def lookup_memento(self, murl=None):
        """
        This function looks up for mementos.

        Parameters:
            murl (str): URI-M

        Returns:
            (str): Path of Memento on Success and None on Failure
        """
        response = Utils.get_murl_info(murl)
        mpath = os.path.join(self.__memento_dir, response["handle"].lower(), response["domain"], response["archive"],
                             response["wrep"], response["lang"], response["timestamp"] + self.__constants.WARC_EXT)
        if os.path.exists(mpath) and os.stat(mpath).st_size > 0:
            return mpath
        else:
            mpath = os.path.join(self.__memento_dir, response["handle"].lower(), response["archive"],
                                 response["wrep"], response["lang"], response["timestamp"] + ".html")
            if os.path.exists(mpath):
                return mpath
        return None

    def write_timemap(self, turl=None, tm_content=None):
        """
        This is function to write TimeMap.

        Parameters:
            turl (str): Twitter URL
            tm_content (str): TimeMap Content
        Returns:
            (bool): True on Success and False on Failure
        """
        tresponse = Utils.get_turl_info(turl)
        tmpath = self.__timemap_dir
        if not os.path.exists(tmpath):
            os.mkdir(tmpath)
        tmpath = os.path.join(tmpath, tresponse["handle"].lower())
        if not os.path.exists(tmpath):
            os.mkdir(tmpath)
        tmpath = os.path.join(tmpath, tresponse["domain"])
        if not os.path.exists(tmpath):
            os.mkdir(tmpath)
        tmpath = os.path.join(tmpath, tresponse["wrep"] + tresponse["lang"])
        if not os.path.exists(tmpath):
            os.mkdir(tmpath)
        millis = int(round(time.time() * 1000))
        try:
            tmpath = os.path.join(tmpath, str(Utils.epochtime_to_memento(millis)) + self.__constants.TM_EXT)
            with open(tmpath, "w") as tm_ofile:
                tm_ofile.write(tm_content)
            return True
        except Exception as e:
            self.__write_error_logs("TimeMap Write Error: " + str(e))
        return False

    def read_timemap(self, turl=None):
        """
        This function is for reading TimeMap.

        Parameters:
            turl (str): Twitter URL

        Returns:
            (list): Content on Success and None on Failure
        """
        if self.lookup_timemap(turl):
            try:
                tmpath = self.__timemap_dir
                tresponse = Utils.get_turl_info(turl)
                tmpath = os.path.join(tmpath, tresponse["handle"].lower())
                tmpath = os.path.join(tmpath, tresponse["domain"], tresponse["wrep"] + tresponse["lang"])
                urims = []
                for time_map in os.listdir(tmpath):
                    with open(os.path.join(tmpath, time_map), "r") as tm_ofile:
                        for line in tm_ofile:
                            if not line.startswith("@"):
                                if line not in urims:
                                    urims.append(line)
                return urims
            except Exception as e:
                self.__write_error_logs("TimeMap Read Error: " + str(e))
        return None

    def lookup_timemap(self, turl=None):
        """
        This function looks up for TimeMap.

        Parameters:
            turl (str): Twitter URL

        Returns:
            (bool): True on Success and False on Failure
        """
        tmpath = self.__timemap_dir
        tresponse = Utils.get_turl_info(turl)
        tmpath = os.path.join(tmpath, tresponse["handle"].lower())
        tmpath = os.path.join(tmpath, tresponse["domain"], tresponse["wrep"] + tresponse["lang"])
        if os.path.exists(tmpath) and len(os.listdir(tmpath)) > 0:
            return True
        return False

    def write_parsed_memento(self, murl=None, pmcontent=""):
        """
        This is function to write Parsed Memento Content.

        Parameters:
            murl (str): URI-M
            pmcontent (str): Parsed Memento Content
        Returns:
            (bool): True on Success and False on Failure
        """
        if self.lookup_parsed_memento(murl):
            return True
        else:
            response = Utils.get_murl_info(murl)
            pm_path = self.__pmemento_dir
            if not os.path.exists(pm_path):
                os.mkdir(pm_path)
            pm_path = os.path.join(pm_path, response["handle"].lower())
            if not os.path.exists(pm_path):
                os.mkdir(pm_path)
            pm_path = os.path.join(pm_path, response["domain"])
            if not os.path.exists(pm_path):
                os.mkdir(pm_path)
            pm_path = os.path.join(pm_path, response["archive"])
            if not os.path.exists(pm_path):
                os.mkdir(pm_path)
            pm_path = os.path.join(pm_path, response["wrep"] + response["lang"])
            if not os.path.exists(pm_path):
                os.mkdir(pm_path)
            try:
                pm_path = os.path.join(pm_path, response["timestamp"] + self.__constants.PARSE_MEM_EXT)
                with open(pm_path, "w") as pm_ofile:
                    pm_ofile.write(pmcontent)
                return True
            except Exception as e:
                self.__write_error_logs("Parsed Memento Write Error: " + str(e))
        return False

    def read_parsed_memento(self, murl=None):
        """
        This function is for reading Parsed Memento.

        Parameters:
            murl (str): URI-M

        Returns:
            (str): Content on Success and None on Failure
        """
        if self.lookup_parsed_memento(murl):
            try:
                response = Utils.get_murl_info(murl)
                pm_path = os.path.join(self.__pmemento_dir, response["handle"].lower(), response["domain"],
                                       response["archive"], response["wrep"] + response["lang"], response["timestamp"]
                                       + self.__constants.PARSE_MEM_EXT)
                with open(pm_path, "r") as pm_ofile:
                    pcontent = []
                    for line in pm_ofile:
                        pcontent.append(line.rstrip())
                return pcontent
            except Exception as e:
                self.__write_error_logs("Parsed Memento Read Error: " + str(e))
        return None

    def lookup_parsed_memento(self, murl=None):
        """
        This function looks up for Parsed Memento.

        Parameters:
            murl (str): URI-M

        Returns:
            (bool): True on Success and False on Failure
        """
        response = Utils.get_murl_info(murl)
        pm_path = os.path.join(self.__pmemento_dir, response["handle"].lower(), response["domain"], response["archive"],
                               response["wrep"] + response["lang"], response["timestamp"]
                               + self.__constants.PARSE_MEM_EXT)
        if os.path.exists(pm_path):
            return True
        else:
            return False

    def write_json_outputs(self, thandle,  fname=None, fcontent=None):
        """
        This is function to write JSON Content.

        Parameters:
            thandle (str): Twitter Handle
            fname (str): File Name
            fcontent (str): File Content
        Returns:
            (bool): True on Success and False on Failure
        """
        try:

            json_path = self.__json_dir
            if not os.path.exists(json_path):
                os.mkdir(json_path)
            json_path = os.path.join(json_path, thandle + self.__constants.USCORE + fname + self.__constants.JSON_EXT)
            with open(json_path, "w") as ofile:
                json.dump(fcontent, ofile)
            return True
        except Exception as e:
            self.__write_error_logs("write_json_outputs: " + str(e))
        return False

    def read_json_outputs(self, thandle, fname):
        """
        This function is for reading JSON file Content.

        Parameters:
            thandle (str): Twitter Handle
            fname (str): File Name

        Returns:
            (str): Content on Success and None on Failure
        """
        json_path = os.path.join(self.__json_dir, thandle + self.__constants.USCORE + fname + self.__constants.JSON_EXT)
        if os.path.exists(json_path):
            with open(json_path) as ofile:
                return json.load(ofile)
        return None

    '''
    Function to lookup Deleted Tweets Json entry
    '''
    def lookup_deleted_tweets(self, thandle="john", tid=None):
        """
        This function looks up for a tweet ID in Deleted Tweets file.

        Parameters:
            thandle (str): Twitter Handle
            tid (str): Twitter ID

        Returns:
            (bool): True on Success and False on Failure
        """
        dt_path = os.path.join(self.__dtweet_dir, thandle.lower() + self.__constants.DT_EXT)
        if os.path.exists(dt_path):
            with open(dt_path, "r") as ofile:
                dtweet_content = json.load(ofile)
                for entry in dtweet_content:
                    if entry["TweetId"] == tid:
                        return True
        return False

    '''
    Function to write Deleted Tweets Json entry
    '''
    def write_deleted_tweets(self, thandle="john", dtweet_json=None):
        """
        This is function to write Deleted Tweets Content.

        Parameters:
            thandle (str): Twitter Handle
            dtweet_json (str): File Content
        Returns:
            (bool): True on Success and False on Failure
        """
        try:
            dt_path = self.__dtweet_dir
            if not os.path.exists(dt_path):
                os.mkdir(dt_path)
            dt_path = os.path.join(dt_path, thandle.lower() + self.__constants.DT_EXT)
            if os.path.exists(dt_path):
                with open(dt_path, "r") as ofile:
                    dt_content = json.load(ofile)
                if isinstance(dt_content, list):
                    for entry in dt_content:
                        dt_content.append(entry)
                else:
                    dt_content.append(dtweet_json)
            else:
                if not isinstance(dtweet_json, list):
                    dt_content = [dtweet_json]
                else:
                    dt_content = dtweet_json
            with open(dt_path, "w") as ofile:
                json.dump(dt_content, ofile)
            return True
        except Exception as e:
            self.__write_error_logs("write_deleted_tweets: " + str(e))
        return False

    def write_follower_count(self, thandle="john", fcontent=None):
        """
        This is function to write Follower Count.

        Parameters:
            thandle (str): Twitter Handle
            fcontent (dict): File Content
        Returns:
            (bool): True on Success and False on Failure
        """
        try:
            if not self.lookup_follower_count(thandle, fcontent["URI-M"]):
                fpath = self.__fcount_dir
                if not os.path.exists(fpath):
                    os.mkdir(fpath)
                if os.path.exists(os.path.join(self.__fcount_dir, thandle + ".csv")):
                    csv_file = open(os.path.join(self.__fcount_dir, thandle + ".csv"), "a+")
                    fieldnames = ["MementoTimestamp", "URI-M", "FollowerCount", "DateTime"]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                else:
                    csv_file = open(os.path.join(self.__fcount_dir, thandle + ".csv"), "w")
                    fieldnames = ["MementoTimestamp", "URI-M", "FollowerCount", "DateTime"]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                writer.writerow(fcontent)
                csv_file.close()
            return True
        except Exception as e:
            self.__write_error_logs("write_follower_count: " + str(e))
        return False

    def lookup_follower_count(self, thandle="john", urim=None):
        """
        This function looks up for a Follower Count.

        Parameters:
            thandle (str): Twitter Handle
            urim (str): URI-M

        Returns:
            (bool): Dictionary of Follower Count on Success and None on Failure
        """
        if os.path.exists(os.path.join(self.__fcount_dir, thandle + ".csv")):
            with open(os.path.join(self.__fcount_dir, thandle + ".csv"), "r") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if row["URI-M"] == urim:
                        return row["FollowerCount"]
        return None
