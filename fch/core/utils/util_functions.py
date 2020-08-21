import datetime
import ast
import re
import bs4
import os
import sys


class Utils:
    """
    This is a class for Utility Functions.
    """

    @staticmethod
    def check_memento(dmanager, memento):
        mcontent = dmanager.read_memento(memento)
        if mcontent is not None:
            soup = bs4.BeautifulSoup(mcontent, "html.parser")
            if soup.find("html") is None or not soup.find("html").has_attr("lang"):
                return False
            else:
                return True

    @staticmethod
    def memento_to_epochtime(mtime):
        """
        Function to convert memento datetime to UTC milliseconds

        Parameters:
            mtime (str): Memento Datetime

        Returns:
            (int): Memento Datetime in milliseconds on Success and None on Failure
        """
        try:
            mdate = datetime.datetime.strptime(mtime, "%Y%m%d%H%M%S")
            epoch = datetime.datetime.utcfromtimestamp(0)
            mepoch = int((mdate - epoch).total_seconds())
            return mepoch
        except Exception as e:
            if mtime != "-1":
                sys.stderr.write("memento_to_epochtime: " + str(mtime) + "   " + str(e) + "\n")
        return None

    @staticmethod
    def epochtime_to_memento(tmillis):
        """
        Function to convert timestamp in millis to Memento datetime

        Parameters:
            tmillis (int): Time in milliseconds

        Returns:
            (int): Memento Datetime on success and None on Failure
        """

        try:
            mdate = datetime.datetime.fromtimestamp(tmillis / 1000)
            mtime = str(mdate.year)
            if mdate.month < 10:
                mtime += "0"
            mtime += str(mdate.month)
            if mdate.day < 10:
                mtime += "0"
            mtime += str(mdate.day)
            if mdate.hour < 10:
                mtime += "0"
            mtime += str(mdate.hour)
            if mdate.minute < 10:
                mtime += "0"
            mtime += str(mdate.minute)
            if mdate.second < 10:
                mtime += "0"
            mtime += str(mdate.second)
            return mtime
        except Exception as e:
            sys.stderr.write("epochtime_to_memento: " + str(e) + "\n")
        return None

    @staticmethod
    def get_timerange(constants, config, db_live=None):
        """
        Function to get the minimum and maximum timestamp for the analysis

        Parameters:
            constants (Constants): for Constants
            config (ConfigurationReader): for Configuration
            db_live (collection): Live Tweets Collection

        Returns:
            (int): Minimum Timestamp
            (int): maximum Timestamp
        """
        min_time = str(config.start_time)
        max_time = str(config.end_time)
        if not Utils.memento_to_epochtime(min_time) and not Utils.memento_to_epochtime(max_time):
            min_time = constants.TWITTER_FOUND_DATE
            cur_time = datetime.datetime.now()
            max_time = cur_time.strftime("%Y%m%d%H%M%S")
        elif not Utils.memento_to_epochtime(min_time) and Utils.memento_to_epochtime(max_time):
            min_time = constants.TWITTER_FOUND_DATE
        elif Utils.memento_to_epochtime(min_time) and not Utils.memento_to_epochtime(max_time):
            cur_time = datetime.datetime.now()
            max_time = cur_time.strftime("%Y%m%d%H%M%S")
        return int(min_time), int(max_time)

    @staticmethod
    def parse_timemap(dmanager, constants, turl, config_reader=None, stime=None, etime=None):
        """
        This function is for parsing the timemap between the start and end time and getting URI-Ms

        Parameters:
            dmanager (DataManager): DataManger Object
            constants (Constants): Constants
            turl (str): Twitter URL
            stime (int): Start Time
            etime (int): End Time

        Returns:
             lurims (list: List of URI-Ms
        """
        try:
            if os.path.exists(os.path.join(os.getcwd(), "mementos.txt")):
                lurims = []
                with open(os.path.join(os.getcwd(), "mementos.txt"), "r") as fobj:
                    for line in fobj:
                        lurims.append(ast.literal_eval(line.rstrip()))
                return lurims

            timemap_content = dmanager.read_timemap(turl)
            if timemap_content:
                lurims = []
                srange = Utils.memento_to_epochtime(str(stime))
                erange = Utils.memento_to_epochtime(str(stime)) + int(config_reader.frequency)
                for line in timemap_content:
                    if constants.ERROR404 in line:
                        return None
                    elif not (line.startswith("!") or line.startswith("@")) and line.rstrip():
                        line_split = line.rstrip().split(" ", 1)
                        memento = ast.literal_eval(line_split[1])
                        if config_reader.debug: sys.stdout.write("parse_timemap: " + str(memento) + "\n")
                        response = Utils.get_turl_info(turl)
                        response = Utils.get_murl_info(memento, response["handle"])
                        if response["archive"] not in ["archive.is", "archive.today", "perma.cc", "webarchive.loc.gov", "web.archive.bibalex.org"]:
                            mtime = line_split[0]
                            if config_reader.debug: sys.stdout.write("parse_timemap: " + str(mtime) + "\n")
                            if stime <= int(mtime) <= etime:
                                if config_reader.frequency == 0:
                                    lurims.append(memento)
                                else:
                                    mtime = Utils.memento_to_epochtime(mtime)
                                    if srange <= mtime <= erange:
                                        # if Utils.check_memento(dmanager, memento):
                                        srange = erange
                                        erange += int(config_reader.frequency)
                                        lurims.append(memento)
                                    elif mtime > erange:
                                        # if Utils.check_memento(dmanager, memento):
                                        lurims.append(memento)
                                        while srange <= mtime:
                                            srange = erange
                                            erange += int(config_reader.frequency)
                            elif Utils.memento_to_epochtime(str(etime)) < Utils.memento_to_epochtime(mtime):
                                break
                with open(os.path.join(os.getcwd(), "mementos.txt"), "w") as fobj:
                    if config_reader.debug: sys.stdout.write("parse_timemap: Going to write memento.txt file" + "\n")
                    for urim in lurims:
                        fobj.write(str(urim) + "\n")
                return lurims
        except Exception as e:
            sys.stderr.write("parse_timemap: " + str(e) + "\n")
        return None

    @staticmethod
    def get_turl_info(turl):
        """
        This function parses semantics of a Twitter URL.

        Parameters:
            turl (str): Twitter URL

        Returns:
             (dict): Dictionary containing Domain, Handle, with_replies and lang information
        """
        reg = re.compile(r'https?://(www\.)?(?P<domain>mobile)?([\w\.\-]+)(:\d+)?/(?P<handle>\w+)'
                         r'((\/(?P<wrep>with_replies))?(\/?\?((lang|locale)=(?P<lang>[\w\-]+))?.*)?)?', re.I)
        response = reg.match(turl)
        response = response.groupdict()
        response["lang"] = (response["lang"] if response["lang"] else "default")
        response["wrep"] = (response["wrep"] + "_" if response["wrep"] else "")
        response["domain"] = (response["domain"] if response["domain"] else "desktop")
        return response

    @staticmethod
    def get_murl_info(*args):
        """
        This function parses semantics of a URI-M.

        Parameters:
            args (variable arguments): Index 1: URI-M/ TimeMap CDXJ Entry, Index 2: Twitter Handle

        Returns:
             (dict): Dictionary containing Archive, Memento Timestamp, Domain, Handle, with_replies and lang information
        """
        flag = True
        try:
            archive_list = ["perma.cc", "archive.is"]
            input = ast.literal_eval(str(args[0]))
            murl = input["uri"]
            for archive in archive_list:
                if archive in murl:
                    flag = False
        except Exception as e:
            murl = args[0]

        if flag:
            reg = re.compile(r'https?://(www\.)?(?P<archive>[\w\.\-]+)(:\d+)?(\/\w+)?(/archive)?/(?P<timestamp>\d+)([a-z]'
                             r'{2}_)?/(?P<TwitterURL>https?://(www\.)?(?P<domain>mobile)?[\w\.\-]+(:\d+)?(\/)+(?P<handle>'
                             r'\w+)'
                             r'((\/(?P<wrep>with_replies))?\/?\?((lang|locale)=(?P<lang>[\w\-]+))?.*)?)', re.I)
            response = reg.match(murl)
            response = response.groupdict()
            response["lang"] = (response["lang"] if response["lang"] else "default")
            response["wrep"] = (response["wrep"] + "_" if response["wrep"] else "")
            response["domain"] = (response["domain"] if response["domain"] else "desktop")
        else:
            reg = re.compile(r'https?://(www\.)?(?P<archive>[\w\.\-]+)(:\d+)?/.*', re.I)
            response = reg.match(murl)
            response = response.groupdict()
            mdate = datetime.datetime.strptime(input["datetime"], "%a, %d %b %Y %H:%M:%S %Z")
            response["timestamp"] = mdate.strftime("%Y%m%d%H%M%S")
            response["lang"] = "default"
            response["wrep"] = ""
            response["domain"] = "desktop"
            if len(args) > 1:
                response["TwitterURL"] = "https://twitter.com/" + args[1].lower()
                response["handle"] = args[1].lower()
            else:
                response["TwitterURL"] = ""
                response["handle"] = ""
        return response

    @staticmethod
    def convert_digits_to_english(number):
        # ldigits good for: fr, es, de, it, id, pt, tr, ru, ar, en, ru, ja, ko, nl, fil, ms, hi, no, sv, fi, da, po, hu,
        # fa, he, ur, th, uk, ca, ga, el, eu, cs, gl, ro, hr, en-gb, bn, bg, sr, sk, gu, mr, kn, ta, va
        # zh-tw zh-cn, vi: To de added
        ldigits = [
            "0٠০ 〇*零०۰-๐૦௦೦零",
            "1١১一१۱א๑૧௧೧壹",
            "2٢২二२۲ב๒૨௨೨貳",
            "3٣৩三३۳๓ג૩௩೩叄",
            "4٤৪四४۴ד๔૪௪೪肆",
            "5٥৫五५۵๕ה૫௫೫伍",
            "6٦৬六६۶ו๖૬௬೬陸",
            "7٧৭七७۷ז๗૭௭೭柒",
            "8٨৮八८۸๘૮ח௮೮捌",
            "9٩৯九९۹ט๙૯௯೯玖",
            "十י௰拾"]
        # For ko, ja mapping
        lmapping = {
            "ja": "廿卅百千万億兆京",
            "value": [20, 30, 100, 1000, 10000, 100000000, 1000000000000, 10000000000000000]}
        # JAPANESE Number system is complex check it
        conv = 0
        for digit in number:
            for index in range(len(ldigits)):
                if digit in ldigits[index]:
                    conv = (10 * conv) + index
                    break
        return conv
