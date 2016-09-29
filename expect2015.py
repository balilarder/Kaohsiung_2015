import datetime

from week import list_1_2_deg

print "will expect 2015"

"""read 2015 case file(real case to compare)"""
real_in_2015 = {}
#real_in_2015 = area_name: [[week1, level], [week2, level], [week3, level]..., active?]"""

for k in list_1_2_deg:
	real_in_2015[k] = [[0, 0] for x in range(53)]		#2015 has 53 weeks
	real_in_2015[k].append(-1)				

import csv
import re

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

	month = 0
	day = 0
	week = 0

	month = segment[2].split("/")[1]
	day = segment[2].split("/")[2]
	week = datetime.date(2015, int(month), int(day)).isocalendar()[1]
	
	
	if(segment[8] != "" ):
		
		if(segment[8] in real_in_2015 ):	
				
			valid_case += 1	
			#print segment[8], week
			real_in_2015[segment[8]][week - 1][0] += 1
			
print  "there are %d valid cases" %valid_case
#test
#print real_in_2015['A6412-0176-00']
for i in real_in_2015:
	if real_in_2015[i][0][0] > 0:
		print i

"""
start expectation, real data by real_in_2015[k][0~52]
And Au, Av2u is from list_1_2_deg
"""

def expect_next_week(predict, week, thresholds, x):
		
	#predict = {}
	for k in list_1_2_deg:
		predict[k] = 0
	for area in list_1_2_deg:

		# week is "this week", a int
		# thresholds is float to decide can be infected by neibor or not
		# area is a string indicating area name
		# x is itself probability if infected in te week
		
		others_to_me = []	#collect all propagate credit from neibor

		#if this week "area" has been infected, it should give itself a probability x for the next week to expect
		if real_in_2015[area][week][0] > 0:
			others_to_me.append(x)
		"""
		for i in range(len(probability_list[area])):
			for key in probability_list[area][i]:
				
				for j in range(len(probability_list[search_index(key)])):
					for being_infected in probability_list[search_index(key)][j]:
						if being_infected == id[area]:
							if infected[search_index(key)] == 1:
								others_to_me.append(probability_list[search_index(key)][j][being_infected])
							else:
								others_to_me.append(0)
							break
		"""
		for i in list_1_2_deg[area][1]:
			if real_in_2015[i[0]][week][0] > 0:
				for search in list_1_2_deg[i[0]][1]:
					if search[0] == area:
						others_to_me.append(search[1])
						#print "haha", area
			else:
				others_to_me.append(0)
		

		#print others_to_me
		expection = 1.0
		for i in others_to_me:
			expection = expection * (1 - i)
		expection = 1- expection
		#print expection
		if expection >= thresholds:
			#print "%s is infected" %area
			predict[area] = 1
		else:
			#print "%s isn't infected" %area
			predict[area] = 0
	
"""experiment"""
print "let's experiment"

def experiment(predict,week):
	compare = {}
	for k in list_1_2_deg:
		if real_in_2015[k][week][0] > 0:
			compare[k] = 1
		else:
			compare[k] = 0
	TP = 0
	FP = 0
	FN = 0
	TN = 0
	#compare = [0 for x in range(len(id))]
	#case = lines[29].strip().split('\t')[1:]	
	"""
	for i in range(len(case)):
		if int(case[i]) > 0:
			for each in range(len(id)):
				if id[each] == col_name[i]:
					compare[each] = 1
	"""

	for k in list_1_2_deg:
		if (predict[k] == 1 and compare[k] == 1):
			TP += 1
		elif(predict[k] == 1 and compare[k] == 0):
			FP += 1
		elif (predict[k] == 0 and compare[k] == 1):
			FN += 1
		elif (predict[k] == 0 and compare[k] == 0):
			TN += 1 
			
	print "TP is %d"  %TP
	print  "FP is %d" %FP
	print "FN is %d" %FN
	print "TN is %d" %TN
	print "Total is %d" %(TP + FP + FN + TN)
	print "TPR is %f" %(TP / float(TP + FN))
	print "FPR is %f" %(FP / float(FP + TN))

thresholds_list = range(41)
for thres in thresholds_list:
	predict = {}
	expect_next_week(predict, 44, float(thres) / 40, 0.3)

	print "thresholds is %f" %(float(thres) / 40)	
	experiment(predict, 45)