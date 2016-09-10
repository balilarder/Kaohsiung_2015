"""
* read the graph
* learn the probabiliy when need 
* predcit by 12 method with "predictMethod"
* analyze and output 12 result
"""
import re
import csv
from graph import Cell, AreaInfo, read_data
import predictMethod
from ReadGraph import read_graph_MoreEdge, read_graph_Neighbor

		
"""
compute probabiliy(when assuming p is not constant)
"""
def computeProbability(graph, week_in_2014):
	
	for k in week_in_2014:
		for w in range(52):
			if w <= 50: 	# check 2 week after
				if week_in_2014[k][w][0] > 0:	
					graph[k].Av += 1
					# check itself
					if week_in_2014[k][w + 1][0] > 0 or week_in_2014[k][w + 2][0] > 0:
						graph[k].toitself.Av2u += 1

					# check its link
					for n1 in graph[k].toother:
						if week_in_2014[n1][w + 1][0] > 0 or week_in_2014[n1][w + 2][0] > 0:
							graph[k].toother[n1].Av2u += 1
			else: 			# only check 53th week
				if week_in_2014[k][w][0] > 0:	
					graph[k].Av += 1
					# check itself
					if week_in_2014[k][w + 1][0] > 0:
						graph[k].toitself.Av2u += 1

					# check its link
					for n1 in graph[k].toother:
						if week_in_2014[n1][w + 1][0] > 0:
							graph[k].toother[n1].Av2u += 1
	

	"""calculate probability by Av2u/Au"""
	print "calculate probability"
	
	# to other
	for k in graph:
		for p in graph[k].toother:
			if graph[k].Av != 0:		#avoid dividing zero
				graph[k].toother[p].pv_u_0 = graph[k].toother[p].Av2u / float(graph[k].Av)
	# to itself
	for k in graph:
		if graph[k].Av != 0:
			graph[k].toitself.pv_u_0 = graph[k].toitself.Av2u / float(graph[k].Av)
	

def clearGraph(graph):
	# reset information but remain graph shape
	for k in graph:
		graph[k].Av = 0
		graph[k].toitself.Av2u = 0
		graph[k].toitself.pv_u_0 = 0
		for link in graph[k].toother:
			graph[k].toother[link].Av2u = 0
			graph[k].toother[link].pv_u_0 = 0

def analyze(prediction, week_in_2015, week, out, data, graph):
	real = {}
	for k in prediction:
		if week_in_2015[k][week][0] >= 1:
			real[k] = 1
		else:
			real[k] = 0

	TP = 0
	FP = 0
	FN = 0
	TN = 0

	# neighbor_infected = 0
	# neighbor_notinfected = 0
	# infected = 0
	# notinfected = 0 

	# for k in prediction:
	# 	if all(real[x] == 0 for x in list_1_2_deg[k].toother):
	# 		neighbor_notinfected += 1
	# 	else:
	# 		neighbor_infected += 1
	# print neighbor_notinfected + neighbor_infected
	case1 = 0
	case2 = 0
	# compute 2 case when guess wrong
	for k in prediction:
		if (prediction[k] == 1 and real[k] == 1):
			TP += 1
			
		elif(prediction[k] == 1 and real[k] == 0):
			FP += 1
			if not all(real[x] == 0 for x in graph[k].toother):
				case2 += 1
		elif (prediction[k] == 0 and real[k] == 1):
			FN += 1
			if all(real[x] == 0 for x in graph[k].toother):
				case1 += 1
		elif (prediction[k] == 0 and real[k] == 0):
			TN += 1
			
	
	FPR = FP / float(FP + TN)
	TPR = TP / float(TP + FN)
	distance = ((FPR - 0) ** 2 + (TPR - 1) ** 2) ** 0.5
	# if neighbor_notinfected != 0:
	# 	case1 = float(infected) / neighbor_notinfected 
	# else:
	# 	case1 = 0
	# if neighbor_infected != 0:
	# 	case2 = float(notinfected) / neighbor_infected
	# else:
	# 	case2 = 0
	case1 = float(case1) / (FP + FN)
	case2 = float(case2) / (FP + FN)
	# print "TP=%d,FP=%d, FN=%d, TN=%d" %(TP, FP, FN, TN)
	# print "The result of week%d. TPR=%f, FPR=%f, distance=%f" %(week, TPR, FPR, distance)

	
	w = csv.writer(out)
	data.extend((FPR, TPR, distance, case1,case2, "", "", ""))
	#w.writerow(data)
	return data

