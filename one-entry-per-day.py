from sys import argv
uname = argv[1]
lastday = ''
with open('./' + uname + '/' + uname + ".csv", "rt") as f:
	with open('./' + uname + '/' + uname + "-last.csv", "wt") as w:
		next(f) #skip first line 
		w.write('date,count\n')
		for line in f:
			parts = line.split(',',1)
			date = parts[0]
			day = date[:6]
			day = '-'.join([day[:4], day[4:6]])
			day = day + '-01'
			print(day)
			if lastday != day:
				lastday = day
				#print("date is " + date)
				number = parts[1]
				number = number.replace(',','')
				newline = str(day) + ',' + str(number)
				#print(newline)
				w.write(newline)