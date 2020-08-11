import bs4
import ast
from datetime import datetime
import os
import sys
from functools import partial
import re
from fch.core.utils.util_functions import Utils

class FollowerParser:

    def __init__(self, thandle, constants, dmanager, conf_reader):
        self.__thandle = thandle
        self.__constants = constants
        self.__dmanager = dmanager
        self.__conf_reader = conf_reader
        self.__lfollower = []

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

    def parse_mementos(self, turl):
        mintime, maxtime = Utils.get_timerange(self.__constants, self.__conf_reader)
        lurims = Utils.parse_timemap(self.__dmanager, self.__constants, turl, self.__conf_reader, mintime, maxtime)
        if lurims:
            for urim in lurims:
                response = Utils.get_murl_info(urim, self.__thandle)
                if self.__conf_reader.debug: sys.stdout.write("parse_mementos: " + str(response) + "\n")
                # If archive.is mementos then skip it, as we do not parse them
                if response["archive"] not in ["archive.is", "archive.md"]:
                    mcontent = self.__dmanager.read_memento(urim)
                    if mcontent is None:
                        if self.__conf_reader.debug: sys.stdout.write("parse_mementos: read_memento:  " + str(urim) + "   " + str(mcontent) + "\n")
                    else:
                        if self.__conf_reader.debug: sys.stdout.write("parse_mementos: read_memento:  " + str(urim) + "   True" + "\n")
                        self.__parse_memento(mcontent, urim)
        return self.__lfollower

    '''
    Function to fetch Followers, Tweet Count, Likes, Replies. retweets from each memento
    '''

    def __parse_memento(self, mcontent, urim):
        murl = urim["uri"]
        soup = bs4.BeautifulSoup(mcontent, "html.parser")
        try:
            lselector = ["li.ProfileNav-item.ProfileNav-item--followers", "ul.user-stats.clearfix",
                            "table.stats.js-mini-profile-stats", "ul.stats.js-mini-profile-stats",
                            "div.stats", "div#section", "table.stats", "div#side"]

            lfollower_tags = list(filter(lambda x: soup.select(x), lselector))
            if lfollower_tags:
                if self.__conf_reader.debug: sys.stdout.write(str(urim) + "  " + str(lfollower_tags[0]) + "\n")
                lfunctions = [partial(self.__parse_case1, soup), partial(self.__parse_case2, soup),
                                partial(self.__parse_case3, soup), partial(self.__parse_case4, soup),
                                partial(self.__parse_case5, soup), partial(self.__parse_case6, soup),
                                partial(self.__parse_case7, soup), partial(self.__parse_case8, soup)]
                x = lambda lfollower_tags, lfunctions, lselector: lfunctions[lselector.index(lfollower_tags[0])]()
                tcount = x(lfollower_tags, lfunctions, lselector)
                if tcount:
                    if self.__conf_reader.debug: sys.stdout.write("URIM: {} Converted: {}".format(murl, tcount) + "\n")
                    response = Utils.get_murl_info(urim, self.__thandle.lower())
                    self.__lfollower.append({"MementoDatetime": response["timestamp"],
                                                "URIM": murl, "FollowerCount":tcount})
            else:
                with open(os.path.join(os.getcwd(), "NonParsedMementos.txt"), "a+") as \
                        ofile:
                    ofile.write("No selector found: " + murl + "\n")
        except Exception as e:
            sys.stderr.write("parse_memento: URL: {}: Error: {}".format(murl, e) + "\n")
            with open(os.path.join(os.getcwd(), "NonParsedMementos.txt"), "a+") as \
                ofile:
                ofile.write("Error: " + murl + "\n")


    def __parse_case1(self, soup):
        if self.__conf_reader.debug: sys.stdout.write("__parse_case1" + "\n")
        follower_tags = soup.select("li.ProfileNav-item.ProfileNav-item--followers")
        for tags in follower_tags:
            if self.__conf_reader.debug: sys.stdout.write(str(tags) + "\n")
            fcount_temp = None
            if tags.select("span.ProfileNav-value")[0].has_attr("data-count"):
                fcount = tags.select("span.ProfileNav-value")[0]["data-count"]
            else:
                fcount = tags.select("a.ProfileNav-stat.ProfileNav-stat--link.u-borderUserColor")
                if self.__conf_reader.debug: sys.stdout.write(str(fcount) + "\n")
                if fcount:
                    fcount = re.sub("\D", '', fcount[0]["title"])
                else:
                    fcount_temp = tags.select("span.ProfileNav-value")[0].text
                    fcount = re.sub("\D", '', fcount_temp)
        if self.__conf_reader.debug: sys.stdout.write("Follower Count: {}".format(fcount) + "\n")
        tcount = Utils.convert_digits_to_english(fcount)
        if fcount_temp is not None:
            if fcount_temp[-1] in ["k", "K", "ಸಾ"]:
                tcount = tcount * 1000
            elif fcount_temp[-1] in ["m", "M"]:
                tcount = tcount * 1000000
            elif fcount_temp in ["b", "B"]:
                tcount = tcount * 1000000000
        return tcount

    def __parse_case2(self, soup):
        if self.__conf_reader.debug: sys.stdout.write("__parse_case2" + "\n")
        follower_tags = soup.select("ul.user-stats.clearfix")
        if self.__conf_reader.debug: sys.stdout.write(str(follower_tags[0]) + "\n")
        tags = follower_tags[0].select("a.user-stats-count.user-stats-followers")[0].text
        tcount = re.sub("\D", '', tags)
        return tcount

    def __parse_case3(self, soup):
        if self.__conf_reader.debug: sys.stdout.write("__parse_case3" + "\n")
        follower_tags = soup.select("table.stats.js-mini-profile-stats")
        # for i in follower_tags[0].select("a.js-nav"):
        #    self.__write_logs(i)
        if self.__conf_reader.debug: sys.stdout.write(str(follower_tags[0].select("a.js-nav")[2]) + "\n")
        tags = follower_tags[0].select("a.js-nav")[2].select("strong")
        if tags[0].has_attr("title"):
            tcount = tags[0]["title"]
        else:
            tcount = tags[0].text
        tcount = re.sub("\D", '', tcount)
        return tcount

    def __parse_case4(self, soup):
        if self.__conf_reader.debug: sys.stdout.write("__parse_case4" + "\n")
        follower_tags = soup.select("ul.stats.js-mini-profile-stats")
        if self.__conf_reader.debug: sys.stdout.write(str(follower_tags[0]) + "\n")
        tags = follower_tags[0].select("a")[2].select("strong")
        if tags[0].has_attr("title"):
            tcount = tags[0]["title"]
        else:
            tcount = tags[0].text
        tcount = re.sub("\D", '', tcount)
        return tcount

    def __parse_case5(self, soup):
        if self.__conf_reader.debug: sys.stdout.write("__parse_case5" + "\n")
        follower_tags = soup.select("div.stats")
        if self.__conf_reader.debug: sys.stdout.write(str(follower_tags[0]) + "\n")
        tags = follower_tags[0].select("span.stats_count.numeric")[1].text
        tcount = re.sub("\D", '', tags)
        return tcount

    def __parse_case6(self, soup):
        if self.__conf_reader.debug: sys.stdout.write("__parse_case6" + "\n")
        follower_tags = soup.select("div#section")
        if self.__conf_reader.debug: sys.stdout.write(str(follower_tags[0]) + "\n")
        tags = follower_tags[0].select("table.stats")[0].select("a#follower_count_link")[0].select("span.stats_count.numeric")[0].text
        tcount = re.sub("\D", '', tags)
        return tcount

    def __parse_case7(self, soup):
        if self.__conf_reader.debug: sys.stdout.write("__parse_case7" + "\n")
        follower_tags = soup.select("table.stats")
        if self.__conf_reader.debug: sys.stdout.write(str(follower_tags[0]) + "\n")
        tags = follower_tags[0].select("span.stats_count.numeric")[1].text
        tcount = re.sub("\D", '', tags)
        return tcount

    def __parse_case8(self, soup):
        if self.__conf_reader.debug: sys.stdout.write("__parse_case8" + "\n")
        follower_tags = soup.select("div#side")
        tags = follower_tags[0].select("ul.stats")
        if tags:
            if self.__conf_reader.debug: sys.stdout.write(str(tags[0]) + "\n")
            tag = tags[0].select("span.stats_count.numeric")[1].text
            tcount = re.sub("\D", '', tag)
        else:
            if self.__conf_reader.debug: sys.stdout.write(str(follower_tags[0]) + "\n")
            tags = follower_tags[0].select("ul")[1].select("li")[1]
            if "Followers" not in tags or "Followers:" not in tags:
                tags = follower_tags[0].select("ul")[1].select("li")[2]
                if "Followers" not in tags or "Followers:" not in tags:
                    return None
            tcount = re.sub("\D", '', tags.text)
        return tcount
