"""
create action log and real case data 2014,2015
When learning, it should not be imported to table.py, which use Cell class as table structure
"""
import datetime
import sys


from deg1_2 import list_1_2_deg

"""store real situation"""

#a data indicate every week situation in an area
week_in_2014 = {}
week_in_2015 = {}
print "there are %d areas" % len(list_1_2_deg)
# week_in_2014 = area_name: [[week1, level], [week2, level], [week3, level]..., active?]

for k in list_1_2_deg:
	week_in_2014[k] = [[0, 0] for x in range(53)]		#isocalendar may has 53 weeks in a year
	week_in_2014[k].append(-1)							#default not active yet
	
	week_in_2015[k] = [[0, 0] for x in range(53)]		#isocalendar may has 53 weeks in a year
	week_in_2015[k].append(-1)							#default not active yet


#real data for 2014
import csv
import re

print "2014 cases:"
file = open('Kaohsiung2014_case.csv', 'r')
lines = file.readlines()
for i in range(len(lines)):	#use regular expression to remove" \n "
	lines[i] = re.sub('[\n]','',lines[i])
print "there are %d case" %(len(lines) - 1)
count = 0

no_match = 0
valid_case = 0

trace = 0

for i in range(1, len(lines)):
	segment = lines[i].split(",")

	year = 0
	month = 0
	day = 0
	week = 0
	tuple = ()

	year = segment[2].split("/")[0]
	month = segment[2].split("/")[1]
	day = segment[2].split("/")[2]
	tuple = datetime.date(int(year), int(month), int(day)).isocalendar()
	week = tuple[1]
	

	
	if(segment[8] != "" ):
		
		if(segment[8] in week_in_2014 ):	
				
			valid_case += 1	

			if tuple[0] == 2014:
				week_in_2014[segment[8]][week - 1][0] += 1
			else:		
				#although it is 2014, but it seem as 2015
				week_in_2015[segment[8]][week - 1][0] += 1
			
print  "there are %d valid cases" %valid_case
file.close()
print

#real data for 2015
print "2015 cases:"
file = open('Kaohsiung2015_case.csv', 'r')
lines = file.readlines()
for i in range(len(lines)):	#use regular expression to remove" \n "
	lines[i] = re.sub('[\n]','',lines[i])
print "there are %d case" %(len(lines) - 1)
count = 0

no_match = 0
valid_case = 0

trace = 0

for i in range(1, len(lines)):
	segment = lines[i].split(",")

	year = 0
	month = 0
	day = 0
	week = 0
	tuple = ()

	year = segment[2].split("/")[0]
	month = segment[2].split("/")[1]
	day = segment[2].split("/")[2]
	tuple = datetime.date(int(year), int(month), int(day)).isocalendar()
	week = tuple[1]
	

	
	if(segment[8] != "" ):
		
		if(segment[8] in week_in_2015 ):	
				
			valid_case += 1	

			if tuple[0] == 2015:
				week_in_2015[segment[8]][week - 1][0] += 1
			
print  "there are %d valid cases" %valid_case
file.close()




"""build a case table, using 2014 to learn, and 2015 is just to be observed"""
# case table 2014
total = 0
header = [""]
for i in range(1, 54):
	header.append(str(i))

file = open("2014case.csv","w")
w = csv.writer(file)
w.writerows([header])
for k in week_in_2014:
	data = []
	data.append(k)
	for j in range(53):
		data.append(str(week_in_2014[k][j][0]))
		total += week_in_2014[k][j][0]
	w.writerows([data])
file.close()
print "total count from csv is %d" %total
# case table 2015
total = 0
header = [""]
for i in range(1, 54):
	header.append(str(i))

file = open("2015case.csv","w")
w = csv.writer(file)
w.writerows([header])
for k in week_in_2015:
	data = []
	data.append(k)
	for j in range(53):
		data.append(str(week_in_2015[k][j][0]))
		total += week_in_2015[k][j][0]
	w.writerows([data])
file.close()
print "total count from csv is %d" %total


"""learning and fill the list_1_2_deg(Au, Av2u), noting that not to imported to table.py"""


print "start learning by 2014"
now_action = 0
action = 0
print week_in_2014['A6412-1446-00']
for k in week_in_2014:
	for w in range(52):
		if w <= 50: 	# check 2 week after
			if week_in_2014[k][w][0] > 0:	
				list_1_2_deg[k].Av += 1
				# check itself
				if week_in_2014[k][w + 1][0] > 0 or week_in_2014[k][w + 2][0] > 0:
					list_1_2_deg[k].toself.Av2u += 1

				# check its neighbor
				for n1 in list_1_2_deg[k].deg1:
					if week_in_2014[n1][w + 1][0] > 0 or week_in_2014[n1][w + 2][0] > 0:
						list_1_2_deg[k].deg1[n1].Av2u += 1
		else: 			# only check 53th week
			if week_in_2014[k][w][0] > 0:	
				list_1_2_deg[k].Av += 1
				# check itself
				if week_in_2014[k][w + 1][0] > 0:
					list_1_2_deg[k].toself.Av2u += 1

				# check its neighbor
				for n1 in list_1_2_deg[k].deg1:
					if week_in_2014[n1][w + 1][0] > 0:
						list_1_2_deg[k].deg1[n1].Av2u += 1
# test
list_1_2_deg['A6409-0129-00'].show()

"""calculate probability by Av2u/Au"""
# to other
for k in list_1_2_deg:
	for p in list_1_2_deg[k].deg1:
		if list_1_2_deg[k].Av != 0:		#avoid dividing zero
			list_1_2_deg[k].deg1[p].pv_u_0 = list_1_2_deg[k].deg1[p].Av2u / float(list_1_2_deg[k].Av)
# to itself
for k in list_1_2_deg:
	if list_1_2_deg[k].Av != 0:
		list_1_2_deg[k].toself.pv_u_0 = list_1_2_deg[k].toself.Av2u / float(list_1_2_deg[k].Av)
