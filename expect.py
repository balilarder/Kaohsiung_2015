
id = []
probability_list = []
def debug (i):
	print id[i]
	print probability_list[i]
f1 = open("check.txt", 'r')
lines = f1.readlines()
#section 1:slicing string to from neibors
for i in range(len(lines)):
	each_list = []
	start = 0
	end = 0
	for ch in range(len(lines[i])):
		if lines[i][ch] == '[':
			start = ch +1
		if lines[i][ch] == ']':
			end = ch 
		area = lines[i].split(" ")[0]
		neibors = lines[i][start:end].replace(" ", "").replace("'", "").split(",")
	id.append(area)
	for each in neibors:
		dict = {}
		dict[each] = 0
		each_list.append(dict)
	probability_list.append(each_list)
f1.close()



#section 2: read table and convert to list form
import csv
f1 = open('writing.csv', 'r')
count = 0
lines = f1.readlines()


count = 0
for i in range(1,len(lines)):
	
	influence= lines[i].strip().split(",")
	for j in range(1,len(influence)):
	 	if float(influence[j]) > 0:
	 		count += 1
	 		update = id[j -1]
	 		for each in range(len(probability_list[i-1])):
	 			for key in probability_list[i-1][each]:
	 				if key == update:
	 					probability_list[i-1][each][key] = float(influence[j])
	 		
#print probability_list
#print count	
f1.close()


def search_index(x):
	i = 0
	for each in id:
		if each == x:
			break
		i += 1
	if i == len (id):
		return -1
	return i
#section 3: expection(try some different thresholds)
infected = [0 for x in range(len(id))]	#a bool list record infected or not, and to compute similarity in real data
predict = [0 for x in range(len(id))]
f1 = open('time-space.csv', 'r')
count = 0
	#goal: find infected in time[3](= line[3])
lines = f1.readlines()
col_name = lines[0].strip().split('\t')[1:]

case = lines[28].strip().split('\t')[1:]
#case = lines[5].strip().split('\t')[1:]	#want to expect after the time

for i in range(len(case)):
	if int(case[i]) > 0:
		#print col_name[i]
		for each in range(len(id)):
			if id[each] == col_name[i]:
				infected[each] = 1
				#print id[each]
				#print probability_list[each]
#print infected

f1.close()
def expect_next_time(thresholds, which):
	#thresholds is float to decide can be infected by neibor or not, which is a int indicating id in all areas
	others_to_me = []	#collect all propagate credit from neibor
	#print id[which]
	#print probability_list[which]

	#if this week "which" has been infected, it should give itself a probability x for the next week to expect
	if infected[which] == 1:
		others_to_me.append(0.8)
	for i in range(len(probability_list[which])):
		for key in probability_list[which][i]:
			#print key
			for j in range(len(probability_list[search_index(key)])):
				for being_infected in probability_list[search_index(key)][j]:
					if being_infected == id[which]:
						if infected[search_index(key)] == 1:
							others_to_me.append(probability_list[search_index(key)][j][being_infected])
						else:
							others_to_me.append(0)
						break
	#print others_to_me
	expection = 1.0
	for i in others_to_me:
		expection = expection * (1 - i)
	expection = 1- expection
	#print expection
	if expection >= thresholds:
		#print "%s is infected" %id[which]
		predict[which] = 1
	else:
		#print "%s isn't infected" %id[which]
		predict[which] = 0
	
#fuction end


#section 4 :compare, may copy "predict/compare(real situation)" to "infected" to process next interative
#There are four menchmark: TP, FP, FN, TN
def experiment():
	TP = 0
	FP = 0
	FN = 0
	TN = 0
	compare = [0 for x in range(len(id))]
	case = lines[29].strip().split('\t')[1:]	

	for i in range(len(case)):
		if int(case[i]) > 0:
			for each in range(len(id)):
				if id[each] == col_name[i]:
					compare[each] = 1

	for i in range(len(id)):
		if (predict[i] == 1 and compare[i] == 1):
			TP += 1
		elif(predict[i] == 1 and compare[i] == 0):
			FP += 1
		elif (predict[i] == 0 and compare[i] == 1):
			FN += 1
		elif (predict[i] == 0 and compare[i] == 0):
			TN += 1 
			
	print "TP is %d"  %TP
	print  "FP is %d" %FP
	print "FN is %d" %FN
	print "TN is %d" %TN
	print "Total is %d" %(TP + FP + FN + TN)
	print "TPR is %f" %(TP / float(TP + FN))
	print "FPR is %f" %(FP / float(FP + TN))


for loop in range(9):
	for i in range(len(id)):
		expect_next_time(loop * 0.1 + 0.1, i)
	print "thresholds is %f" %(loop * 0.1 + 0.1)	#0.1~0.9
	
	experiment()