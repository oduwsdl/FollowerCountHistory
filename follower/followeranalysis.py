import ast
import csv
import os
from datetime import datetime
from core.utils.util_functions import Utils


class FollowerAnalysis:
    def __init__(self, thandle, conf_reader, constants, dmanager, logger):
        self.__thandle = thandle.lower()
        self.__constants = constants
        self.__logger = logger
        self.__dmanager = dmanager
        self.__conf_reader = conf_reader
    '''
    Analyze TimeMap for distribution of archives
    '''
    def timemap_analysis(self):
        turl = self.__constants.TWITTER_URL + self.__thandle
        tcontent = self.__dmanager.read_timemap(turl)
        larchive_2018 = []
        larchive_2019 = []
        lacount = [[], []]
        for entry in tcontent.split("\n"):
            entry = entry.rstrip()
            if entry:
                if not entry.startswith("@"):
                    entry = entry.split(" ", 1)
                    if 20180101000000 <= int(entry[0]) <= self.__conf_reader.start_time:
                        entry = ast.literal_eval(entry[1])
                        archive, mtimestamp, thandle, url_lang, with_replies = \
                            self.__dmanager.get_murl_info(entry["uri"])
                        if mtimestamp:
                            if archive not in larchive_2018:
                                larchive_2018.append(archive)
                                lacount[0].append(1)
                            else:
                                index = larchive_2018.index(archive)
                                lacount[0][index] += 1
                    elif self.__conf_reader.start_time <= int(entry[0]) <= self.__conf_reader.end_time:
                        entry = ast.literal_eval(entry[1])
                        archive, mtimestamp, thandle, url_lang, with_replies = \
                            self.__dmanager.get_murl_info(entry["uri"])
                        if mtimestamp:
                            if archive not in larchive_2019:
                                larchive_2019.append(archive)
                                lacount[1].append(1)
                            else:
                                index = larchive_2019.index(archive)
                                lacount[1][index] += 1

        with open("/data/Nauman/MementoDump/FollowerCount/" + self.__thandle + "_analysis.csv", "w") as csv_file:
            larchives = list(set(larchive_2018) | set(larchive_2019))
            irow = {}
            writer = csv.DictWriter(csv_file, fieldnames=larchives)
            writer.writeheader()
            for archive in larchives:
                if archive in larchive_2018:
                    index = larchive_2018.index(archive)
                    irow[archive] = lacount[0][index]
                else:
                    irow[archive] = 0
            writer.writerow(irow)
            for archive in larchives:
                if archive in larchive_2019:
                    index = larchive_2018.index(archive)
                    irow[archive] = lacount[1][index]
                else:
                    irow[archive] = 0
            writer.writerow(irow)
            csv_file.close()

    '''
    Function to create daily and original sampled mementos for Follower Count  analysis
    '''

    def relative_analysis(self):
        lrows = []
        lrows_daily = []

        mtimestamp = []
        daily_time = 0
        info_row = self.__thandle + "\n"
        ofile = open(os.path.join(self.__conf_reader.out_dir, "FollowerCount", "Info.txt"), "a+")
        with open(os.path.join(self.__conf_reader.out_dir, "FollowerCount", self.__thandle + ".csv"), "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for entry in reader:
                if entry["MementoTimestamp"] not in mtimestamp:
                    mtimestamp.append(entry["MementoTimestamp"])
                    lrows.append(entry)

        lrows = sorted(lrows, key=lambda i: i['MementoTimestamp'])

        for entry in lrows:
            if not daily_time:
                lrows_daily.append(entry)
                daily_time = Utils.memento_to_epochtime(entry["MementoTimestamp"])
            else:
                mtime = Utils.memento_to_epochtime(entry["MementoTimestamp"])
                if mtime > (daily_time + (24 * 3600)):
                    lrows_daily.append(entry)
                    daily_time = mtime
        lrows_daily = sorted(lrows_daily, key=lambda i: i['MementoTimestamp'])

        fieldnames = ["MementoTimestamp", "URI-M", "FollowerCount", "DateTime", "AbsRelative", "AbsPrevRelative",
                      "PerRelative", "PerPrevRelative", "RateRelative", "RatePrevRelative"]
        with open(os.path.join(self.__conf_reader.out_dir, "FollowerCount", self.__thandle + "_analysis.csv"), "w") as \
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
                if i == 1:
                    info_row += "ST: " + str(lrows[i]["DateTime"]) + " ,SCount: " + str(lrows[i]["FollowerCount"]) + \
                                "\n"
                elif i == (len(lrows) - 1):
                    info_row += "ET: " + str(lrows[i]["DateTime"]) + " ,ECount: " + str(lrows[i]["FollowerCount"]) + \
                                "\n"
                    info_row += "Increase: " + str(rabs) + " , %Increase: " + \
                                str(round((rabs / int(lrows[0]["FollowerCount"])) * 100, 2)) + "\n"
            ofile.write(info_row)
            ofile.close()
        with open(os.path.join(self.__conf_reader.out_dir, "FollowerCount", self.__thandle + "_daily.csv"), "w") as \
                csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            row = {"MementoTimestamp": lrows[0]["MementoTimestamp"], "URI-M": lrows[0]["URI-M"],
                   "FollowerCount": lrows[0]["FollowerCount"], "DateTime": lrows[0]["DateTime"],
                   "AbsRelative": 0, "AbsPrevRelative": 0, "PerRelative": 0, "PerPrevRelative": 0,
                   "RateRelative": 0, "RatePrevRelative": 0}
            writer.writerow(row)

            for i in range(1, len(lrows_daily)):
                tpdiff = int(datetime.strptime(lrows_daily[i]["DateTime"], "%Y-%m-%d %H:%M:%S").timestamp() -
                             datetime.strptime(lrows_daily[i - 1]["DateTime"], "%Y-%m-%d %H:%M:%S").timestamp())
                tdiff = int(datetime.strptime(lrows_daily[i]["DateTime"], "%Y-%m-%d %H:%M:%S").timestamp() -
                            datetime.strptime(lrows_daily[0]["DateTime"], "%Y-%m-%d %H:%M:%S").timestamp())

                rabs = int(lrows_daily[i]["FollowerCount"]) - int(lrows_daily[0]["FollowerCount"])
                rpabs = int(lrows_daily[i]["FollowerCount"]) - int(lrows_daily[i - 1]["FollowerCount"])
                row = {"MementoTimestamp": lrows_daily[i]["MementoTimestamp"], "URI-M": lrows_daily[i]["URI-M"],
                       "FollowerCount": lrows_daily[i]["FollowerCount"], "DateTime": lrows_daily[i]["DateTime"],
                       "AbsRelative": rabs, "AbsPrevRelative": rpabs,
                       "PerRelative": round((rabs / int(lrows_daily[0]["FollowerCount"])) * 100, 2),
                       "PerPrevRelative": round((rpabs / int(lrows_daily[i - 1]["FollowerCount"])) * 100, 2),
                       "RateRelative": round(rabs / tdiff, 5), "RatePrevRelative": round(rpabs / tpdiff, 5)}
                writer.writerow(row)

