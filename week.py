import datetime
from deg1_2 import list_1_2_deg
#print datetime.date(2016, 12, 31).isocalendar()[1]

#a data indicate every week situation in an area
week_in_2015 = []
"""week_in_2015 = [[area_name], [[week1, level], [week2, level], [week3, level]...]"""
for i in range(len(list_1_2_deg)):
	container = [[], []]
	container[1] = [[0, 0]] * 53	#2015 has 53 weeks
	container[0].append(list_1_2_deg[i][0][0])
	week_in_2015.append(container)
	
import csv
import re
file = open('Kaohsiung(2015).csv', 'r')
lines = file.readlines()
for i in range(len(lines)):	#use regular expression to remove" \n "
	lines[i] = re.sub('[\n]','',lines[i])
print "there are %d case" %(len(lines) - 1)

for i in range(1, len(lines)):
	segment = lines[i].split(",")

	month = 0
	day = 0
	week = 0

	month = segment[2].split("/")[1]
	day = segment[2].split("/")[2]
	week = datetime.date(2015, int(month), int(day)).isocalendar()[1]
	
	print month, day, segment[8], week
