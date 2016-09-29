"""
read neighbor information, and form a graph of 1,2 degree of neighbor
to a dict "list_1_2_deg"
"""
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


match = 0
unmatch = 0
list_1_2_deg= {}						
"""
{area: Av, [[1deg, Av2u],[]...], [[2deg, Av2u], [],...]}
note that Av2u will become probability
"""
for i in range(1, total_areas):

	segment1 = lines_1[i].split(",")
	segment1.pop()
	list_1_2_deg[segment1[0]] = []
	list_1_2_deg[segment1[0]].append(0)
	nei_1 = []
	for j in range(1, len(segment1)):
		list1deg = []
		list1deg.append(segment1[j])
		list1deg.append(0)
		nei_1.append(list1deg)
	list_1_2_deg[segment1[0]].append(nei_1)

for i in range(1, total_areas):
	segment2 = lines_2[i].split(",")
	segment2.pop()
	nei_2 = []
	for j in range(1, len(segment2)):
		list2deg = []
		list2deg.append(segment2[j])
		list2deg.append(0)
		nei_2.append(list2deg)
	list_1_2_deg[segment2[0]].append(nei_2)


print len(list_1_2_deg)


deg1.close()
deg2.close()