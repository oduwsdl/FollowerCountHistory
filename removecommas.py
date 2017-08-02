lastline = ''
with open("original.csv", "rt") as f:
	with open("original-nocommas.csv", "wt") as w:
		for line in f:
			if line != lastline:
				lastline = line
				parts = line.split(',',1)
				date = parts[0]
				print("date is " + date)
				number = parts[1]
				number = number.replace(',','')
				newline = str(date) + ',' + str(number)
				print(newline)
				w.write(newline)



