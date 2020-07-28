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

    def relative_analysis(self, lfollower):
        lfollower = sorted(lfollower, key=lambda i: i['MementoTimestamp'])
        for i in range (0, len(lfollower)):
          if i == 0:
            lfollower[i]["AbsGrowth"] = 0
            lfollower[i]["RelGrowth"] = 0
            lfollower[i]["AbsPerGrowth"] = 0
            lfollower[i]["RelPerGrowth"] = 0
            lfollower[i]["AbsFolRate"] = 0
            lfollower[i]["RelFolRate"] = 0
          else:
            tpdiff = int(datetime.strptime(lfollower[i]["MementoTimestamp"], "%Y%m%d%H%M%S").timestamp() -
                         datetime.strptime(lfollower[i - 1]["MementoTimestamp"], "%Y%m%d%H%M%S").timestamp())
            tdiff = int(datetime.strptime(lfollower[i]["MementoTimestamp"], "%Y%m%d%H%M%S").timestamp() -
                        datetime.strptime(lfollower[0]["MementoTimestamp"], "%Y%m%d%H%M%S").timestamp())
            abs_growth = int(lfollower[i]["FollowerCount"]) - int(lfollower[0]["FollowerCount"])
            rel_gowth = int(lfollower[i]["FollowerCount"]) - int(lfollower[i - 1]["FollowerCount"])
            lfollower[i]["AbsGrowth"] = abs_growth
            lfollower[i]["RelGrowth"] = rel_gowth
            lfollower[i]["AbsPerGrowth"] = round((abs_growth / int(lfollower[0]["FollowerCount"])) * 100, 2)
            lfollower[i]["RelPerGrowth"] = round((rel_gowth / int(lfollower[i -1]["FollowerCount"])) * 100, 2)
            lfollower[i]["AbsFolRate"] = round(abs_growth / tdiff, 5)
            lfollower[i]["RelFolRate"] = round(rel_gowth / tpdiff, 5)
        if self.__conf_reader.out:
          ext = self.__conf_reader.out.split(".")[1].lower()
        else:
          ext = None
        if not self.__conf_reader.out or ext == "csv":
          fieldnames = ["MementoTimestamp", "URI-M", "FollowerCount", "AbsGrowth", "RelGrowth",
              "AbsPerGrowth", "RelPerGrowth", "AbsFolRate", "RelFolRate"]
          if not self.__conf_reader.out:
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
            fobj = None
          elif ext == "csv":
            fobj = open(self.__conf_reader.out, "w")
            writer = csv.DictWriter(fobj, fieldnames=fieldnames)
          writer.writeheader()
          writer.writerows(lfollower)
          if fobj:
            fobj.close()
        elif ext == "json":
          fobj = open(self.__conf_reader.out, "w") 
          json.dump(lfollower, fobj)
          fobj.close()
        else:
          sys.stderr.write("Unsupported file type \n")
        '''
        exit()
        if self.__conf_reader.debug: sys.stdout.write("Relative Analysis: parsed json received" + "\n")



        if self.__conf_reader.out and ext in ("csv", "json"):
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
'''