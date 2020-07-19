import bs4
import re
from core.utils.util_functions import Utils
import ast
from datetime import datetime
import os


class FollowerParser:
    
    def __init__(self, thandle, constants, dmanager, logger):
        self.__thandle = thandle
        self.__constants = constants
        self.__logger = logger
        self.__dmanager = dmanager

    def __write_logs(self, message):
        if self.__logger.debug_log is not None:
            self.__logger.debug_log.debug(message)

    '''
    Function to get list of URIM-s between a timerange
    '''
    @classmethod
    def __get_language(cls, lang_code):
        lang_path = os.path.join(os.path.dirname(__file__), "data", "iso_lang_list.txt")
        with open(lang_path) as lfile:
            llangs = ast.literal_eval(lfile.read())
            for entry in llangs:
                if entry[0] == lang_code:
                    return entry[1]
        return None

    def parse_mementos(self, config, turl):
        mintime, maxtime = Utils.get_timerange(self.__constants, config)
        lurims = Utils.parse_timemap(self.__dmanager, self.__constants, turl, mintime, maxtime)
        if lurims:
            for urim in lurims:
                response = Utils.get_murl_info(urim, self.__thandle)
                self.__write_logs("parse_mementos: " + str(response))
                # If archive.is mementos then skip it, as we do not parse them
                if response["archive"] not in ["archive.is", "archive.md"]:
                    mcontent = self.__dmanager.read_memento(urim)
                    if mcontent is None:
                        self.__write_logs("parse_mementos: read_memento:  " + str(urim) + "   " + str(mcontent))
                    else:
                        self.__write_logs("parse_mementos: read_memento:  " + str(urim) + "   True") 
                        self.__parse_memento(mcontent, urim)

    '''    
    Function to fetch Followers, Tweet Count, Likes, Replies. retweets from each memento
    '''

    def __parse_memento(self, mcontent, urim):
        murl = urim["uri"]
        soup = bs4.BeautifulSoup(mcontent, "html.parser")
        try:
            if soup.find("html").has_attr("lang"):
                mcode = soup.find("html")["lang"]
                if mcode:
                    follower_tags = soup.select("li.ProfileNav-item.ProfileNav-item--followers")
                    if follower_tags:
                        for tags in follower_tags:
                            self.__logger.debug_log.debug(murl + " " + str(tags))
                            if tags.select("span.ProfileNav-value")[0].has_attr("data-count"):
                                fcount = tags.select("span.ProfileNav-value")[0]["data-count"]
                            else:
                                fcount_temp = tags.select("span.ProfileNav-value")[0].text
                                fcount = re.sub("\D", '', fcount_temp)
                            self.__logger.debug_log.debug("Follower Count: {}".format(fcount))
                            tcount = Utils.convert_digits_to_english(fcount)
                            if ["k", "K", "ಸಾ"] in fcount_temp:
                                tcount = tcount * 1000
                            elif ["m", "M"] in fcount_temp:
                                tcount = tcount * 1000000
                            elif ["b", "B"] in fcount_temp:
                                tcount = tcount * 1000000000
                            self.__logger.debug_log.debug("URIM: {} Original number: {} Converted: {}".format(murl,
                                                                                                              fcount,
                                                                                                        tcount))
                            response = Utils.get_murl_info(urim, self.__thandle.lower())
                            self.__dmanager.write_follower_count(self.__thandle.lower(), {"MementoTimestamp":
                                                                                              response["timestamp"],
                                                                                  "URI-M": murl, "FollowerCount":
                                                                                              tcount,
                                                                  "DateTime": datetime.strptime(response["timestamp"],
                                                                                                "%Y%m%d%H%M%S")
                                                                                          })
                    else:
                        with open(os.path.join(os.path.dirname(__file__), "data", "NonParsedMementos.txt"), "a+") as \
                                ofile:
                            ofile.write("Non parsed due to selector problem: " + murl + "\n")
            else:
                with open(os.path.join(os.path.dirname(__file__), "data", "NonParsedMementos.txt"), "a+") as \
                        ofile:
                    ofile.write("Non parsed due to language: " + murl + "\n")
        except Exception as e:
            self.__logger.error_log.debug("parse_memento: URL: {}: Error: {}".format(murl, e))
