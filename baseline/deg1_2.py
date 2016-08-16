"""
* In baseline of the experiment, we don't need to learn to probabilities,
  just setting a value to its 1 deg neighbor, then 2 deg.(ex. 1/2, 1/4).
  When predict, don't care how many of its neighbor has been infected and 
  without considering the effect of time

  -> probability is constant

* Output: chart2.xlsx
"""
import sys
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
		return "p is %s" %(self.pv_u_0)
    
# Information collection of an area
class AreaInfo(object):
	def __init__(self):
		self.Av = 0
		self.deg1 = {}	# ex:{'A6432-0108-00': Cell1, 'A6432-0104-00': Cell2}
		self.deg2 = {}
		self.toitself = Cell()
	def show(self):
		
		print self.deg1 
		print self.deg2 
		
"""	
read neighbor information, and form a graph of 1,2 degree of neighbor
to a dict "list_1_2_deg"
"""
def baseline(p):
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
	list_1_2_deg = {}						


	for i in range(1, total_areas):
		segment1 = lines_1[i].split(",")
		segment1.pop()
		list_1_2_deg[segment1[0]] = AreaInfo()	# create an object information of area
		
		
		for j in range(1, len(segment1)):
			list_1_2_deg[segment1[0]].deg1[segment1[j]] = Cell()
			list_1_2_deg[segment1[0]].deg1[segment1[j]].pv_u_0 = p 
		

	for i in range(1, total_areas):
		segment2 = lines_2[i].split(",")
		segment2.pop()

		
		
		for j in range(1, len(segment2)):
			list_1_2_deg[segment2[0]].deg2[segment2[j]] = Cell()
			list_1_2_deg[segment2[0]].deg2[segment2[j]].pv_u_0 = p / p
	

	deg1.close()
	deg2.close()
	return list_1_2_deg
"""
real data
"""
import datetime
def read_data(list_1_2_deg, week_in_2014, week_in_2015):	
	
	print "there are %d areas" % len(list_1_2_deg)
	# week_in_2014 = area_name: [[week1, level], [week2, level], [week3, level]..., active?]

	for k in list_1_2_deg:
		week_in_2014[k] = [[0, 0] for x in range(53)]		#isocalendar may has 53 weeks in a year
		week_in_2014[k].append(-1)							#default not active yet
		
		week_in_2015[k] = [[0, 0] for x in range(53)]		#isocalendar may has 53 weeks in a year
		week_in_2015[k].append(-1)							#default not active yet


	#real data for 2014
	import csv
	import re

	print "2014 cases:"
	file = open('Kaohsiung2014_case.csv', 'r')
	lines = file.readlines()
	for i in range(len(lines)):	#use regular expression to remove" \n "
		lines[i] = re.sub('[\n]','',lines[i])
	print "there are %d case" %(len(lines) - 1)
	count = 0

	no_match = 0
	valid_case = 0

	trace = 0

	for i in range(1, len(lines)):
		segment = lines[i].split(",")

		year = 0
		month = 0
		day = 0
		week = 0
		tuple = ()

		year = segment[2].split("/")[0]
		month = segment[2].split("/")[1]
		day = segment[2].split("/")[2]
		tuple = datetime.date(int(year), int(month), int(day)).isocalendar()
		week = tuple[1]
		

		
		if(segment[8] != "" ):
			
			if(segment[8] in week_in_2014 ):	
					
				valid_case += 1	

				if tuple[0] == 2014:
					week_in_2014[segment[8]][week - 1][0] += 1
				else:		
					#although it is 2014, but it seem as 2015
					week_in_2015[segment[8]][week - 1][0] += 1
				
	print  "there are %d valid cases" %valid_case
	file.close()
	print

	#real data for 2015
	print "2015 cases:"
	file = open('Kaohsiung2015_case.csv', 'r')
	lines = file.readlines()
	for i in range(len(lines)):	#use regular expression to remove" \n "
		lines[i] = re.sub('[\n]','',lines[i])
	print "there are %d case" %(len(lines) - 1)
	count = 0

	no_match = 0
	valid_case = 0

	trace = 0

	for i in range(1, len(lines)):
		segment = lines[i].split(",")

		year = 0
		month = 0
		day = 0
		week = 0
		tuple = ()

		year = segment[2].split("/")[0]
		month = segment[2].split("/")[1]
		day = segment[2].split("/")[2]
		tuple = datetime.date(int(year), int(month), int(day)).isocalendar()
		week = tuple[1]
		

		
		if(segment[8] != "" ):
			
			if(segment[8] in week_in_2015 ):	
					
				valid_case += 1	

				if tuple[0] == 2015:
					week_in_2015[segment[8]][week - 1][0] += 1
				
	print  "there are %d valid cases" %valid_case
	file.close()


