from graph import Cell, AreaInfo
import re
import csv
def read_graph_MoreEdge(graph):
	# read the file and constructure graph with more edege 
	file = open("Contagious graph.txt", "r")
	lines = file.readlines()

	print len(lines)
	for i in range(len(lines)):
		
		lines[i] = lines[i].replace(" ", "")
		
		segment = lines[i].split(":")
		
		
		graph[segment[0]] = AreaInfo()

		nodes = segment[1].split(",")
		nodes.pop()
		
		for node in nodes:
			graph[segment[0]].toother[node] = Cell()
			
		print segment[0], len(nodes)

def read_graph_Neighbor(graph):
	# read nrighbor file and constructure graph with neighbor link
	deg1 = open('neighbors_1deg.csv', 'r')
	lines_1 = deg1.readlines()

	
	total_areas = len(lines_1)

	for i in range(len(lines_1)):	#use regular expression to remove "  " " and " \n "
		lines_1[i] = re.sub('["\n]','',lines_1[i])


	for i in range(1, total_areas):
		segment1 = lines_1[i].split(",")
		segment1.pop()
		graph[segment1[0]] = AreaInfo()	# create an object information of area
		
		
		for j in range(1, len(segment1)):
			graph[segment1[0]].toother[segment1[j]] = Cell()
		
	deg1.close()

	