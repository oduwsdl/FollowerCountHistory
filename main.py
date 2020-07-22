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
        if kw["analysis"]:
            fcount.get_follower_analysis()
        if kw["count"]:
            fcount.get_follower_count()
            if config_reader.debug: sys.stdout.write("follower count successfully completed for : " + kw["thandle"] + "\n")
        if kw["graph"]:
            fcount.plot_graph()
            if config_reader.debug: sys.stdout.write("Plot R Graph Done" + "\n")
    else:
        if config_reader.debug: sys.stdout.write("Enter valid Memento DateTime in 14 digits format (yyyymmddHHMMSS)" + "\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Follower Count History (fch)", prog="fch")

    # follower_parser = subparsers.add_parser("follower", help="Get follower count for a Twitter handle")
    parser.add_argument("thandle", help="Enter a Twitter handle")
    parser.add_argument("--st", type=int, metavar="", default=20190101000000, help="Start timestamp (in "
                                                                                            "Memento datetime format)")
    parser.add_argument("--et", type=int, metavar="", default=20200419235959, help="End timestamp (in "
                                                                                            "Memento datetime format)")
    parser.add_argument("--analysis", action='store_true', default=False, help="Follower Count analysis")
    parser.add_argument("--count", action='store_true', default=False, help="Get Follower Count")
    parser.add_argument("--frequency", metavar="", default="all", help="Frequency (in seconds)")
    parser.add_argument("--graph", action='store_true', default=False, help="Plot R Graphs")
    parser.add_argument("--debug", action='store_true', default=False, help="Debug Mode")
    parser.set_defaults(func=run_follower)
    args = parser.parse_args()
    try:
        args.func(**vars(args))
    except Exception as e:
        print(e)
        parser.print_help()
