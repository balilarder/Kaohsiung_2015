"""
* read the graph
* learn the probabiliy when need 
* predcit
* analyze
"""
import re
from graph import Cell, AreaInfo, read_data

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
	count = 0
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
		# count += 1
		# print count

	# test
	#list_1_2_deg['A6409-0129-00'].show()

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
	
# """
# prediction
# """
# # 36,37 44,45 50,51's 
# # result of prediction will be the same, because don't care time. so just compare with real data
# def predict(list_1_2_deg, thresholds, week_in_2015, week, parameter):
# 	prediction = {}
# 	for k in list_1_2_deg:
# 		prediction[k] = "?"

# 		contribution = []
# 		#self
# 		# if week_in_2015[k][week - 1][0] > 0:
# 		#  	contribution.append(parameter)
# 		# if week_in_2015[k][week - 2][0] > 0:
# 		#  	contribution.append(parameter * 0.5)
# 		# if week_in_2015[k][week - 3][0] > 0:
# 		#  	contribution.append(parameter * 0.25)
# 		#self end
# 		for neighbor1 in list_1_2_deg[k].toother:
# 			if week_in_2015[neighbor1][week - 1][0] > 0:
# 				contribution.append(list_1_2_deg[neighbor1].toother[k].pv_u_0)
# 			if week_in_2015[neighbor1][week - 2][0] > 0:
# 				contribution.append(list_1_2_deg[neighbor1].toother[k].pv_u_0 * 0.5)
# 			if week_in_2015[neighbor1][week - 3][0] > 0:
# 				contribution.append(list_1_2_deg[neighbor1].toother[k].pv_u_0 * 0.25)
# 		# ignore 2 deg
# 		"""
# 		for neighbor2 in list_1_2_deg[k].deg2:
# 			contribution.append(list_1_2_deg[neighbor2].deg2[k].pv_u_0)
# 		"""
# 		expection = 1.0
# 		for i in contribution:
# 			expection = expection * (1 - i)
# 		expection = 1 - expection
# 		#print expection
# 		if expection >= thresholds:
			
# 			prediction[k] = 1
# 		else:
	
# 			prediction[k] = 0
		
# 	return prediction

# def analyze(prediction, week_in_2015, week, out, data):
# 	real = {}
# 	for k in prediction:
# 		if week_in_2015[k][week][0] >= 1:
# 			real[k] = 1
# 		else:
# 			real[k] = 0

# 	TP = 0
# 	FP = 0
# 	FN = 0
# 	TN = 0

# 	# neighbor_infected = 0
# 	# neighbor_notinfected = 0
# 	# infected = 0
# 	# notinfected = 0 

# 	# for k in prediction:
# 	# 	if all(real[x] == 0 for x in list_1_2_deg[k].toother):
# 	# 		neighbor_notinfected += 1
# 	# 	else:
# 	# 		neighbor_infected += 1
# 	# print neighbor_notinfected + neighbor_infected
# 	case1 = 0
# 	case2 = 0
# 	# compute 2 case when guess wrong
# 	for k in prediction:
# 		if (prediction[k] == 1 and real[k] == 1):
# 			TP += 1
			
# 		elif(prediction[k] == 1 and real[k] == 0):
# 			FP += 1
# 			if not all(real[x] == 0 for x in list_1_2_deg[k].toother):
# 				case2 += 1
# 		elif (prediction[k] == 0 and real[k] == 1):
# 			FN += 1
# 			if all(real[x] == 0 for x in list_1_2_deg[k].toother):
# 				case1 += 1
# 		elif (prediction[k] == 0 and real[k] == 0):
# 			TN += 1
			
	
# 	FPR = FP / float(FP + TN)
# 	TPR = TP / float(TP + FN)
# 	distance = ((FPR - 0) ** 2 + (TPR - 1) ** 2) ** 0.5
# 	# if neighbor_notinfected != 0:
# 	# 	case1 = float(infected) / neighbor_notinfected 
# 	# else:
# 	# 	case1 = 0
# 	# if neighbor_infected != 0:
# 	# 	case2 = float(notinfected) / neighbor_infected
# 	# else:
# 	# 	case2 = 0
# 	case1 = float(case1) / (FP + FN)
# 	case2 = float(case2) / (FP + FN)
# 	print "TP=%d,FP=%d, FN=%d, TN=%d" %(TP, FP, FN, TN)
# 	print "The result of week%d. TPR=%f, FPR=%f, distance=%f" %(week, TPR, FPR, distance)

	
# 	w = csv.writer(out)
# 	data.extend((FPR, TPR, distance, case1,case2, "", "", ""))
# 	#w.writerow(data)
# 	return data

if __name__ == '__main__':

	# read graph as input
	list_1_2_deg = {}
	read_graph(list_1_2_deg)
	# read real data
	week_in_2014 = {}
	week_in_2015 = {}
	read_data(list_1_2_deg, week_in_2014, week_in_2015)

	# test
	print week_in_2014["A6405-1309-00"]

	# compute probability
	computeProbability(list_1_2_deg, week_in_2014)
