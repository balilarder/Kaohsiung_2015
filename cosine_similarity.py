import csv
f1 = open('time-space.csv', 'r')
lines = f1.readlines()
areas = lines[0].strip().split('\t')[1:]	#get all areas in time-space(5538)

def search_index(x):
	i = 0
	for each in areas:
		if each == x:
			break
		i += 1
	if i == len (areas):
		return -1
	return i

def cos(listA, listB):
	#compute cosine similarity of two int lists
	AcrossB = 0
	vecALen = 0
	vecBLen = 0
	similarity = 0
	for x, y in zip(listA, listB):
		AcrossB += (x * y)
	
	for x in listA:
		vecALen += (x ** 2)
	vecALen = vecALen ** 0.5
	
	for y in listB:
		vecBLen += (y ** 2)
	vecBLen = vecBLen ** 0.5
	
	if (vecALen * vecBLen) == 0:
		return 0
	similarity = AcrossB / (vecALen * vecBLen)
	return similarity


def real(k):
	#return a list of real data in week k
	output = lines[k].strip().split('\t')[1:]
	output = map(int, output)
	return  output
	

def predict(k):
	#predict the situation of k'nd week, and return a list 
	
	#we need to check over past k-1 weeks, find the highest similarity, then use its next to predict k 

	pass_record = []	#a list that record the similarity of pass(k-1) weeks and the k'nd week
	i = 1			#i indicate which line to compute
	while i < k-1:
		pass_record.append(cos(real(i), real(k - 1)))
		
		i += 1
	#print pass_record
	#find the largest id
	m = max(pass_record)
	#get its position
	position = [i for i, j in enumerate(pass_record) if j == m]
	#print position
	target = position[0] + 1
	
	#print "%d and %d is the most similarity" %(k - 1, target)
	result = []
	for i in range(len(real(target + 1))):
		result.append(real(target + 1)[i])
	return result


def compare(k):
	#get real k'nd week, comparing with predict(k), get TP, FP, FN, TN

	#argument: set different k, and find difference
	TP = 0
	FP = 0
	FN = 0
	TN = 0
	#predict(k) vs real(k)
	a = predict(k)
	b = real(k)

	for i in range(len(areas)):
		if (a[i] == 1 and b[i] == 1):
			TP += 1
		elif(a[i] == 1 and b[i] == 0):
			FP += 1
		elif (a[i] == 0 and b[i] == 1):
			FN += 1
		elif (a[i] == 0 and b[i] == 0):
			TN += 1 
			
	print "TP is %d"  %TP
	print  "FP is %d" %FP
	print "FN is %d" %FN
	print "TN is %d" %TN
	print "Total is %d" %(TP + FP + FN + TN)
	print "TPR is %f" %(TP / float(TP + FN))
	print "FPR is %f" %(FP / float(FP + TN))

#the lower bound and upper bound of prediction = 3 to 35
#print cos(predict(3), real(2))
#print cos(predict(35), real(34))

#experiment#
for i in range(3, 36):
	print "compare week %d" %i
	compare(i)
f1.close()