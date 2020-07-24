#!/usr/bin/env python3

import argparse
import os
import sys

from core.config.configreader import ConfigurationReader
from core.config.configwriter import ConfigurationWriter
from core.utils.constants import Constants
from core.datamanager import DataManager
from core.utils.util_functions import Utils

from follower.followercount import FollowerCount

def init(**kwargs):

    ConfigurationWriter(**kwargs)
    config_reader = ConfigurationReader()
    constants = Constants()
    dmanager = DataManager(config_reader, constants)
    return dmanager, config_reader, constants


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

def run_follower(**kw):
    if check_mtime_format(str(kw["st"])) and check_mtime_format(str(kw["et"])):
        dmanager, config_reader, constants = init(**kw)
        if config_reader.debug: sys.stdout.write("Twitter Handle: " + kw["thandle"] + "\n")
        fcount = FollowerCount(kw["thandle"], config_reader, constants, dmanager)
        fcount.get_follower_count()
        if config_reader.debug: sys.stdout.write("follower count successfully completed for : " + kw["thandle"] + "\n")
    else:
        if config_reader.debug: sys.stdout.write("Enter valid Memento Datetime in 14 digits format (yyyymmddHHMMSS)" + "\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Follower Count History (fch)", prog="fch")

    parser.add_argument("thandle", help="Enter a Twitter handle")
    parser.add_argument("--st", type=int, metavar="", default=-1, help="Memento start datetime format (in RFC 1123 datetime format)")
    parser.add_argument("--et", type=int, metavar="", default=-1, help="Memento end datetime (in RFC 1123 datetime format)")
    parser.add_argument("--freq", metavar="", default="all", help="Sampling frequency of mementos(in seconds)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--out", action='store_true', default=False, help="Path for follower count output in CSV format")
    group.add_argument("--debug", action='store_true', default=False, help="Debug Mode")
    parser.set_defaults(func=run_follower)
    args = parser.parse_args()
    try:
        args.func(**vars(args))
    except Exception as e:
        print(e)
        parser.print_help()
