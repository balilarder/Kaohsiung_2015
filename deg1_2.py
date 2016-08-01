"""
read neighbor information, and form a graph of 1,2 degree of neighbor
to a dict "list_1_2_deg"
"""
import csv
import re
class AreaInfo(object):
	def __init__(self):
		self.Av = 0
		self.deg1Av2u = {}
		self.deg2Av2u = {}
		self.toself = 0
	def show(self):
		print self.Av
		print self.deg1Av2u 
		print self.deg2Av2u 
		print self.toself
		


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


for i in range(1, total_areas):
	segment1 = lines_1[i].split(",")
	segment1.pop()
	list_1_2_deg[segment1[0]] = AreaInfo()
	
	
	for j in range(1, len(segment1)):
		list_1_2_deg[segment1[0]].deg1Av2u[segment1[j]] = 0
	

for i in range(1, total_areas):
	segment2 = lines_2[i].split(",")
	segment2.pop()

	
	
	for j in range(1, len(segment2)):
		list_1_2_deg[segment2[0]].deg2Av2u[segment2[j]] = 0


print len(list_1_2_deg)
# 17387
list_1_2_deg['A6432-0106-00'].show()

deg1.close()
deg2.close()