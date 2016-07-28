"""
This is a table for area to area information:
each cell is a Cell object, with
pv,u (changed with t, a 3D value(dynamical)),
tau v,u (use for average time delay), in other words, mean life time for pv,u,t , 
Av2u
credit(a) (a list for all different action)
...

Also, need dict: infl(u), infl(a)

===========================================================

use class to store information, with tau, more pass week to expect
"""
class Cell(object):
	def __init__(self):
		self.pv_u_0 = 0
		self.tau = 1
		self.Av2u = 0
		self.credit_a = []
	def __repr__(self):
		return "p is %s. tau is %s. Av2u is %s. credit_a is %s." %  \
    	(self.pv_u_0, self.tau, self.Av2u, self.credit_a)
infl_u = {}
infl_a = {}

# step1: modify the table with cell, by origin deg1_2.py
from deg1_2 import list_1_2_deg

for k in list_1_2_deg:
	for l in list_1_2_deg[k][1]:
		l[1] = Cell()


# step2 learning with modified table, by origin week.py(2014)
# static and CT model only phase 1, DT model has phase 2
from week import week_in_2014, week_in_2015, log_2014, log_2015

#start learning
print "start learning"

#..phase 1: get Av, tau
print "phase 1"
now_action = 0
propagate = 0
for i in range(len(log_2014)):
	
	#Av +1
	list_1_2_deg[log_2014[i][0]][0] += 1

	now_action = log_2014[i][1]
	for j in range(i+1, len(log_2014)):
		conect = 0
		
		if log_2014[j][1] == now_action and log_2014[j][2] > log_2014[i][2]:
			for k in list_1_2_deg[log_2014[i][0]][1]:
				if k[0] == log_2014[j][0]:
					conect = 1
					k[1].Av2u += 1	#Av2u +1
					
					#can build a propagate graph...prop(a, v, u)
					#update tau
					k[1].tau = (k[1].tau * (k[1].Av2u - 1) + (log_2014[j][2] - log_2014[i][2])) / float(k[1].Av2u)
					
					propagate += 1
					break
			
		elif log_2014[j][1] > now_action:
			
			break

print propagate
# check and modify tau reassign to 0 that without propagating, then reset Av2u for phase 2:   
ok = 0
all = 0
for k in list_1_2_deg:
	for l in list_1_2_deg[k][1]:
		if l[1].Av2u == 0:
			l[1].tau = 0 
		
		#reset Av2u only for DT model
		#l[1].Av2u = 0
		
"""
#..phase 2:scan action log again,  get new Av2u, p

print "phase 2"
now_action = 0
propagate = 0
for i in range(len(log_2014)):

	now_action = log_2014[i][1]
	for j in range(i+1, len(log_2014)):
		conect = 0
		
		if log_2014[j][1] == now_action and log_2014[j][2] > log_2014[i][2]:
			for k in list_1_2_deg[log_2014[i][0]][1]:
				#now, if 0 < tu-tv <tau vu, form a action
				if k[0] == log_2014[j][0] and k[1].tau > (log_2014[j][2] - log_2014[i][2]):		
					conect = 1
					k[1].Av2u += 1	#Av2u +1
					
					propagate += 1
					break
			
		elif log_2014[j][1] > now_action:
			
			break

print propagate
"""
#calculate probability by Av2u/Au
for k in list_1_2_deg:
	for p in list_1_2_deg[k][1]:
		if list_1_2_deg[k][0] != 0:		#avoid dividing zero
			p[1].pv_u_0 = p[1].Av2u / float(list_1_2_deg[k][0])




# step 3: evaluating(expect), add some week before current time with exponential(concept of CT nodel)
from math import exp
def expect_next_week(predict, week, thresholds, x):
		
	for k in list_1_2_deg:
		predict[k] = 0
	for area in list_1_2_deg:

		# week is "this week", a int
		# thresholds is float to decide can be infected by neibor or not
		# area is a string indicating area name
		# x is itself probability if infected in te week
		
		others_to_me = []	#collect all propagate credit from neibor

		#if this week "area" has been infected, it should give itself a probability x for the next week to expect
		#past two week also have weaker influence, by arbitrary
		if week_in_2015[area][week][0] > 0:
			others_to_me.append(x)
		if week_in_2015[area][week - 1][0] > 0:
			others_to_me.append(x * 0.5)
		if week_in_2015[area][week - 2][0] > 0:
			others_to_me.append(x * 0.25)

		#past two week also have weaker influence, by exp
		for i in list_1_2_deg[area][1]:
			if week_in_2015[i[0]][week][0] > 0:
				for search in list_1_2_deg[i[0]][1]:
					if search[0] == area:
						others_to_me.append(search[1].pv_u_0)

			if week_in_2015[i[0]][week - 1][0] > 0:
				for search in list_1_2_deg[i[0]][1]:
					if search[0] == area:
						if search[1].pv_u_0 != 0:
							others_to_me.append( (search[1].pv_u_0) * exp(-(1 / search[1].tau)) ) 
							#print "e=",(search[1].pv_u_0) * exp(-(1 / search[1].tau))

			if week_in_2015[i[0]][week - 2][0] > 0:
				for search in list_1_2_deg[i[0]][1]:
					if search[0] == area:
						if search[1].pv_u_0 != 0:
							others_to_me.append( (search[1].pv_u_0) * exp(-(2 / search[1].tau)) ) 
							#print "e=",(search[1].pv_u_0) * exp(-(1 / search[1].tau))
						
			else:
				others_to_me.append(0)
		

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
	
#compare
print "let's experiment"

def experiment(predict,week):
	"""
	real = {}
	for k in list_1_2_deg:
		if week_in_2015[k][week][0] > 0:
			real[k] = 1
		else:
			real[k] = 0
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

	
	print "FPR is %f" %(FP / float(FP + TN))
	print "TPR is %f" %(TP / float(TP + FN))
	"""

	"""
	expexted newly infected or not newly infected
	"""
	
	# 1. newly infected(TPR):
	total_care = 0
	TP = 0
	for k in list_1_2_deg:
		if week_in_2015[k][week][0] > 0 and week_in_2015[k][week - 1][0] == 0:	# the case to be considered

			total_care += 1
			if predict[k] == 1:
				TP += 1
	print "newly infected TPR = ", TP / float(total_care)
	
	# 2. not newly infected:


thresholds_list = range(41)
for thres in thresholds_list:
	predict = {}
	expect_next_week(predict, 44, float(thres) / 40, 0.5)

	print "thresholds is %f" %(float(thres) / 40)	
	experiment(predict, 45)
