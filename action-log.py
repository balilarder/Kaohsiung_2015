"""get area in time-space"""
f1=open("time-space.txt")
lines=f1.readlines()
#print lines[0]
A = 0
for ch in lines[0]:
	if ch == "A":
		A += 1
print "there are %d areas~" %A
areas = lines[0].split("\t")	#areas is area in the time-space
del(areas[0])	#del first element
areas[len(areas) - 1] = areas[len(areas) - 1].rstrip()
#print areas

"""find area in neighbor then construct graph"""
match = []	#bool list
neighbor = {}	#neighbor dict
for i in range(len(areas)):
	match.append(False)

import csv
f2 = open('neighbors.csv', 'r')
index = 0
count = 0
for row in csv.DictReader(f2):
	index += 1
	if row['codebase'].strip() in areas:
		#print "find: %d in %d" %(index, areas.index(row['codebase'].strip()))
		match[areas.index(row['codebase'].strip())] = True
		neighbor[row['codebase'].strip()] = row['neighbors'].split(",")
		if "" in neighbor[row['codebase'].strip()]:
			neighbor[row['codebase'].strip()].remove("")
			

		count += 1
f2.close()
"""check every neibor whether in time space??"""
for key in neighbor:
	neighbor[key] = [x for x in (neighbor[key]) if x in areas]


print "count = %d" %count

"""find which is false(unmatch)??"""
unmatch = 0
for i in range(len(match)):
	if match[i] == False:
		unmatch += 1
		print "%d is false" %i
#print unmatch
#print neighbor

"""open a file and print to debug"""
f3 = open("check.txt", 'w')
for each in neighbor:
	print >> f3, "%s -- %s" %(each, neighbor[each])
f3.close()

f6 = open("total.txt", 'w')
for each in areas:
	print >> f6, "%s" %(each)

f6.close()

"""functions"""
def extract(week):
	lst = lines[week].split("\t")	#areas is area in the time-space
	del(lst[0])	#del first element
	lst[len(areas) - 1] =lst[len(areas) - 1].rstrip()	#delete newline
	return lst
"""a function to seach areas index [x][y]"""
def search_index(x):
	i = 0
	for each in neighbor:
		if each == x:
			break
		i += 1
	if i == len (neighbor):
		return -1
	return i

"""build action log.csv"""
time = []
for i in range(len(areas)):
	time.append(-1)
log = []
def action_log(a):
	# a is  action index
	for i in range(len(areas)):
		time[i] = -1#initial no infected
	for i in range(a, a+3):
		case = extract(i)
		for j in range(len(case)):
			if int(case[j]) > 0 and time[j] == -1:
				time[j] = i
	for i in range(len(match)):
		if match[i] == True and time[i] != -1:
			log.append([areas[i], a, time[i]])

	#testing
	#for k in log:
		#print k

for i in range(1, 27):
	action_log(i)
log = sorted(log, key = lambda x : (x[1], x[2]))	#sort by two criteria (first by col1, then col2)


f4 = open("action_log.txt", 'w')
for each in log:
	print >> f4, "%s" %each
f4.close()


f7 = open('action_log.csv', 'w')
writer = csv.writer(f7)
writer.writerow(["Areas", "action number", "infected time"])
for each in log:
   	writer.writerow([each[0], each[1], each[2]])

f7.close()

"""counting Au, Av2u"""
Au = []
for i in range(0, len(neighbor)):
	Au.append(0)
Av2u = [[0 for x in range(len(neighbor))] for x in range(len(neighbor))]
probability = [[0 for x in range(len(neighbor))] for x in range(len(neighbor))]
for i in range(len(neighbor)):
	for j in range(len(neighbor)) :
		if i == j :
			probability[i][j] = -1

#debug
f10 = open("infection.txt", 'w')



print "len Au is:", len(Au)
now_action = 0
for i in range(len(log)):
	
	print >> f10, log[i]
	Au[search_index(log[i][0])] += 1

	now_action = log[i][1]
	for j in range(i+1, len(log)):
		conect = 0
		print >> f10, "let's check %s and %s "%(log[i][0], log[j][0])
		if log[j][1] == now_action and log[j][2] > log[i][2]:
			for k in neighbor[log[i][0]]:
				if k == log[j][0]:
					conect = 1
					break
			if conect == 1:	
				#there is a infection
				#Av2u increment
				print >> f10, "%s infection %s with %d action!!! "%(log[i][0], log[j][0], now_action)
				Av2u[search_index(log[i][0])][search_index(log[j][0])] += 1
				
			else:
				print >> f10, "%s and %s are not neighbor" %(log[i][0], log[j][0])
		elif log[j][1] > now_action:
			print >> f10, "not the same action!!!"
			break
			



print  "Au testing", Au[search_index("A6734-0206-00")]
print  "Av2u testing", Av2u[search_index("A6734-0206-00")][search_index("A6734-0245-00")] 
for i in neighbor:
	for j in neighbor[i]:
		if Au[search_index(i)] != 0:
			probability[search_index(i)][search_index(j)] = Av2u[search_index(i)][search_index(j)] / float(Au[search_index(i)])


print  "probability testing", probability[search_index("A6734-0206-00")][search_index("A6734-0245-00")] 
print search_index("A6734-0206-00")
print search_index("A6734-0245-00")



"""build probability table"""
with open('writing.csv', 'wb') as writer:  
    	w = csv.DictWriter(writer, [""] + neighbor.keys())
    	w.writeheader()
writer = csv.writer(open('writing.csv', 'a'))

for key in  neighbor:
	writer.writerow([key] + probability[search_index(key)])

"""..."""


print "len(areas)=",len(areas), "len(time)=", len(time), "len(neighbor)=", len(neighbor),  "len(match)=", len(match)



"""f1, f2 must close file"""



