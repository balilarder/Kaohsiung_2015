# Use day to tag intagious areas:
# (write csv with 365(366) days)
import csv
import re

def ReadCaseByDay(city, graph, base2first_table, base2secondary_table):

	print(len(graph))
	days_count2014 = {}			# accumulate cases
	days_tag2014 = {}			# if the day is in risk?
	days_count2015 = {}			# accumulate cases
	days_tag2015 = {}			# if the day is in risk?

	for k in graph:
		days_count2014[k] = [0 for x in range(366)]
		days_tag2014[k] = [0 for x in range(366)]
		days_count2015[k] = [0 for x in range(366)]
		days_tag2015[k] = [0 for x in range(366)]

	print(len(days_count2014), len(days_tag2014))


	if city == "K":
		f2014 = '../inputfiles/Kaohsiung2014_case.csv'
		f2015 = '../inputfiles/Kaohsiung2015_case.csv'
	elif city == "T":
		f2014 = '../inputfiles/Tainan2014_case.csv'
		f2015 = '../inputfiles/Tainan2015_case.csv'

	print f2014, f2015

	# 2014
	file = open(f2014, 'r')
	lines = file.readlines()
	for i in range(len(lines)): #use regular expression to remove" \n "
		lines[i] = re.sub('[\n]','',lines[i])
	print "there are %d case" %(len(lines) - 1)
	

	for i in range(1, len(lines)):
		segment = lines[i].split(",")
		if(segment[8] != "" and segment[8] in base2secondary_table):
			to2nd = base2secondary_table[segment[8]]
			# compute day
			d = convert2WhichDay(segment[2])
			# count
			days_count2014[to2nd][d-1] += 1

	# 2015
	file = open(f2015, 'r')
	lines = file.readlines()
	for i in range(len(lines)): #use regular expression to remove" \n "
		lines[i] = re.sub('[\n]','',lines[i])
	print "there are %d case" %(len(lines) - 1)
	

	for i in range(1, len(lines)):
		segment = lines[i].split(",")
		if(segment[8] != "" and segment[8] in base2secondary_table):
			to2nd = base2secondary_table[segment[8]]
			# compute day
			d = convert2WhichDay(segment[2])
			# count
			days_count2015[to2nd][d-1] += 1
	
	# coloring
	coloring_tag(days_count2014, days_tag2014)
	coloring_tag(days_count2015, days_count2015)

	return days_tag2014, days_tag2015

def Day2Csv(data):
	pass


def convert2WhichDay(datestring):
	year = int(datestring[:4])
	month = int(datestring[5:7])
	day = int(datestring[8:])

	leap_year = 0
	valid = 1
	# leap year
	if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
		leap_year = 1

	
	# compute day number
	if valid:
		count = 0
		i = 1
		while i < month:
			if i == 1 or i == 3 or i == 5 or i == 7 \
				or i == 8 or i == 10 or i == 12:
					count += 31
			if i == 4 or i == 6 or i == 9 or i == 11:
				count += 30
			if i == 2 and leap_year:
				count += 29
			if i == 2 and not(leap_year):
				count += 28
			i += 1

		count += day
		
	return count


# change tag from 0 to 1		
def coloring_tag(days_count, days_tag):
	alert_thershold = 6 	# or 7(for 2nd stastic areas)

	startbound = 366 - 6
	print startbound
	for k in days_count:	
		for i in range(startbound):
			# given s(tart), t(erminate) day to check a unit 7 days on the risk
			check = 0
			s = i
			t = i + 7
			for day in range(s, t):
				check += days_count[k][day]
			if check >= alert_thershold:
				# tag 7 days at once
				for day in range(s, t):
					days_tag[k][day] = 1 

	print "coloring"