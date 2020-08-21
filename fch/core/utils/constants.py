class Constants:
    """
            This class is for Constants.

            Attributes:
                JSON_EXT (str): JSON file Extention
                TM_EXT (str): TimeMap file extention
                PARSE_MEM_EXT (str): Parsed Memento file extention
                WARC_EXT (str): Memento Records stored as WARC
                DT_EXT (str): Deleted Tweets file extention
                USCORE (str): Underscore Separator
                FSLASH (str): Forward Slash Separator
                ERROR404 (str): Represents 404 error text found in mementos
                TWEET_DEL (str): Original Deleted Tweet
                ACCT_DEL (str): Account Deleted
                ACCT_SUS (str): Account Suspended
                ACCT_PRI (str): Account Private
                UNRT (str): Unretweet a Tweet
                RT_ACCT_DEL (str): Retweet Account Deleted
                RT_ACCT_SUS (str): Retweet Account Suspended
                RT_ACCT_PRI (str): Retweet Account made Private
                ORG_TWEET_OF_RT_DEL (str): Original Tweet for Retweet Deleted
                ORG_ACCT_OF_TWEET_DEL (str): Account for Original Tweet Deleted
                ORG_ACCT_OF_TWEET_SUS (str): Account for Original Tweet Suspended
                ORG_ACCT_OF_TWEET_PRI (str): Account for Original Tweet goes Private
                TWEET_404 (int): Status Code 404
                ACCT_DEL (int): Twitter Error Code for Account Deleted
                ACCT_SUS (int): Twitter Error Code for Account Suspended
                ACCT_PRI (int): Twitter Error Code for Account Private
                OT (str): Original Tweet
                RT (str): Retweet
                OT_OF_RT (str): Original Tweet of a Retweet
                MEMGATOR_URL (str): Memgator URL
                MEMGATOR_FORMAT (str): Memgator Data Format
                TWITTER_URL (str): Twitter URL
                MOBILE_TWITTER_URL (str): Twitter Mobile URL
                TWITTER_FOUND_DATE = "20160321120000"
                PRE_SNOWFLAKE_BEGIN_TID = 20
                PRE_SNOWFLAKE_END_TID = 29700859247
        """

    def __init__(self):

        """
        This is the constructor for Constants class.

        Parameters:

        """
        # File Extentions
        self.JSON_EXT = ".json"
        self.TM_EXT = ".tm"
        self.PARSE_MEM_EXT = ".parsed"
        self.WARC_EXT = ".warc.gz"
        self.DT_EXT = ".del"

        # Separators
        self.USCORE = "_"
        self.FSLASH = "/"

        # Error
        self.ERROR404 = "404 page not found"

        # Tweet Deletion Types
        self.TWEET_DEL = "A1"
        self.ACCT_DEL = "A2"
        self.ACCT_SUS = "A3"
        self.ACCT_PRI = "A4"
        self.UNRT = "AB1"
        self.RT_ACCT_DEL = "AB2"
        self.RT_ACCT_SUS = "AB3"
        self.RT_ACCT_PRI = "AB4"
        self.ORG_TWEET_OF_RT_DEL = "B1"
        self.ORG_ACCT_OF_TWEET_DEL = "B2"
        self.ORG_ACCT_OF_TWEET_SUS = "B3"
        self.ORG_ACCT_OF_TWEET_PRI = "B4"

        # Twitter Error Codes
        self.TWEET_404 = 144
        self.ACCT_DEL = 34
        self.ACCT_SUS = 63
        self.ACCT_PRI = 179

        # Tweet Types
        self.OT = "OT"
        self.RT = "RT"
        self.OT_OF_RT = "OTR"

        # Memgator Variables
        self.MEMGATOR_URL = "http://localhost:1208/timemap/"
        self.MEMGATOR_FORMAT = "cdxj"
        self.TWITTER_URL = "http://twitter.com/"
        self.MOBILE_TWITTER_URL = "https://mobile.twitter.com"
        self.TWITTER_FOUND_DATE = "20060321120000"
        self.PRE_SNOWFLAKE_BEGIN_TID = 20
        self.PRE_SNOWFLAKE_END_TID = 29700859247