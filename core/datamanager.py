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
    def __init__(self, config, constants):
        """
            The constructor of DataManager class.

            Parameters:
                config (ConfigurationReader): Configuration object
                constants (Constants): For constants
        """
        self.__config = config
        self.__data_dir = config.out_dir
        self.__constants = constants
        self.__memento_dir = os.path.join(self.__data_dir, "Mementos")
        self.__timemap_dir = os.path.join(self.__data_dir, "TimeMap")
        self.__pmemento_dir = os.path.join(self.__data_dir, "ParsedMementos")
        self.__dtweet_dir = os.path.join(self.__data_dir, "DeletedTweets")
        self.__json_dir = os.path.join(self.__data_dir, "JsonOutputs")
        self.__fcount_dir = os.path.join(self.__data_dir, "FollowerCount")

    def set_twitter_handle(self, thandle):
        """
            Function to set Twitter handle
            
            Parameters:
                thandle (str): Twitter handle

            Returns:
        """
        self.__thandle = thandle

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
            response = Utils.get_murl_info(murl, self.__thandle)
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
                print("Memento Write Error: " + str(e) + "URL:" + murl)
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
                    print("Memento Read Error: " + str(e))
        return None

    def lookup_memento(self, murl=None):
        """
        This function looks up for mementos.

        Parameters:
            murl (str): URI-M

        Returns:
            (str): Path of Memento on Success and None on Failure
        """
        response = Utils.get_murl_info(murl, self.__thandle)
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
            print("TimeMap Write Error: " + str(e))
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
                print("TimeMap Read Error: " + str(e))
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
            print(fcontent["URI-M"])
            print(self.lookup_follower_count(thandle, fcontent["URI-M"]))
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
            print("write_follower_count: " + str(e))
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
