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

    '''    
    Function to fetch Followers, Tweet Count, Likes, Replies. retweets from each memento
    '''

    def parse_memento(self, mcontent, murl):
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
                                fcount = tags.select("span.ProfileNav-value")[0].text
                                fcount = re.sub("\D", '', fcount)
                            self.__logger.debug_log.debug("Follower Count: {}".format(fcount))
                            tcount = Utils.convert_digits_to_english(fcount)
                            self.__logger.debug_log.debug("URIM: {} Original number: {} Converted: {}".format(murl,
                                                                                                              fcount,
                                                                                                        tcount))
                            response = Utils.get_murl_info(murl)
                            self.__dmanager.write_follower_count(self.__thandle.lower(), {"MementoTimestamp":
                                                                                              response["timestamp"],
                                                                                  "URI-M": murl, "FollowerCount":
                                                                                              tcount,
                                                                  "DateTime": datetime.strptime(response["timestamp"],
                                                                                                "%Y%m%d%H%M%S")
                                                                                          })
                    else:
                        print(murl)
                        with open(os.path.join(os.path.dirname(__file__), "data", "NonParsedMementos.txt"), "a+") as \
                                ofile:
                            ofile.write("Non parsed due to selector problem: " + murl + "\n")
            else:
                print(murl)
                with open(os.path.join(os.path.dirname(__file__), "data", "NonParsedMementos.txt"), "a+") as \
                        ofile:
                    ofile.write("Non parsed due to language: " + murl + "\n")
        except Exception as e:
            self.__logger.error_log.debug("parse_memento: URL: {}: Error: {}".format(murl, e))
