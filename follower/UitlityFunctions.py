import os
import csv

'''
Function to categorize the candidates on the basis of follower growth in 4 categories
High Follower Growth, High % Increase: Beneticial
Low Follower Growth, High % Increase: Worthwhile
High Follower Growth, Low % Increase: Disheartening
Low Follower Growth, Low % Increase: Not worth it
'''


def label_candidates(follower_increase_threshold=100000, follower_percentage_threshold=100.0):
    lincrease = []
    lpincrease = []
    lhandle = []
    lcount = 1
    hcount = 1

    ifile = open("/home/msiddique/WSDL_Work/Rtest/DemCluster.csv", "w")
    fiednames = ["Handle", "Increase", "Perc"]
    writer = csv.DictWriter(ifile, fieldnames=fiednames)
    writer.writeheader()
    with open(os.path.join("/data/Nauman/MementoDump", "FollowerCount", "Info.txt"), "r") as ofile:
        for line in ofile:
            if line.startswith("Increase"):
                lincrease.append(int(line.rstrip().split(",")[0].split(":")[-1]))
                lpincrease.append(float(line.rstrip().split(",")[-1].split(":")[-1]))
            if lcount == hcount:
                lhandle.append(line.rstrip())
                lcount += 4
            hcount += 1
    lehandles = ["senwarren", "repswalwell", "sensanders", "reptimryan", "repbetoorourke", "senkamalaharris",
                 "gillibrandny", "tulsipress", "repjohndelaney", "senbooker", "senatorbennet"]
    for handle in lehandles:
        idx = lhandle.index(handle)
        lhandle.remove(handle)
        del lpincrease[idx]
        del lincrease[idx]
    zipped = list(zip(lincrease, lhandle, lpincrease))
    zipped.sort()
    lincrease, lhandle, lpincrease = zip(*zipped)
    # lincrease, lhandle = zip(*sorted(zip(lincrease, lhandle)))
    for i in range(0, len(lhandle)):
        print(lhandle[i] + ": " + str(lincrease[i]) + " : " + str(lpincrease[i]))
        writer.writerow({"Handle": lhandle[i], "Increase": lincrease[i], "Perc": lpincrease[i]})
    ifile.close()
    lcategory = [[], [], [], []]

    for i in range(0, len(lhandle)):
        if lincrease[i] >= follower_increase_threshold and lpincrease[i] >= follower_percentage_threshold:
            lcategory[0].append(lhandle[i])
        elif lincrease[i] < follower_increase_threshold and lpincrease[i] >= follower_percentage_threshold:
            lcategory[1].append(lhandle[i])
        elif lincrease[i] >= follower_increase_threshold and lpincrease[i] < follower_percentage_threshold:
            lcategory[2].append(lhandle[i])
        elif lincrease[i] < follower_increase_threshold and lpincrease[i] < follower_percentage_threshold:
            lcategory[3].append(lhandle[i])

    print("Big Increase + Big %   :" + str(lcategory[0]))
    print("Low Increase + Big %   :" + str(lcategory[1]))
    print("Big Increase + Low %   :" + str(lcategory[2]))
    print("Low Increase + Low %   :" + str(lcategory[3]))


label_candidates()
