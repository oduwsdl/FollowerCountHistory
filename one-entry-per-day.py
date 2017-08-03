lastday = ''
with open("megynkelly-nocommas.csv", "rt") as f:
	with open("megynkelly-oneperday.csv", "wt") as w:
		for line in f:
			parts = line.split(',',1)
			date = parts[0]
			day = date[:6]
			print(day)
			day = '-'.join([day[:4], day[4:6]])
			print(day)
			if lastday != day:
				lastday = day
				#print("date is " + date)
				number = parts[1]
				number = number.replace(',','')
				newline = str(day) + ',' + str(number)
				#print(newline)
				w.write(newline)