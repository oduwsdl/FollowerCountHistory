#!/usr/bin/env	python3

import argparse
import os
import sys

from core.logger import Logger
from core.config.configreader import ConfigurationReader
from core.config.configwriter import ConfigurationWriter
from core.utils.constants import Constants
from core.datamanager import DataManager
from core.utils.util_functions import Utils

from deletedtweets.deletedtweetfinder import TweetDeletionFinder
from follower.followercount import FollowerCount
from tests.simulator import Simulator


def init(log_type, **kwargs):

    ConfigurationWriter(**kwargs)
    config_reader = ConfigurationReader()
    constants = Constants()
    logger = Logger(config_reader)
    logger.create_logging_instances(log_type)
    dmanager = DataManager(config_reader, constants, logger)
    return dmanager, config_reader, constants, logger


def check_mtime_format(mtime):
    '''
    Function to check Memento
    :param mtime:
    :return:
    '''

    if Utils.memento_to_epochtime(mtime):
        return True
    else:
        return False


def run_deleted(**kw):
    '''
    Function to deleted tweets
    :param kw:
    :return:
    '''
    if kw["mode, _m"] == 1 and check_mtime_format(str(kw["st"])) and check_mtime_format(str(kw["et"])):
        dmanager, config_reader, constants, logger = init(log_type="deleted", **kw)
        tfinder = TweetDeletionFinder(kw["thandle"], config_reader, constants, dmanager, logger)
        print("Going to find deleted tweets: " + kw["thandle"])
        tfinder.find_deleted_tweets()
    else:
        print("Enter valid Memento DateTime in 14 digits format (yyyymmddHHMMSS)")


def run_follower(**kw):
    if check_mtime_format(str(kw["st"])) and check_mtime_format(str(kw["et"])):
        print("Twitter Handle: " + kw["thandle"])
        dmanager, config_reader, constants, logger = init(log_type="follower", **kw)
        fcount = FollowerCount(kw["thandle"], config_reader, constants, dmanager, logger)
        if kw["analysis"]:
            fcount.get_follower_analysis()
        if kw["count"]:
            fcount.get_follower_count()
            print("follower count successfully completed for : " + kw["thandle"])
    else:
        print("Enter valid Memento DateTime in 14 digits format (yyyymmddHHMMSS)")


def run_tests(**kw):
    dmanager, config_reader, constants, logger = init(log_type="tests")
    sim = Simulator(dmanager, config_reader, constants, logger)
    if kw["mdtparser"]:
        sim.test_dt_memento_parser(kw["mdtparser"])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Twitter Archival Analysis (taa)", prog="taa")
    subparsers = parser.add_subparsers()

    deleted_parser = subparsers.add_parser("deleted",
                                            help="Generate a JSON file of deleted tweets for a Twitter handle")
    deleted_parser.add_argument("thandle", help="Enter a Twitter handle")
    deleted_parser.add_argument("--out, -o", metavar="", default="/data/Nauman/MementoDump", help="Output Directory")
    deleted_parser.add_argument("--mode, -m", type=int, metavar="", default=1, help="Mode 0: Recent 3200 tweets, 1:"
                                                                                   "Timerange-based")
    deleted_parser.add_argument("--can, -c", type=bool, metavar="", default=False, help="Url Cononicalization")
    deleted_parser.add_argument("--st", type=int, metavar="", default=20190101000000, help="Start timestamp (in "
                                                                                            "Memento datetime format)")
    deleted_parser.add_argument("--et", type=int, metavar="", default=20190813235959, help="End timestamp (in "
                                                                                            "Memento datetime format)")
    deleted_parser.set_defaults(func=run_deleted)

    follower_parser = subparsers.add_parser("follower", help="Get follower count for a Twitter handle")
    follower_parser.add_argument("thandle", help="Enter a Twitter handle")
    follower_parser.add_argument("--st", type=int, metavar="", default=20190101000000, help="Start timestamp (in "
                                                                                            "Memento datetime format)")
    follower_parser.add_argument("--et", type=int, metavar="", default=20200419235959, help="End timestamp (in "
                                                                                            "Memento datetime format)")
    follower_parser.add_argument("--analysis", action='store_true', default=False, help="Follower Count analysis")
    follower_parser.add_argument("--count", action='store_true', default=False, help="Get Follower Count")
    follower_parser.set_defaults(func=run_follower)

    tests_parser = subparsers.add_parser("tests", help="Run tests for follower count and deleted tweets code")
    tests_parser.add_argument("-mdtparser", metavar="", help="Enter a URIM to tests the memento parser")
    tests_parser.set_defaults(func=run_tests)

    args = parser.parse_args()
    try:
        args.func(**vars(args))
    except Exception as e:
        print(e)
        parser.print_help()