def OutputFile(filename, constant_list, graph, week_in_2015, iteration):

	open(name, 'w').close()

	for parameter in constant_list:
		out = open(name,"r+")
		
		w = csv.writer(out)
		r = csv.reader(out)
		
		print "start predict"
		all_rows = []
		row_index = 0
		for rows in r:
			all_rows.append(rows)
		out.seek(0)


		print len(all_rows)
		if len(all_rows) == 0:
			w.writerow(["baseline method, p=" + str(parameter), "","","", "", "", "", "", ""] )
		else:
			w.writerow(all_rows[row_index] + ["baseline method, p=" + str(parameter), "","","", "", "" ,"", "", ""] )
			row_index += 1

		check_week = [37, 45, 51]
		
		for week in check_week:

			if len(all_rows) == 0:
				w.writerow(["The result of " + str(week) + " prediction:", "","","", "", "", "", "", ""] )
				w.writerow(["threshold", "FPR", "TPR", "distance", "case1 rate", "case2 rate","", "", ""])
			else:
				w.writerow(all_rows[row_index] + ["The result of " + str(week) + " prediction:", "","","", "", "", "", "", ""] )
				row_index += 1
				w.writerow(all_rows[row_index] + ["threshold", "FPR", "TPR", "distance","case1 rate","case2 rate","","", ""])
				row_index += 1

			thresholds_list = range(41)
			for thres in thresholds_list:
				prediction = iteration(graph, float(thres) / 40, week_in_2015, week, parameter)
				#print "finish once"
				data = []
				#print "thresholds is %f" %(float(thres) / 40)
				data.append(float(thres) / 40)
				analyze(prediction, week_in_2015, week, out, data, graph)
				if len(all_rows) == 0:
					w.writerow(data)
				else:
					w.writerow(all_rows[row_index] + data)
					row_index += 1

			w.writerows(["\n"])
			row_index += 1

		out.close()


if __name__ == '__main__':

	# read 2 kinds of graph as input
	graph_MoreEdge = {}
	graph_NeighborEdge = {}
	
	read_graph_MoreEdge(graph_MoreEdge)
	read_graph_Neighbor(graph_NeighborEdge)

	
	# read real data to get week in 2014, 2015
	week_in_2014 = {}
	week_in_2015 = {}
	read_data(graph_NeighborEdge, week_in_2014, week_in_2015)
	

	# compute probability for two graphs
	computeProbability(graph_MoreEdge, week_in_2014)
	computeProbability(graph_NeighborEdge, week_in_2014)



	# both self and other are constant
	BothConst = [predictMethod.predictMethod1, predictMethod.predictMethod2,
	predictMethod.predictMethod3, predictMethod.predictMethod4]


	# not both self and other are constant
	NotBothConst = [predictMethod.predictMethod5, predictMethod.predictMethod6,
	predictMethod.predictMethod7, predictMethod.predictMethod8, predictMethod.predictMethod9,
	predictMethod.predictMethod10, predictMethod.predictMethod11, predictMethod.predictMethod12]
	
	graph_kind = [graph_NeighborEdge, graph_MoreEdge]
	#graph_kind = [graph_MoreEdge]
	for g in graph_kind:

		outputFileId = 1
		# first fourth method
		for iteration in BothConst:
			name = str(graph_kind.index(g) + 1) + " method" + str(outputFileId) + ".csv"
			outputFileId += 1

			# output a file
			const_parameter = [0.5]
			OutputFile(name, const_parameter, g, week_in_2015, iteration)
			
			# clear Av, Av2u, and recalculate probability graph
			"""
			g = {}
			if g == graph_NeighborEdge:
				read_graph_Neighbor(g)
			elif g == graph_MoreEdge:
				read_graph_MoreEdge(g)
			"""
			clearGraph(g)
			computeProbability(g, week_in_2014)
			print name + " is finish"
		
		
		outputFileId = 5
		# remain 8 method
		for iteration in NotBothConst:
			name = str(graph_kind.index(g) + 1) + " method" + str(outputFileId) + ".csv"
			outputFileId += 1

			# output a file
			const_parameter = [0.5]

			OutputFile(name, const_parameter, g, week_in_2015, iteration)
			
			# clear Av, Av2u, and recalculate probability graph
			"""
			g = {}
			if g == graph_NeighborEdge:
				read_graph_Neighbor(g)
			elif g == graph_MoreEdge:
				read_graph_MoreEdge(g)
			"""
			clearGraph(g)
			computeProbability(g, week_in_2014)
			print name + " is finish"
	
	

