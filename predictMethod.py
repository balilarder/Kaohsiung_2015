"""
prediction method:12 methods
"""
# 36,37 44,45 50,51's 
def convertToConstant(graph, constant):
	# to other
	for k in graph:
		for p in graph[k].toother:
			graph[k].toother[p].pv_u_0 = constant
	# to itself
	for k in graph:
		graph[k].toitself.pv_u_0 = constant
	
def predictResult(prediction, contribution, thresholds):
	for k in contribution:
		expection = 1.0
		for i in contribution[k]:
			expection = expection * (1 - i)
		expection = 1 - expection
		#print expection
		
		if thresholds == 0:		# all infected
			prediction[k] = 1
		elif thresholds == 1:	# all uninfected
			prediction[k] = 0

		else:
			if expection >= thresholds:
				
				prediction[k] = 1
			else:

				prediction[k] = 0


def predictMethod1(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	convertToConstant(graph, constant)

	prediction = {}
	contribution = {}	# Now, contribution is dictionary

	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0 * 0.25)
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

		print "predict a node"
		count += 1
		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod2(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	convertToConstant(graph, constant)

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0)
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		

		#print "predict a node"
#		count += 1
#		print count

	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod3(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	convertToConstant(graph, constant)

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		
		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod4(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	convertToConstant(graph, constant)

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod5(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	# other is constant
	for k in graph:
		for p in graph[k].toother:
			graph[k].toother[p].pv_u_0 = constant

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0)
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		
		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod6(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	# self is constant
	for k in graph:
		graph[k].toitself.pv_u_0 = constant

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0)
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		

		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod7(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0)
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		

		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod8(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		

		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod9(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	# other is constant
	for k in graph:
		for p in graph[k].toother:
			graph[k].toother[p].pv_u_0 = constant

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0 * 0.25)
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod10(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	# self is constant
	for k in graph:
		graph[k].toitself.pv_u_0 = constant

	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0 * 0.25)
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod11(graph, thresholds, week_in_2015, 
	week, constant):

	count = 0
	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		
		# self
		if week_in_2015[k][week - 1][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	contribution[k].append(graph[k].toitself.pv_u_0 * 0.25)
		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction

def predictMethod12(graph, thresholds, week_in_2015, 
	week, constant):
	count = 0
	prediction = {}
	contribution = {}	# Now, contribution is dictionary
	
	for k in graph:
		prediction[k] = "?"
		contribution[k] = []
	for k in graph:
		

		# other
		if week_in_2015[k][week - 1][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0)
		if week_in_2015[k][week - 2][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
		if week_in_2015[k][week - 3][0] > 0:
		 	for each in graph[k].toother:
		 		contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

		#print "predict a node"
#		count += 1
#		print count
	predictResult(prediction, contribution, thresholds)
		
	return prediction