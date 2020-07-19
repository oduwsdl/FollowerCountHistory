import datetime
import twitter
import ast
import re


class Utils:
    """
    This is a class for Utility Functions.
    """

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
            print("memento_to_epochtime: " + str(e))
            print("memento_to_epochtime: " + str(mtime))
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
            print("epochtime_to_memento: " + str(e))
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
        if config.mode == 1:
            min_time = config.start_time
            max_time = config.end_time
            if not min_time and not max_time:
                min_time = constants.TWITTER_FOUND_DATE
                cur_time = datetime.datetime.now()
                max_time = cur_time.strftime("%Y%m%d%H%M%S")
            elif not min_time and max_time:
                min_time = constants.TWITTER_FOUND_DATE
            elif min_time and not max_time:
                cur_time = datetime.datetime.now()
                max_time = cur_time.strftime("%Y%m%d%H%M%S")
        else:
            tstamps = []
            cursor = db_live.find()
            for row in cursor:
                tstamps.append(int(row["TweetTimestamp"]))
            min_time = min(tstamps)
            max_time = max(tstamps)
            min_time = datetime.datetime.fromtimestamp(min_time).strftime('%Y%m%d%H%M%S')
            max_time = datetime.datetime.fromtimestamp(max_time).strftime('%Y%m%d%H%M%S')
        return int(min_time), int(max_time)

    @staticmethod
    def create_twitter_instance():
        """
        Create Twitter Instance. All the fields can be collected from the developer site of Twitter

        Returns:
            api (TwitterAPI): Twitter API Object
        """
        api = twitter.Api(consumer_key='5Q3CFnvq02nKj6kI9gRpGNHXH',
                          consumer_secret='4OBnuBjedjwZUZmtslwzzPmWxeQtN7LHUeYHf4jsqZjQkEyW4v',
                          access_token_key='907341293717737473-for4ikiKhPAHxD54pnRqhJSPpr1QmNB',
                          access_token_secret='jV6TplxXfCQOu8C8zArB2wzlwGisq2Y0kRHUtrvuKYQNr',
                          sleep_on_rate_limit=True)
        return api

    @staticmethod
    def parse_timemap(dmanager, constants, turl, stime=None, etime=None):
        """
        This function is for parsing the timemap between the start and end time and getting URI-Ms

        Parameters:
            dmanager (DataManager): DataManger Object
            constants (Constants): Constants
            turl (str): Twitter URL
            stime (int): Start Time
            etime (int): End Time

        Returns:
             lurims (list): List of URI-Ms
        """
        timemap_content = dmanager.read_timemap(turl)
        if timemap_content:
            lurims = []
            for line in timemap_content:
                if constants.ERROR404 in line:
                    return None
                elif not line.startswith("@") and line.rstrip():
                    line_split = line.split(" ", 1)
                    memento = ast.literal_eval(line_split[1])
                    mtime = line_split[0]
                    if stime <= int(mtime) <= etime:
                        lurims.append(memento)
            return lurims
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
