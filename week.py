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
			else:		#although it is 2104, but it seem as 2015
				#print "although %s is 2014, but it seem as 2015" %segment[2]
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
"""



#2014 action log
log_write = open("2014action_log_kaohsiung.txt", 'w')
log_2014 = []
#there are 51 actions(number from 1 to 51)
for i in range(1, 52):											#i indicate action number
	#time = [-1 for x in range(len(list_1_2_deg))]				#time is a list record every area do an action time, if no action, then = -1
	
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
for i in range(1, 52):											#i indicate action number
	#time = [-1 for x in range(len(list_1_2_deg))]				#time is a list record every area do an action time, if no action, then = -1
	
	#for a new action, default it is inactive
	for k in week_in_2015:
		week_in_2015[k][53] = -1
	
	for k in week_in_2015:					
		for b in range(i - 1, i + 2):							#b indicate the block which need to lookup in the week_in_2015{}
			if(week_in_2015[k][b][0] > 0 and week_in_2015[k][53] == -1):		#more than 0 means action
				week_in_2015[k][53] = b
				log_2015.append([k, i , b + 1])


log_2015 = sorted(log_2015, key = lambda x : (x[1], x[2]))				#sort by two criteria (first by col1, then col2)
for each in log_2015:
	print >> log_write, "%s" %each
log_write.close()


"""learning and fill the list_1_2_deg(Au, Av2u), noting that not to imported to table.py"""
if sys.argv[0] != "table.py":

	def build_propagate_graph():
		pass
	# write a file to indicate edges(propagate) 
	# format:<a(action number), v, u, tu-tv>

	print "start learning"
	now_action = 0
	action = 0
	for i in range(len(log_2014)):
		
		
		#Av +1
		list_1_2_deg[log_2014[i][0]][0] += 1

		now_action = log_2014[i][1]
		for j in range(i+1, len(log_2014)):
			conect = 0
			
			if log_2014[j][1] == now_action and log_2014[j][2] > log_2014[i][2]:
				for k in list_1_2_deg[log_2014[i][0]][1]:
					if k[0] == log_2014[j][0]:
						conect = 1
						k[1] += 1	#Av2u +1
						#can build a propagate graph...prop(a, v, u)

						action += 1
						
						#print "there is a action %d, cause by %d. %s to %s" %(action, i, log_2014[i][0], log_2014[j][0])
						break
				
			elif log_2014[j][1] > now_action:
				
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
