lastday = ''
with open("michelleobama.csv", "rt") as f:
	with open("michelleobama-last.csv", "wt") as w:
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