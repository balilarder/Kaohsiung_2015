
id = []
probability_list = []
def debug (i):
	print id[i]
	print probability_list[i]
f1 = open("check.txt", 'r')
lines = f1.readlines()
#slicing string to from neibors
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
	 		#print j

print probability_list
print count	



f1.close()