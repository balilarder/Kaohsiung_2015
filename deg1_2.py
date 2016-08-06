"""
read neighbor information, and form a graph of 1,2 degree of neighbor
to a dict "list_1_2_deg"

combine AreaInfo with Cell to build a table maintain information
"""
import csv
import re

# A relation between an area and its neighborhoods
class Cell(object):
	def __init__(self):
		self.pv_u_0 = 0
		self.tau = 1
		self.Av2u = 0
		self.credit_a = []
	def __repr__(self):
		return "p is %s. tau is %s. Av2u is %s. credit_a is %s." %  \
    	(self.pv_u_0, self.tau, self.Av2u, self.credit_a)
# Information collection of an area
class AreaInfo(object):
	def __init__(self):
		self.Av = 0
		self.deg1 = {}	# ex:{'A6432-0108-00': Cell1, 'A6432-0104-00': Cell2}
		self.deg2 = {}
		self.toself = Cell()
	def show(self):
		print self.Av
		print self.deg1 
		print self.deg2 
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
	list_1_2_deg[segment1[0]] = AreaInfo()	# create an object information of area
	
	
	for j in range(1, len(segment1)):
		list_1_2_deg[segment1[0]].deg1[segment1[j]] = Cell()
	

for i in range(1, total_areas):
	segment2 = lines_2[i].split(",")
	segment2.pop()

	
	
	for j in range(1, len(segment2)):
		list_1_2_deg[segment2[0]].deg2[segment2[j]] = Cell()


print len(list_1_2_deg)	# should be 17387
# test
#list_1_2_deg['A6432-0106-00'].show()

deg1.close()
deg2.close()