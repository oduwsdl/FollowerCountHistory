import csv
import json
import sys
import os

mementoData = "var mementoData = [];\n"
def parse_csv(csvFilePath):

    data = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        
        index = 0
        for rows in csvReader:
            #print(rows)
            data.append(rows)
            index+=1

    jsonData = json.dumps(data)
    #l = list(data)
    #print(jsonData)
    return jsonData
            


def add_to_mementodata(data, iden, path):

    global mementoData
    handle = os.path.basename(path)[0:-4];
    entry = "mementoData.push({ id : " + str(iden) + ", active : true, handle : '" + handle +  "', data : " + data + "});\n"
    mementoData = mementoData + entry

def write_to_js():
    f = open("generatedGraphStub.html", "w")
    s = open("generateGraph_base.js", "r")
    i = open("index.html", "r")

    for line in i:
        f.write(line)

    f.write("\n")
    f.write(mementoData)
    f.write("\n")

    for line in s:
        f.write(line)
    
    s.close()
    f.close()
    i.close()

def main():
    args = sys.argv[1:]
    for i in range(0, len(args)):
        data = parse_csv(args[i])
        add_to_mementodata(data, i, args[i])

    print(mementoData)
    write_to_js()

    

if __name__ == "__main__":
    main()

