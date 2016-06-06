import csv
import re
deg1 = open('neighbors_1deg.csv', 'r')
lines_1 = deg1.readlines()

deg2 = open("neighbors_2deg.csv", 'r')
lines_2 = deg2.readlines()
total_areas = len(lines_1)

for i in range(len(lines_1)):	#use regular expression to remove "  " " and " \n "
	lines_1[i] = re.sub('["\n]','',lines_1[i])
	lines_2[i] = re.sub('["\n]','',lines_2[i])

segment = lines_1[1].split(",")
segment.pop()

list_1_2_deg= []
for i in range(1, total_areas):
	combination = [[], [], []]		#[[area_Au], [deg1_Pu2v], [deg2_Pu2v]]
	
	segment = lines_1[i].split(",")
	segment.pop()
	combination[0].append(segment[0])
	combination[0].append(0)
	

	for j in range(1, len(segment)):
		list1deg = []
		list1deg.append(segment[j])
		list1deg.append(0)
		combination[1].append(list1deg)
	
	segment = lines_2[i].split(",")
	segment.pop()

	for j in range(1, len(segment)):
		list2deg = []
		list2deg.append(segment[j])
		list2deg.append(0)
		combination[2].append(list2deg)
	list_1_2_deg.append(combination)
	
deg1.close()
deg2.close()