"""
prediction
"""
# 36,37 44,45 50,51's 
# result of prediction will be the same, because don't care time. so just compare with real data
def predict(list_1_2_deg, thresholds, week_in_2015, week, parameter):
	prediction = {}
	for k in list_1_2_deg:
		prediction[k] = "?"

		contribution = []
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution.append(parameter)
		if week_in_2015[k][week - 2][0] > 0:
		 	contribution.append(parameter * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	contribution.append(parameter * 0.25)
		# self end
		for neighbor1 in list_1_2_deg[k].deg1:
			if week_in_2015[neighbor1][week - 1][0] > 0:
				contribution.append(list_1_2_deg[neighbor1].deg1[k].pv_u_0)
			if week_in_2015[neighbor1][week - 2][0] > 0:
				contribution.append(list_1_2_deg[neighbor1].deg1[k].pv_u_0 * 0.5)
			if week_in_2015[neighbor1][week - 3][0] > 0:
				contribution.append(list_1_2_deg[neighbor1].deg1[k].pv_u_0 * 0.25)
		# ignore 2 deg
		"""
		for neighbor2 in list_1_2_deg[k].deg2:
			contribution.append(list_1_2_deg[neighbor2].deg2[k].pv_u_0)
		"""
		expection = 1.0
		for i in contribution:
			expection = expection * (1 - i)
		expection = 1 - expection
		#print expection
		if expection >= thresholds:
			
			prediction[k] = 1
		else:
	
			prediction[k] = 0
		
	return prediction

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

	for k in prediction:
		if (prediction[k] == 1 and real[k] == 1):
			TP += 1
		elif(prediction[k] == 1 and real[k] == 0):
			FP += 1
		elif (prediction[k] == 0 and real[k] == 1):
			FN += 1
		elif (prediction[k] == 0 and real[k] == 0):
			TN += 1
	
	FPR = FP / float(FP + TN)
	TPR = TP / float(TP + FN)
	distance = ((FPR - 0) ** 2 + (TPR - 1) ** 2) ** 0.5
	print "TP=%d,FP=%d, FN=%d, TN=%d" %(TP, FP, FN, TN)
	print "The result of week%d. TPR=%f, FPR=%f, distance=%f" %(week, TPR, FPR, distance)

	
	w = csv.writer(out)
	data.extend((FPR, TPR, distance))
	#w.writerow(data)
	return data

if __name__ == "__main__":
	test_parameter = [0.5, 0.33, 0.2, 0.15, 0.1]
	open("chart2.xlsx", 'w').close()

	for parameter in test_parameter:
		out = open("chart2.xlsx","r+")
		
		w = csv.writer(out)
		r = csv.reader(out)

		list_1_2_deg = baseline(parameter)
		print len(list_1_2_deg)	# should be 17387
		# test
		#list_1_2_deg['A6432-0106-00'].show()
		
		week_in_2014 = {}
		week_in_2015 = {}
		read_data(list_1_2_deg, week_in_2014, week_in_2015)

		print "start predict"
		all_rows = []
		row_index = 0
		for rows in r:
			all_rows.append(rows)
		out.seek(0)


		print len(all_rows)
		if len(all_rows) == 0:
			w.writerow(["baseline method, p=" + str(parameter), "", "", ""] )
		else:
			w.writerow(all_rows[row_index] + ["baseline method, p=" + str(parameter), "", "" ,""] )
			row_index += 1

		check_week = [37, 45, 51]
		
		for week in check_week:

			if len(all_rows) == 0:
				w.writerow(["The result of " + str(week) + " prediction:", "", "", ""] )
				w.writerow(["threshold", "FPR", "TPR", "distance"])
			else:
				w.writerow(all_rows[row_index] + ["The result of " + str(week) + " prediction:", "", "", ""] )
				row_index += 1
				w.writerow(all_rows[row_index] + ["threshold", "FPR", "TPR", "distance"])
				row_index += 1

			thresholds_list = range(41)
			for thres in thresholds_list:
				prediction = predict(list_1_2_deg, float(thres) / 40, week_in_2015, week, parameter)
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
	