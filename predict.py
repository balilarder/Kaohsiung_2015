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

def read_graph(list_1_2_deg):
	file = open("Contagious graph.txt", "r")
	lines = file.readlines()

	print len(lines)
	for i in range(len(lines)):
		
		lines[i] = lines[i].replace(" ", "")
		
		segment = lines[i].split(":")
		
		
		list_1_2_deg[segment[0]] = AreaInfo()

		nodes = segment[1].split(",")
		nodes.pop()
		
		for node in nodes:
			list_1_2_deg[segment[0]].toother[node] = Cell()
			
		print segment[0], len(nodes)
		
"""
compute probabiliy(when assuming p is not constant)
"""
def computeProbability(list_1_2_deg, week_in_2014):
	
	for k in week_in_2014:
		for w in range(52):
			if w <= 50: 	# check 2 week after
				if week_in_2014[k][w][0] > 0:	
					list_1_2_deg[k].Av += 1
					# check itself
					if week_in_2014[k][w + 1][0] > 0 or week_in_2014[k][w + 2][0] > 0:
						list_1_2_deg[k].toitself.Av2u += 1

					# check its link
					for n1 in list_1_2_deg[k].toother:
						if week_in_2014[n1][w + 1][0] > 0 or week_in_2014[n1][w + 2][0] > 0:
							list_1_2_deg[k].toother[n1].Av2u += 1
			else: 			# only check 53th week
				if week_in_2014[k][w][0] > 0:	
					list_1_2_deg[k].Av += 1
					# check itself
					if week_in_2014[k][w + 1][0] > 0:
						list_1_2_deg[k].toitself.Av2u += 1

					# check its link
					for n1 in list_1_2_deg[k].toother:
						if week_in_2014[n1][w + 1][0] > 0:
							list_1_2_deg[k].toother[n1].Av2u += 1
	

	"""calculate probability by Av2u/Au"""
	print "calculate probability"
	
	# to other
	for k in list_1_2_deg:
		for p in list_1_2_deg[k].toother:
			if list_1_2_deg[k].Av != 0:		#avoid dividing zero
				list_1_2_deg[k].toother[p].pv_u_0 = list_1_2_deg[k].toother[p].Av2u / float(list_1_2_deg[k].Av)
	# to itself
	for k in list_1_2_deg:
		if list_1_2_deg[k].Av != 0:
			list_1_2_deg[k].toitself.pv_u_0 = list_1_2_deg[k].toitself.Av2u / float(list_1_2_deg[k].Av)
	


def analyze(prediction, week_in_2015, week, out, data):
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
			if not all(real[x] == 0 for x in list_1_2_deg[k].toother):
				case2 += 1
		elif (prediction[k] == 0 and real[k] == 1):
			FN += 1
			if all(real[x] == 0 for x in list_1_2_deg[k].toother):
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
	print "TP=%d,FP=%d, FN=%d, TN=%d" %(TP, FP, FN, TN)
	print "The result of week%d. TPR=%f, FPR=%f, distance=%f" %(week, TPR, FPR, distance)

	
	w = csv.writer(out)
	data.extend((FPR, TPR, distance, case1,case2, "", "", ""))
	#w.writerow(data)
	return data

if __name__ == '__main__':

	# read graph as input
	list_1_2_deg = {}
	read_graph(list_1_2_deg)
	# read real data
	week_in_2014 = {}
	week_in_2015 = {}
	read_data(list_1_2_deg, week_in_2014, week_in_2015)

	# compute probability
	computeProbability(list_1_2_deg, week_in_2014)

	# copy list_1_2_deg for 12 methods
	AllProbability = list_1_2_deg

	
	# both self and other are constant
	BothConst = [predictMethod.predictMethod1, predictMethod.predictMethod2,
	predictMethod.predictMethod3, predictMethod.predictMethod4]


	# not both self and other are constant
	NotBothConst = [predictMethod.predictMethod5, predictMethod.predictMethod6, 
	predictMethod.predictMethod7, predictMethod.predictMethod8, predictMethod.predictMethod9,
	predictMethod.predictMethod10, predictMethod.predictMethod11, predictMethod.predictMethod12]
	
	outputFileId = 1
	# first fourth method
	
	for iteration in BothConst:
		name = "Result of method" + str(outputFileId) + ".csv"
		outputFileId += 1

		# output a file
		test_parameter = [0.5]
		open(name, 'w').close()

		for parameter in test_parameter:
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
					prediction = iteration(list_1_2_deg, float(thres) / 40, week_in_2015, week, parameter)
					print "finish once"
					data = []
					print "thresholds is %f" %(float(thres) / 40)
					data.append(float(thres) / 40)
					analyze(prediction, week_in_2015, week, out, data)
					if len(all_rows) == 0:
						w.writerow(data)
					else:
						w.writerow(all_rows[row_index] + data)
						row_index += 1

				w.writerows(["\n"])
				row_index += 1
				
			out.close()

		# restore probability dict
		list_1_2_deg = AllProbability
		print name + " is finish"
	
	outputFileId = 5
	# remain 8 method
	for iteration in NotBothConst:
		name = "Result of method" + str(outputFileId) + ".csv"
		outputFileId += 1

		# output a file
		test_parameter = [0.5]
		open(name, 'w').close()

		for parameter in test_parameter:
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
					prediction = iteration(list_1_2_deg, float(thres) / 40, week_in_2015, week, parameter)
					print "finish once"
					data = []
					print "thresholds is %f" %(float(thres) / 40)
					data.append(float(thres) / 40)
					analyze(prediction, week_in_2015, week, out, data)
					if len(all_rows) == 0:
						w.writerow(data)
					else:
						w.writerow(all_rows[row_index] + data)
						row_index += 1

				w.writerows(["\n"])
				row_index += 1
				
			out.close()

		# restore probability dict
		list_1_2_deg = AllProbability
		print name + " is finish"

	

