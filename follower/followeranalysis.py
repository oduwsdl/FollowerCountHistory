import ast
import csv
import os
import sys
import json
from datetime import datetime
from core.utils.util_functions import Utils


class FollowerAnalysis:
    def __init__(self, thandle, conf_reader, constants, dmanager):
        self.__thandle = thandle.lower()
        self.__constants = constants
        self.__dmanager = dmanager
        self.__conf_reader = conf_reader

    '''
    Function to create daily and original sampled mementos for Follower Count  analysis
    '''

    def relative_analysis(self):
        lrows = []
        mtimestamp = []
        if not self.__conf_reader.out:
            return

        fpath = os.path.join(os.getcwd(), "output", "followerCSV")
        with open(os.path.join(fpath, self.__thandle + ".csv"), "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for entry in reader:
                lrows.append(entry)

        lrows = sorted(lrows, key=lambda i: i['MementoTimestamp'])
        if self.__conf_reader.debug: sys.stdout.write("Relative Analysis: CSV File Read" + "\n")
        fieldnames = ["MementoTimestamp", "URI-M", "FollowerCount", "DateTime", "AbsRelative", "AbsPrevRelative",
                      "PerRelative", "PerPrevRelative", "RateRelative", "RatePrevRelative"]

        if self.__conf_reader.out:
            fpath = os.path.join(os.getcwd(), "output", "followerCSV")
        with open(os.path.join(fpath, self.__thandle + "_analysis.csv"), "w") as \
                csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            row = {"MementoTimestamp": lrows[0]["MementoTimestamp"], "URI-M": lrows[0]["URI-M"],
                   "FollowerCount": lrows[0]["FollowerCount"], "DateTime": lrows[0]["DateTime"],
                   "AbsRelative": 0, "AbsPrevRelative": 0, "PerRelative": 0, "PerPrevRelative": 0,
                   "RateRelative": 0, "RatePrevRelative": 0}
            writer.writerow(row)
            for i in range(1, len(lrows)):
                tpdiff = int(datetime.strptime(lrows[i]["DateTime"], "%Y-%m-%d %H:%M:%S").timestamp() -
                             datetime.strptime(lrows[i - 1]["DateTime"], "%Y-%m-%d %H:%M:%S").timestamp())
                tdiff = int(datetime.strptime(lrows[i]["DateTime"], "%Y-%m-%d %H:%M:%S").timestamp() -
                            datetime.strptime(lrows[0]["DateTime"], "%Y-%m-%d %H:%M:%S").timestamp())
                rabs = int(lrows[i]["FollowerCount"]) - int(lrows[0]["FollowerCount"])
                rpabs = int(lrows[i]["FollowerCount"]) - int(lrows[i - 1]["FollowerCount"])
                row = {"MementoTimestamp": lrows[i]["MementoTimestamp"], "URI-M": lrows[i]["URI-M"],
                       "FollowerCount": lrows[i]["FollowerCount"], "DateTime": lrows[i]["DateTime"],
                       "AbsRelative": rabs, "AbsPrevRelative": rpabs,
                       "PerRelative": round((rabs / int(lrows[0]["FollowerCount"])) * 100, 2),
                       "PerPrevRelative": round((rpabs / int(lrows[i - 1]["FollowerCount"])) * 100, 2),
                       "RateRelative": round(rabs / tdiff, 5), "RatePrevRelative": round(rpabs / tpdiff, 5)}
                writer.writerow(row)
