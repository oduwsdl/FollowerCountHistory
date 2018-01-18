#!/usr/bin/env	python

from bs4 import BeautifulSoup
from sys import argv
import urllib.request as urllib, requests, re, subprocess
import os, errno

uname = argv[1] #get twitter username from first argument
if len(argv) > 2:
    wantR = argv[2] #Should a graph be created from the R script [0|1]
else:
    wantR = 1 #defaults to true
archivelink = 'http://web.archive.org/web/timemap/link/http://twitter.com/' + uname
print(uname)
print(archivelink)
r = requests.get(archivelink)
linkslist = []
try:
    os.makedirs('./' + uname)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
writefile = './' + uname + '/' + uname + ".csv"
w = open (writefile, "a+")
w.write('date,count'+'\n')
lastline = ''
for line in r.iter_lines(): #on each line if rel="memento" doesn't exist, ignore. If it does get the link and add it to the list of links
	#print(line)
	if ('rel="memento"'.encode('utf-8') in line):
		if (line != lastline):
			lastline = line
			linkslist.append(line[1:line.find('>;'.encode('utf-8'))])
print(str(len(linkslist)) + " archive points found") 

lastdate = ''
#with open("test.txt", "r") as f: 
for line in linkslist:
	line = line.decode('utf-8')
	dateloc = line.find("/web/")
	date = line[dateloc+5:dateloc+19] #get the timestamp from the link
	#get one entry per month
	if (date[:6] == lastdate): #if new month is the same as previous, skip
		continue			
	print(date)
	res = urllib.urlopen(line)
	html = res.read()
	soup = BeautifulSoup(html, "lxml") #html.parser -> lxml
	#get rid of scripts(javascript especially)
	for elem in soup.findAll(['script', 'style']):
		elem.extract()
	if int(date) < 10120700000000:
		continue
	else:
		#try excepts that find the follower counts for different versions of Twitter since its 2008
		try:
			result = soup.select(".ProfileNav-item--followers")[0]
			try:
				result = result.find("a")['title']
			except:
				result = result.find("a")['data-original-title']
		except:
			try:
				result = soup.select(".js-mini-profile-stat")[-1]['title']
			except:
				try:
					result = soup.select(".stats li")[-1].find("strong")['title']
				except:
					try:
						result = soup.select(".stats li")[-1].find("strong").text
					except:
						try:
							result = soup.select("#follower_count")[0].text
						except:
							try:
								result = soup.select("#followers_count")[0].text
							except:
								try:
									result = soup.select(".user-stats-followers")[0].text
									#result = result[:result.find("Followers")]
								except:
									try:
										result = soup.select(".stats_count")[1].text
									except:
										print("Couldn't figure it out")
										continue
	result = re.sub(r'\D', '', result) #remove everything that's not a number
	if (result == ''):
		continue
	try:
		print(result)
		day = '-'.join([date[:4], date[4:6], date[6:8]])
		w.write(day + ',' + result + '\n')
		lastdate = date[:6]
	except:
		print("Number not Arabic numeral")
		continue
w.close()

if (wantR == '1'):
	#Call the Rscript to create a linechart with the numbers collected
	Rcall = "Rscript --vanilla follower_count_linechart.R " + uname
	subprocess.call(Rcall, shell=True)
