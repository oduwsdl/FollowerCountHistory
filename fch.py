#!/usr/bin/env python3

import argparse
import sys
import re

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

def get_thandle(turl):
    reg = re.compile(r'(https?://(www\.)?(?P<domain>mobile)?([\w\.\-]+)(:\d+)?/)?(@)?(?P<handle>\w+)((\/(?P<wrep>with_replies))?(\/?\?((lang|locale)=(?P<lang>[\w\-]+))?.*)?)', re.I)
    response = reg.match(turl)
    return response.groupdict() ["handle"]

def run_follower(**kw):
    dmanager, config_reader, constants = init(**kw)
    thandle = get_thandle(kw["thandle"]).lower()
    if config_reader.debug: sys.stdout.write("Twitter Handle: " + thandle + "\n")
    if config_reader.out and config_reader.out.split(".")[1].lower() not in ["csv", "json"]:
        sys.stderr.write("Unsupported file format \n")
        return
    fcount = FollowerCount(thandle, config_reader, constants, dmanager)
    fcount.get_follower_count()
    if config_reader.debug: sys.stdout.write("follower count successfully completed for : " + kw["thandle"] + "\n")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Follower Count History (fch)", prog="fch")
    parser.add_argument("thandle", help="Enter a Twitter handle/ URL")
    parser.add_argument("--st", type=int, metavar="", default=-1, help="Memento start datetime (in RFC 1123 datetime format)")
    parser.add_argument("--et", type=int, metavar="", default=-1, help="Memento end datetime (in RFC 1123 datetime format)")
    parser.add_argument("--freq", type=int, metavar="", default=0, help="Sampling frequency of mementos (in seconds)")
    parser.add_argument("-f", metavar="", help="Output file path (Supported Extensions: JSON and CSV)")
    parser.set_defaults(func=run_follower)
    args = parser.parse_args()
    try:
        args.func(**vars(args))
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        parser.print_help()
