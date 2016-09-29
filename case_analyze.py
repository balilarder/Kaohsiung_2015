"""
1. analyze disease growing area whether cause by neighbor?? 
2. compare 2014 and 2015 initiator similarity
"""

import csv

from deg1_2 import list_1_2_deg
from week import week_in_2014, week_in_2015

print "1. analyze disease growing area whether cause by neighbor?? "

def new_active_infect_or_spontaneous(infor, w):
	# w is current week number
	# dict: 1=infect,0=spontaneous, both 1 and 0 is newly active, but -1=inactive or has been active for a time
	# compute a rate of infect_by_neighbor over newly_active
	dict = {}
	newly_active = 0
	infect_by_neighbor = 0
	for k in infor:
		if infor[k][w][0] > 0 and infor[k][w - 1][0] == 0:
			newly_active += 1
			flag = 0
			for j in list_1_2_deg[k][1]:
				if infor[j[0]][w - 1][0] > 0:
					flag = 1
					break
			if flag:
				dict[k] = 1
				infect_by_neighbor += 1
			else:
				dict[k] = 0		

		else:
			dict[k] = -1

	print "infect_by_neighbor", infect_by_neighbor
	print "newly_active", newly_active
	if newly_active == 0:
		return 0
	else:
		return infect_by_neighbor / float(newly_active)

# 2014
file = open("case_analyze.csv","w")
week_total_2014 = []
for i in range(53):
	total = 0
	for k in week_in_2014:
		total += week_in_2014[k][i][0]
	week_total_2014.append(total)
print week_total_2014

t = 0
for i in week_total_2014:
	t += i
print "t is ", t


w = csv.writer(file)
w.writerows([["2014 analyze"]])
w.writerows([["week number", "every week total case", "the rate of infected by neighbor"]])
for i in range(53):
	if i == 0:
		data = [i+1, week_total_2014[i], 0]
	else:
		data = [i+1, week_total_2014[i], new_active_infect_or_spontaneous(week_in_2014, i)]
	w.writerows([data])


# 2015
week_total_2015 = []
for i in range(53):
	total = 0
	for k in week_in_2015:
		total += week_in_2015[k][i][0]
	week_total_2015.append(total)
print week_total_2015

t = 0
for i in week_total_2015:
	t += i
print "t is ", t

w.writerows([[]])
w.writerows([[]])
w.writerows([["2015 analyze"]])
w.writerows([["week number", "every week total case", "the rate of infected by neighbor"]])
for i in range(53):
	if i == 0:		#2015's first week need to compare with 2014's last week, modify function
		newly_active = 0
		infect_by_neighbor = 0
		
		for k in week_in_2015:
			if week_in_2015[k][0][0] > 0 and week_in_2014[k][51][0] == 0:
				newly_active += 1
				flag = 0
				for j in list_1_2_deg[k][1]:
					if week_in_2014[j[0]][51][0] > 0:
						flag = 1
						break
				if flag:
					infect_by_neighbor += 1

		if newly_active == 0:
			r = 0
		else:
			r = infect_by_neighbor / float(newly_active)

		data = [i+1, week_total_2015[i], r]

	else:
		data = [i+1, week_total_2015[i], new_active_infect_or_spontaneous(week_in_2015, i)]
	w.writerows([data])

file.close()
print
print "2. compare 2014 and 2015 initiator similarity"
def early_similarity(w, d2014, d2015):
	# w is current week
	# use 2014, 2015's real week data to compute similarity
	s = 0
	vec1 = []
	vec2 = []
	for k in d2014:
		
		if d2014[k][w][0] > 0 or d2014[k][w + 1][0] or d2014[k][w - 1][0]:
			vec1.append(1)
		else:
			vec1.append(0)
		
		if d2015[k][w][0] > 0 or d2015[k][w + 1][0] or d2015[k][w - 1][0]:
			vec2.append(1)
		else:
			vec2.append(0)
		
		"""
		# directly append case number
		vec1.append(d2014[k][w][0])
		vec2.append(d2015[k][w][0])
		"""	
	AcrossB = 0
	vecALen = 0
	vecBLen = 0
	similarity = 0

	for x, y in zip(vec1, vec2):
		AcrossB += (x * y)
	
	for x in vec1:
		vecALen += (x ** 2)
	vecALen = vecALen ** 0.5
	
	for y in vec2:
		vecBLen += (y ** 2)
	vecBLen = vecBLen ** 0.5
	
	if (vecALen * vecBLen) == 0:
		return 0
	s = AcrossB / (vecALen * vecBLen)
	return s

list = []
for i in range(30, 40):
	list.append(early_similarity(i, week_in_2014, week_in_2015))

print list