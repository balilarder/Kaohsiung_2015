"""
prediction method:12 methods
"""
# 36,37 44,45 50,51's 
def convertToConstant(list_1_2_deg, constant):
	# to other
	for k in list_1_2_deg:
		for p in list_1_2_deg[k].toother:
			list_1_2_deg[k].toother[p].pv_u_0 = constant
	# to itself
	for k in list_1_2_deg:
		list_1_2_deg[k].toitself.pv_u_0 = constant
	
def predictResult(prediction, contribution, thresholds):
	for k in contribution:
		expection = 1.0
		for i in contribution[k]:
			expection = expection * (1 - i)
		expection = 1 - expection
		#print expection
		if expection >= thresholds:
			
			prediction[k] = 1
		else:

			prediction[k] = 0


def predictMethod1(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	convertToConstant(list_1_2_deg, constant)

	prediction = {}
	contribution = {}	# Now, contribution is dictionary

	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0 * 0.25)
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.25)

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod2(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	convertToConstant(list_1_2_deg, constant)

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0)
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		

		print "predict a node"
		count += 1
		print count

	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod3(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	convertToConstant(list_1_2_deg, constant)

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		
		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod4(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	convertToConstant(list_1_2_deg, constant)

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.25)

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod5(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	# other is constant
	for k in list_1_2_deg:
		for p in list_1_2_deg[k].toother:
			list_1_2_deg[k].toother[p].pv_u_0 = constant

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0)
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		
		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod6(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	# self is constant
	for k in list_1_2_deg:
		list_1_2_deg[k].toitself.pv_u_0 = constant

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0)
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod7(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0)
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod8(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod9(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	# other is constant
	for k in list_1_2_deg:
		for p in list_1_2_deg[k].toother:
			list_1_2_deg[k].toother[p].pv_u_0 = constant

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0 * 0.25)
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.25)

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod10(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	# self is constant
	for k in list_1_2_deg:
		list_1_2_deg[k].toitself.pv_u_0 = constant

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0 * 0.25)
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.25)

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod11(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):

	count = 0
	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	contribution[k].append(list_1_2_deg[k].toitself.pv_u_0 * 0.25)
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.25)

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod12(list_1_2_deg, thresholds, week_in_2015, 
	week, constant):
	count = 0
	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in list_1_2_deg:
		prediction[k] = "?"
		contribution[k] = []
	for k in list_1_2_deg:
		

		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in list_1_2_deg[k].toother:
		 		contribution[each].append(list_1_2_deg[k].toother[each].pv_u_0 * 0.25)

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction