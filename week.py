import datetime

from deg1_2 import list_1_2_deg

""" Because structure has changed to dict, the function may become useless
def find_list_id(string):
	for i in range(len(list_1_2_deg)):
		if(list_1_2_deg[i][0][0] == string):
			return i 
	return -1	#can't find this area
"""
#a data indicate every week situation in an area
week_in_2014 = {}

print "there are %d areas" % len(list_1_2_deg)
"""week_in_2014 = area_name: [[week1, level], [week2, level], [week3, level]..., active?]"""
for k in list_1_2_deg:
	week_in_2014[k] = [[0, 0] for x in range(53)]		#2014 has 53 weeks
	week_in_2014[k].append(-1)				#default not active yet
	#test
	#print len(week_in_2014[k])

import csv
import re
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

	month = 0
	day = 0
	week = 0

	month = segment[2].split("/")[1]
	day = segment[2].split("/")[2]
	week = datetime.date(2014, int(month), int(day)).isocalendar()[1]
	
	
	if(segment[8] != "" ):
		
		if(segment[8] in week_in_2014 ):	
				
			valid_case += 1	
			#print segment[8], week
			week_in_2014[segment[8]][week - 1][0] += 1
			
print  "there are %d valid cases" %valid_case
#test
#print week_in_2014['A6405-1114-00']



"""build a case table"""

total = 0
header = [""]
for i in range(1, 54):
	header.append(str(i))

file = open("case.csv","w")
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


"""product action log (1+ people)"""

log_write = open("action_log_kaohsiung.txt", 'w')
log = []
#there are 51 actions(number from 1 to 51)
for i in range(1, 52):								#i indicate action number
	#time = [-1 for x in range(len(list_1_2_deg))]				#time is a list record every area do an action time, if no action, then = -1
	
	#for a new action, default it is inactive
	for k in week_in_2014:
		week_in_2014[k][53] = -1
	
	for k in week_in_2014:					
		for b in range(i - 1, i + 2):					#b indicate the block which need to lookup in the week_in_2014{}
			if(week_in_2014[k][b][0] > 0 and week_in_2014[k][53] == -1):		#more than 0 means action
				week_in_2014[k][53] = b
				log.append([k, i , b + 1])


log = sorted(log, key = lambda x : (x[1], x[2]))					#sort by two criteria (first by col1, then col2)
for each in log:
	print >> log_write, "%s" %each
log_write.close()



"""learning and fill the list_1_2_deg(Au, Av2u)"""

print "start learning"
now_action = 0
action = 0
for i in range(len(log)):
	
	
	#Au +1
	list_1_2_deg[log[i][0]][0] += 1

	now_action = log[i][1]
	for j in range(i+1, len(log)):
		conect = 0
		
		if log[j][1] == now_action and log[j][2] > log[i][2]:
			for k in list_1_2_deg[log[i][0]][1]:
				if k[0] == log[j][0]:
					conect = 1
					k[1] += 1	#Av2u +1
					action += 1
					
					#print "there is a action %d, cause by %d. %s to %s" %(action, i, log[i][0], log[j][0])
					break
			
		elif log[j][1] > now_action:
			
			break
#test
#print list_1_2_deg['A6412-0312-00']
#print list_1_2_deg['A6409-0129-00']

"""calculate probability by Av2u/Au"""
for k in list_1_2_deg:
	for p in list_1_2_deg[k][1]:
		if list_1_2_deg[k][0] != 0:		#avoid dividing zero
			p[1] = p[1] / float(list_1_2_deg[k][0])
#test
#print list_1_2_deg['A6412-0312-00']
#print list_1_2_deg['A6409-0129-00']
