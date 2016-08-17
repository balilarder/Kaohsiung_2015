import datetime
import csv
from week import list_1_2_deg, week_in_2014, week_in_2015


"""
predict function: based on real data(week in 2015) to predict specific week
return a dictionary of predict result
"""

def predict_next_week(predict, week, thresholds):
		
	#predict = {}
	for k in list_1_2_deg:
		predict[k] = 0
	for area in list_1_2_deg:

		# week is "this week", a int
		# thresholds is float to decide can be infected by neibor or not
		# area is a string indicating area name
		others_to_me = []	#collect all propagate credit from neibor

		#if this week "area" has been infected, it should give itself a probability x for the next week to expect
		# if week_in_2015[area][week][0] > 0:
		#  	others_to_me.append(list_1_2_deg[area].toself.pv_u_0)
		#  	#others_to_me.append(0.5)
		# if week_in_2015[area][week - 1][0] > 0:
		# 	others_to_me.append(list_1_2_deg[area].toself.pv_u_0 * 0.5)
		# 	#others_to_me.append(0.5 * 0.5)
		# if week_in_2015[area][week - 2][0] > 0:
		# 	others_to_me.append(list_1_2_deg[area].toself.pv_u_0 * 0.25)
		# 	#others_to_me.append(0.5 * 0.25)
		
		for n1 in list_1_2_deg[area].deg1:
			if week_in_2015[n1][week][0] > 0:
				others_to_me.append(list_1_2_deg[n1].deg1[area].pv_u_0)
				#others_to_me.append(0.5)
			if week_in_2015[n1][week - 1][0] > 0:
				others_to_me.append(list_1_2_deg[n1].deg1[area].pv_u_0 * 0.5)
				#others_to_me.append(0.5 * 0.5)
			if week_in_2015[n1][week - 2][0] > 0:
				others_to_me.append(list_1_2_deg[n1].deg1[area].pv_u_0 * 0.25)
				#others_to_me.append(0.5 * 0.25)
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
	return predict
	
"""
experiment function: observe the result of the changing between inactive and active in an area
especially 0 -> 1 in early time

"""

def experiment(predict,week, data):
	real = {}
	for k in list_1_2_deg:
		if week_in_2015[k][week][0] > 0:
			real[k] = 1
		else:
			real[k] = 0

	# analyze
	TP = 0
	FP = 0
	FN = 0
	TN = 0
	

	for k in list_1_2_deg:
		if (predict[k] == 1 and real[k] == 1):
			TP += 1
		elif(predict[k] == 1 and real[k] == 0):
			FP += 1
		elif (predict[k] == 0 and real[k] == 1):
			FN += 1
		elif (predict[k] == 0 and real[k] == 0):
			TN += 1 
	
	TPR = (TP / float(TP + FN))
	FPR = (FP / float(FP + TN))	
	distance = ((FPR - 0) ** 2 + (TPR - 1) ** 2) ** 0.5	
	# print "TP is %d"  %TP
	# print  "FP is %d" %FP
	# print "FN is %d" %FN
	# print "TN is %d" %TN
	# print "Total is %d" %(TP + FP + FN + TN)
	print "TPR is %f" %TPR
	print "FPR is %f" %FPR
	print "distance=%f" %distance
	data.extend((FPR, TPR, distance))

out = open("chart_summary.xlsx","w")
w = csv.writer(out)
check_week = [37, 45, 51]
for week in check_week:
	w.writerow(["The result of " + str(week) + " prediction:"] )
	w.writerow(["threshold", "FPR", "TPR", "distance", "AUC"])
	thresholds_list = range(41)
	for thres in thresholds_list:

		predict = {}
		predict_next_week(predict, week - 1, float(thres) / 40)
		data = []
		data.append(float(thres) / 40)
		

		print "thresholds is %f" %(float(thres) / 40)	
		experiment(predict, week, data)
		w.writerow(data)
out.close()