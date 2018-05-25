#Truss Software Engineering Interview Project Solution
#Kaylee Moss
#Converts the provided CSV file into a normalized CSV file format

import csv, sys, datetime

inf = input("Enter input file name: ")
ouf = input("Enter output file name: ")
fin = open(inf, 'r', encoding='utf-8', errors='replace') #Opens the csv file from the first command line arguement, replaces all non-utf-8 characters with the unicode replacement character
reader = csv.reader(fin)
fout = open(ouf, 'w', encoding='utf-8', errors='replace') #Creates the new csv file from the second command line arguement
writer = csv.writer(fout)
for index,row in enumerate(reader):
	if index == 0:
		writer.writerow(row) #Writes the header as is
	else:
		#Timestamp
		try:
			PM = row[0][-2] #Checks if the time is PM or AM
			row[0] = row[0][:-3] #Removes the PM or AM from the time
			date = datetime.datetime.strptime(row[0], '%m/%d/%y %H:%M:%S') #Converts the time to a date variable
			if(PM=='P'):
				date = date + datetime.timedelta(hours=12) #Fixes for PM times
			date = date + datetime.timedelta(hours=3) #Converts from PST to EST		
			row[0] = date.isoformat() #Updates the row with the correct format
		except ValueError:
			print ("Warning: Invalid datetime. Row dropped") #Drops the row for a invalid value
			continue
		
		#ZIP - note to self, the CSV editor you're using makes it look like this doesn't work. It does
		try:
			row[2] = row[2].zfill(5) #Adds zeroes to the front of the number until it is five digits
		except ValueError:
			print ("Warning: Invalid ZIP. Row dropped") #Drops the row for a invalid value
			continue

		#FullName
		row[3] = row[3].upper() #Converts the column to uppercase

		#FooDuration and BarDuration
		footimearray = row[4].split(":")
		footime = int(footimearray[0])*60*60+int(footimearray[1])*60
		row[4] = float(footime) + float(footimearray[2]) #Converts FooDuration to floating point seconds
		bartimearray = row[5].split(":")
		bartime = int(bartimearray[0])*60*60+int(bartimearray[1])*60
		row[5] = float(bartime) + float(bartimearray[2]) #Converts BarDuration to floating point seconds
		
		#TotalDuration
		row[6]=row[4]+row[5]

		writer.writerow(row) #Writes the final row out
