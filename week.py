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


"""
product action log (1+ people) both 2014 and 2015
2015 action log is to obseved the action time of a node, tv, in Discrete Time model 

* action log v2: consider the effect of self-propagation, by defining its action
"""
#2014 action log
log_write = open("2014action_log_kaohsiung.txt", 'w')
log_2014 = []
#there are 51 actions(number from 1 to 51)
for i in range(1, 52):									#i indicate action number
	
	
	#for a new action, default it is inactive
	for k in week_in_2014:
		week_in_2014[k][53] = -1
	
	for k in week_in_2014:					
		for b in range(i - 1, i + 2):							#b indicate the block which need to lookup in the week_in_2014{}
			if(week_in_2014[k][b][0] > 0 and week_in_2014[k][53] == -1):		#more than 0 means action
				week_in_2014[k][53] = b
				log_2014.append([k, i , b + 1])


log_2014 = sorted(log_2014, key = lambda x : (x[1], x[2]))				#sort by two criteria (first by col1, then col2)
for each in log_2014:
	print >> log_write, "%s" %each
log_write.close()

#2015 action log
log_write = open("2015action_log_kaohsiung.txt", 'w')
log_2015 = []
#there are 51 actions(number from 1 to 51)
for i in range(1, 52):									#i indicate action number
	
	
	#for a new action, default it is inactive
	for k in week_in_2015:
		week_in_2015[k][53] = -1
	
	for k in week_in_2015:					
		for b in range(i - 1, i + 2):
			#b indicate the block which need to lookup in the week_in_2015{}
			if(week_in_2015[k][b][0] > 0 and week_in_2015[k][53] == -1):		#more than 0 means action
				week_in_2015[k][53] = b
				log_2015.append([k, i , b + 1])


log_2015 = sorted(log_2015, key = lambda x : (x[1], x[2]))				#sort by two criteria (first by col1, then col2)
for each in log_2015:
	print >> log_write, "%s" %each
log_write.close()


"""learning and fill the list_1_2_deg(Au, Av2u), noting that not to imported to table.py"""
if sys.argv[0] == "expect2015.py":

	print "start learning"
	now_action = 0
	action = 0
	for i in range(len(log_2014)):
		
		#Av +1
		list_1_2_deg[log_2014[i][0]].Av += 1

		now_action = log_2014[i][1]

		# Learning probability to other
		for j in range(i+1, len(log_2014)):
			conect = 0
			
			if log_2014[j][1] == now_action and log_2014[j][2] > log_2014[i][2]:
				for k in list_1_2_deg[log_2014[i][0]].deg1:

					if k == log_2014[j][0]:
						conect = 1
						
						list_1_2_deg[log_2014[i][0]].deg1[k].Av2u += 1				#Av2u +1
						

						action += 1
						
						#print "there is a action %d, cause by %d. %s to %s" %(action, i, log_2014[i][0], log_2014[j][0])
						break
				
			elif log_2014[j][1] > now_action:
				
				break

		# Learning probability to self
		# The condition is that when an area do an action(in log), and its action id and action time is same
		# means the action is the earliest it could be, then check 2 week later. If once of then infected
		# seen as self propagation
		if log_2014[i][1] == log_2014[i][2]:
			if week_in_2014[log_2014[i][0]][log_2014[i][2]][0] > 0 or \
			week_in_2014[log_2014[i][0]][log_2014[i][2] + 1][0] > 0:
				# self += 1
				list_1_2_deg[log_2014[i][0]].toself.Av2u += 1


	print "total action(to other):%d" %action
	#test
	#print list_1_2_deg['A6412-0312-00']
	#print list_1_2_deg['A6409-0129-00']

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


	#test
	
	print "A6405-0814-00:"
	list_1_2_deg['A6405-0814-00'].show()
	print "A6409-0129-00"
	list_1_2_deg['A6409-0129-00'].show()
	
