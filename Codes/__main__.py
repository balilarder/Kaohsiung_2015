if __name__ == '__main__':
	import copy
	from graph import *
	from case import *
	from predict import *		# predict all
	from result import *
	from case_days import *		# observe day data for 2nd statistic area 
	import precisionkMethod		# only care for precision at k
	
	print "main function"

	# step1: determine graph structure, attribute table
	first_member = {}
	secondary_member = {}
	base2first_table = {}
	base2secondary_table = {}
	first2secondary_table = {}

	base_graph = {}
	first_graph = {}
	secondary_graph = {}

	base_populationTable= {}
	base_homeTable = {}
	base_areaTable = {}
	first_populationTable = {}
	first_homeTable = {}
	first_areaTable = {}
	secondary_populationTable = {}
	secondary_homeTable = {}
	secondary_areaTable = {}

	city = "K"
	# T/K

	BuildBase(base_graph, city)
	BuildBigger(base_graph, first_graph, secondary_graph, base2first_table, 
		base2secondary_table, first2secondary_table, first_member, secondary_member, city)
	# # test
	# print len(base_graph)
	# print len(first_member)
	# print len(secondary_member)

	# print first_member["A6405-54-006"]
	# print first_member["A6418-03-010"]

	# # print graph to file
	# g1 = open("first-graph.txt", "w")
	# for k in first_graph:
	#     print >> g1, "%s:" %k,
	#     for f in first_graph[k].toother:
	#         print >> g1, "%s," %f,
	#     print >> g1
	# g1.close()
	# g2 = open("second-graph.txt", "w")
	# for k in secondary_graph:
	#     print >> g2, "%s:" %k,
	#     for f in secondary_graph[k].toother:
	#         print >> g2, "%s," %f,
	#     print >> g2
	# g2.close()

	# get attribute table(Kaouhiung)
	if city == "K":
		base_populationTable = read_population()
		base_homeTable = read_home()
		base_areaTable = read_area()

		first_populationTable = BuildAttributeTable(base_populationTable, first_member)
		first_homeTable = BuildAttributeTable(base_homeTable, first_member)
		first_areaTable = BuildAttributeTable(base_areaTable, first_member)

		secondary_populationTable = BuildAttributeTable(first_populationTable, secondary_member)
		secondary_homeTable = BuildAttributeTable(first_homeTable, secondary_member)
		secondary_areaTable = BuildAttributeTable(first_areaTable, secondary_member)
	
	# New: case for day
	daydata = ReadCaseByDay(city, secondary_graph, base2first_table, base2secondary_table)
	

	Day2Csv(city+"2014", daydata[0])		# write 2014 csv
	Day2Csv(city+"2015", daydata[1])		# write 2015 csv

	# For observation...
	# build distance table: each node has its 1~5 distance list
	distance_Matrix = pairdistance(secondary_graph)


	exit()

	# step2: count case by weeks, based on given time interval, T
	
	base_2014 = {}
	base_2015 = {}

	first_2014 = {}
	first_2015 = {}

	secondary_2014 = {}
	secondary_2015 = {}
	# setting parameter and control
	g = 2
	T = 1
	MEcontrol = 0
	read_data(base_graph, base_2014, base_2015, T, city)

	# compute higher level case accumulation
	first_2014, first_2015 = accumulate(base_2014, base_2015, first_graph, first_member, T)
	secondary_2014, secondary_2015 = accumulate(first_2014, first_2015, secondary_graph, secondary_member, T)

	# output
	output_case(base_2014, "base_2014.csv", T) 
	output_case(base_2015, "base_2015.csv", T)

	output_case(first_2014, "first_2014.csv", T)
	output_case(first_2015, "first_2015.csv", T)

	output_case(secondary_2014, "secondary_2014.csv", T)
	output_case(secondary_2015, "secondary_2015.csv", T)

	if city == "K":
		phase = [37, 45, 49]		# early, middle,last
	elif city == "T":
		phase = [33, 36, 40]

	# p = phase[0]
	# this might influence situation

	
	# define "how many seen as infected?, situation means threshold for case"
	first_situation = def_situation(first_2014, T)
	secondary_situation = def_situation(secondary_2014, T)
	# for base_graph, infected if more than 0
	base_situation = {}
	for k in base_2014:
		base_situation[k] = 1
	
	"""
	The very easy condition (Fixed standard), situation for Tainan must be careful, 2014 is very little
	"""
	# 1st situation
	for k in first_2014:
		first_situation[k] = 1
		
	# 2nd situation
	for k in secondary_2014:
		secondary_situation[k] = 6

	"""
	more edge structure(option)
	sample from more edge to decrease link
	"""
	
	if MEcontrol:
		# build ME graph and compute probability
		# MEbase_graph = []
		# MEfirst_graph = []
		# MEsecondaey_graph = []
		if g == 0:
			print "MEbase_graph"
			MEbase_graph = MEgraph(base_graph, base_2014, base_2015, T, base_situation)
		elif g == 1:
			print "MEfirst_graph"
			MEfirst_graph = MEgraph(first_graph, first_2014, first_2015, T, first_situation)
		elif g == 2:
			print "MEsecondary_graph"
			MEsecondary_graph = MEgraph(secondary_graph, secondary_2014, secondary_2015, T, secondary_situation)
				
	# compute probability
	base_model = []
	first_model = []
	secondary_model = []
	if MEcontrol == 0:
		# use neighbor graph to compute probability as model
		if g == 0:
			for p in phase:
				computeProbability(base_graph, base_2014, base_2015, base_situation, T, p)
				model = copy.deepcopy(base_graph)
				# value = 0
				# for k in model:
				# 	for l in model[k].toother:
				# 		if model[k].toother[l].pv_u_0>0:
				# 			value+=1
				# print value
				base_model.append(model)

				# a=0
				# for k in model:
				# 	a += model[k].Av
				# print a/len(model)

				clearGraph(base_graph)

		# if base_model[0] != base_model[1] and base_model[1]!=base_model[2] and base_model[2] != base_model[0]:
		# 	print "all different"
		# # print len(base_model)
		# # print type(base_model[0])
		# print "three model's average Av"
		
		# for i in range(len(base_model)):
		# 	a=0
		# 	for k in base_model[i]:
		# 		for l in base_model[i][k].toother:
		# 			if base_model[i][k].toother[l].pv_u_0>0:
		# 				a += 1
		# 	print "good link",a

		# computeProbability(base_graph, base_2014, base_2015, base_situation, T, 37)

		# while 1:
		# 	pass
		if g == 1:
			for p in phase:
				computeProbability(first_graph, first_2014, first_2015, first_situation, T, p)
				model = copy.deepcopy(first_graph)
				first_model.append(model)
				clearGraph(first_graph)
		if g == 2:
			for p in phase:
				computeProbability(secondary_graph, secondary_2014, secondary_2015, secondary_situation, T, p)
				model = copy.deepcopy(secondary_graph)
				secondary_model.append(model)
				clearGraph(secondary_graph)
	else:
		# use ME graph as model
		if g == 0:
			for p in phase:
				computeProbability(MEbase_graph, base_2014, base_2015, base_situation, T, p)
				model = copy.deepcopy(MEbase_graph)
				base_model.append(model)
				clearGraph(MEbase_graph)
		
		elif g == 1:
			for p in phase:
				computeProbability(MEfirst_graph, first_2014, first_2015, first_situation, T, p)
				model = copy.deepcopy(MEfirst_graph)
				first_model.append(model)
				clearGraph(MEfirst_graph)

		elif g == 2:
			for p in phase:
				computeProbability(MEsecondary_graph, secondary_2014, secondary_2015, secondary_situation, T, p)
				model = copy.deepcopy(MEsecondary_graph)
				secondary_model.append(model)
				clearGraph(MEsecondary_graph)
		# base_model = MEbase_graph
		# first_model = MEfirst_graph
		# secondary_model = MEsecondaey_graph

	# print "there are nine model"
	# print len(base_model), len(first_model), len(secondary_model)

	# for i in range(len(base_model)):
	# 	a=0
	# 	for k in base_model[i]:
	# 		for l in base_model[i][k].toother:
	# 			if base_model[i][k].toother[l].pv_u_0>0:
	# 				a += 1
	# 	print "good link",a



	# step3: predict
	# condition, given graph, time, T, situation, a method, const of p

	# origin: parameter is graph, now modity to model, which is a list contain 3 graph
	container = [(base_model, base_2014, base_2015, base_situation),
	(first_model, first_2014, first_2015, first_situation),
	(secondary_model, secondary_2014, secondary_2015, secondary_situation)]

	
	const = 0.5
	filename = "method1-g0.csv"

	# g determine graph category, 0-base, 1-first, 2-secondary
	
	# observe p's decay rate
	print "observe p decay rate"
	rate = find_p_decay_rate(container[g][1], container[g][2], container[g][0][0], phase, container[g][3])

	print rate
	# while 1:
	# 	pass


	method = predictMethod11
	"""
	predict all: goal is AUC
	"""
	
	# container[g][0] is 3 models
	# OutputROC(filename, const, container[g][0], container[g][2], method, container[g][3], T, phase)

	# print len(container[g][0])

	# # clearGraph(container[g][0])
	# # computeProbability(container[g][0], container[g][1], container[g][2], container[g][3], T, 37)
	# # for m in container[g][0]:
	# # 	clearGraph(m)
	# # for id in range(len(container[g][0])):
	# # 	computeProbability(container[g][0][id], container[g][1], container[g][2], container[g][3], T, phase[id])



	# # step4: output
	# # compute AUC, efficiency, precision at k... 

	# # given a ROCfile as input, compute 3 AUC, 3 times
	# result = computeAUC("method1-g0.csv")		# give a file, comput AUC
	# print "result AUC is", result
	"""
	finish a AUC
	"""
	
	"""
	predict all: baseline, cos similarity vs our model
	"""
	# set a thres value
	ths = 0.025
	baseline(const, container[g][0], container[g][2], method, container[g][3], T, phase, ths)




	"""
	precision k: goal is precision
	"""
	# methodK = precisionkMethod.precisionkMethod11
	# print "setting a k"
	# f = open("p@k.csv", "w")
	# w = csv.writer(f)
	# for k in range(1,21):

	# 	precision = precisionkMethod.computeK(T, k, const, container[g][0], container[g][2], methodK,
	# 	container[g][3], phase, ifconf=0, newly=0)
	# 	# precision is a list, len=3, each of them is a period
	# 	print precision
	# 	w.writerow(precision)
	# 	# clearGraph(container[g][0])
	# 	# computeProbability(container[g][0], container[g][1], container[g][3], T)
	# 	for m in container[g][0]:
	# 		clearGraph(m)
	# 	for id in range(len(container[g][0])):
	# 		computeProbability(container[g][0][id], container[g][1], container[g][2], container[g][3], T, phase[id])

	# w.writerow(["g="+str(g), "T="+str(T)])
	# print "g=",g, "T=",T
