import ast
import csv
import os
import sys
import json
from datetime import datetime
from fch.core.utils.util_functions import Utils


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
      try:
        lfollower = sorted(lfollower, key=lambda i: i['MementoDatetime'])
        if self.__conf_reader.debug: sys.stdout.write(str(lfollower) + "\n")
        for i in range (0, len(lfollower)):
          if self.__conf_reader.debug: sys.stdout.write(str(lfollower[i]) + "\n")
          if i == 0:
            lfollower[i]["AbsGrowth"] = 0
            lfollower[i]["RelGrowth"] = 0
            lfollower[i]["AbsPerGrowth"] = 0
            lfollower[i]["RelPerGrowth"] = 0
            lfollower[i]["AbsFolRate"] = 0
            lfollower[i]["RelFolRate"] = 0
          else:
            tpdiff = int(datetime.strptime(lfollower[i]["MementoDatetime"], "%Y%m%d%H%M%S").timestamp() -
                         datetime.strptime(lfollower[i - 1]["MementoDatetime"], "%Y%m%d%H%M%S").timestamp())
            tdiff = int(datetime.strptime(lfollower[i]["MementoDatetime"], "%Y%m%d%H%M%S").timestamp() -
                        datetime.strptime(lfollower[0]["MementoDatetime"], "%Y%m%d%H%M%S").timestamp())
            if tpdiff == 0:
              tpdiff = 1
            if tdiff == 0:
              tdiff = 1
            abs_growth = int(lfollower[i]["FollowerCount"]) - int(lfollower[0]["FollowerCount"])
            rel_gowth = int(lfollower[i]["FollowerCount"]) - int(lfollower[i - 1]["FollowerCount"])
            lfollower[i]["AbsGrowth"] = abs_growth
            lfollower[i]["RelGrowth"] = rel_gowth
            lfollower[i]["AbsPerGrowth"] = round((abs_growth / int(lfollower[0]["FollowerCount"])) * 100, 2)
            lfollower[i]["RelPerGrowth"] = round((rel_gowth / int(lfollower[i -1]["FollowerCount"])) * 100, 2)
            lfollower[i]["AbsFolRate"] = round(abs_growth / tdiff, 5)
            lfollower[i]["RelFolRate"] = round(rel_gowth / tpdiff, 5)
        if self.__conf_reader.debug: sys.stdout.write("Analysis done on follower JSON goig for writing" + "\n")
        if self.__conf_reader.out:
          ext = self.__conf_reader.out.split(".")[1].lower()
        else:
          ext = None
        if not self.__conf_reader.out or ext == "csv":
          fieldnames = ["MementoDatetime", "URIM", "FollowerCount", "AbsGrowth", "RelGrowth",
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
      except Exception as e:
        sys.stderr.write("FollowerAnalysis: " + str(e) + "\n")
