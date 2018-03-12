#!/usr/bin/env	python3

from bs4 import BeautifulSoup
from sys import argv
import urllib.request as urllib, requests, re, subprocess
import os, errno
import argparse
import unicodedata2 as unicodedata

def main():
	parser = argparse.ArgumentParser(description='Follower Count History. Given a Twitter username, collect follower counts from the Internet Archive.')

	parser.add_argument('-g', dest='graph', action='store_true', help='Generate a graph with data points')
	parser.add_argument('-e', dest='allMemento', action='store_false', help='Collect every memento, not just one per month')
	parser.add_argument('uname', help='Twitter username without @')
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-p', dest='push', action='store_true', help='Push to Internet Archive')
	group.add_argument('-P', dest='pushAll', action='store_true', help='Push to all Archives available through ArchiveNow')

	args = parser.parse_args()

	#Dependencies Optional
	if args.push or args.pushAll:
		from archivenow import archivenow
		import datetime

	def slugify(value):
		"""
		Convert to ASCII. Convert spaces to hyphens.
		Remove characters that aren't alphanumerics, underscores, or hyphens.
		Convert to lowercase. Also strip leading and trailing whitespace.
		"""
		value = str(value)
		value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
		value = str(re.sub('[^\w\s-]', '', value).strip().lower())
		value = str(re.sub('[-\s]+', '-', value))
		return value



	archivelink = 'http://web.archive.org/web/timemap/link/http://twitter.com/' + args.uname
	print(args.uname)
	print(archivelink)
	r = requests.get(archivelink)
	linkslist = []
	safeuname= slugify(args.uname)
	try:
	    os.makedirs('./' + safeuname)
	except OSError as e:
	    if e.errno != errno.EEXIST:
	        raise


	writefile = './' + safeuname + '/' + safeuname + ".csv"
	errorfile = './' + safeuname + '/' + safeuname + "-Error.csv"
	w = open (writefile, "a+")
	e = open (errorfile, "a+")
	olddates =[]
	if (os.stat(writefile).st_size==0):
		#ensure header line does not get re written
		w.write('date,count,URL-M'+'\n')
	else:
		w.seek(0)
		#read in old data points
		for line in w.readlines():
			row = line.split(",")
			if(row[0] != "date"):
				olddates.append( row[0].replace("-",""))
		#reset to the end
	lastline = ''
	for line in r.iter_lines(): #on each line if rel="memento" doesn't exist, ignore. If it does get the link and add it to the list of links
		#print(line)
		if ('rel="memento"'.encode('utf-8') in line or 'rel="first memento"'.encode('utf-8') in line):
			if (line != lastline):
				lastline = line
				linkslist.append(line[1:line.find('>;'.encode('utf-8'))])
	print(str(len(linkslist)) + " archive points found")

	lastdate = ''
	date = '0'
	#with open("test.txt", "r") as f:
	for line in linkslist:
		line = line.decode('utf-8')
		dateloc = line.find("/web/")
		date = line[dateloc+5:dateloc+19] #get the timestamp from the link

		if(args.allMemento):
			#get one entry per month
			if (date[:6] == lastdate): #if new month is the same as previous, skip
				e.write(date+",duplicate month,"+ line + "\n")
				continue

		if (date[:8] in olddates): #if date is in old data-> skip
			continue

		if(not args.allMemento): #If not all mementos AND if month is in old data-> skip
			for x in olddates:
				if x[:6] == date[:6]:
					e.write(date+",duplicate month,"+ line + "\n")
					continue

		print(date)
		try:
			res = urllib.urlopen(line)
		except:
			e.write(day+",URI-M not loaded,"+ line + "\n")
			continue

		html = res.read()
		soup = BeautifulSoup(html, "lxml") #html.parser -> lxml
		#get rid of scripts(javascript especially)
		for elem in soup.findAll(['script', 'style']):
			elem.extract()

		#Make sure this isn't a redirected Momento
		realURL = res.geturl()
		realdateloc = realURL.find("/web/")
		realdate = realURL[dateloc+5:dateloc+19] #get the timestamp from the link
		day = '-'.join([date[:4], date[4:6], date[6:8]])
		if(date != realdate):
			e.write(day+",redirect,"+ line + "\n")
			continue


		if int(date) < 10120700000000:
			e.write(day+",before 10120700000000,"+ line + "\n")
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
											try:
												result = soup.select("follower_stats")
												if not result:
													raise ValueError('Empty')
											except:
												e.write(day+",followers not found,"+ line + "\n")
												continue

		result = re.sub(r'\D', '', str(result)) #remove everything that's not a number
		if (result == ''):
			e.write(day+",followers not numbers,"+ line + "\n")
			continue
		try:
			result = str(int(result)) #Make sure a number. Also translates other languages if possible.
			print(result)

			w.write(day + ',' + result + ',' + realURL + '\n')
			lastdate = date[:6]
		except:
			e.write(day+",followers not arabic numerals,"+ line + "\n")
			continue
	w.close()

	if args.push or args.pushAll:
		#Send to archive
		now = datetime.datetime.now().strftime("%Y%m")

		if( int(date[:6]) < int(now)):
			if args.pushAll:
				print("Pushing to Archives")
				archivenow.push("http://twitter.com/" + args.uname,"all")
			else:
				print("Pushing to Internet Archive")
				archivenow.push("http://twitter.com/" + args.uname,"ia")
		else:
			print("Not Pushing to Archive. Last Memento Within Current Month.")
	if (args.graph):
		#Call the Rscript to create a linechart with the numbers collected
		Rcall = "Rscript --vanilla follower_count_linechart.R " + safeuname
		subprocess.call(Rcall, shell=True)

if __name__ == "__main__":
	main()
