********************
[TWITTER]

**********
MODE:
This is to set the mode of your analysis for finding deleted tweets.

Supported Value:
0: For getting deleted tweets based on Twitter api's usertimeline method. (Most recent 3200 tweets)
1: For providing user defined start and end time for analysis
**********

**********
START_TIMESTAMP:
This sets the start timestamp for fetching mementos. It accepts value in Memento DateTime format (20190107235959)
* Note: MODE 1 is required for using this option.
**********

**********
END_TIMESTAMP:
This sets the end timestamp for fetching mementos. It accepts value in Memento DateTime format (20190807235959)
* Note: MODE 1 is required for using this option.
**********


**********
URL_CANONICALIZATION: F
This option allows for creating canonicalized Twitter URLs.
For example, a Twitter URL will be appended with language variation and with_replies parameter.

https://twitter.com/dougjones (1 URL)
https://twitter.com/dougjones/with_replies (1 URL)
https://twitter.com/dougjones?lang=en (47 URLs for 47 languages)
https://twitter.com/dougjones/with_replies?lang=en (47 URLs for 47 languages)
Total: 96 URLs for each URI-R

Supported Value:
T: Set to True
F: Set to False
**********


********************
[COMMON]
********************

**********
OUTPUT_DIR:
This options sets the default output directory.
**********

**********
DEBUG_MODE:
This option sets the dedug mode.

Supported Value:
True: Set to True
False: Set to False
**********

********************
[TWITTER_LANGUAGES]
********************

**********
LANGUAGES: fr en ar ja es de it id pt ko tr ru nl fil ms zh-tw zh-cn hi no sv fi da pl hu fa he ur th uk ca ga el eu cs gl ro hr en-gb vi bn bg sr sk gu mr ta kn

This option lists all the languages supported in Twitter URL. When a new language is encountered in the Twitter
URL than already present in the current list add to the current list.
**********