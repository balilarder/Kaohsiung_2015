"""
find feature that may influence the propagation:
Assume:
	* distance
	* delta time
	* other attribute(population...)?
The severity use contagious length for judgement.
Assume:
	* contagious length
	* infected people? 
	* ...
"""
import json
import csv

def main():
	print("start to find features...")
	read1 = "../tempfiles/pairdistance.json"
	# get distance information
	with open(read1, 'r') as file:
		data_distance = json.load(file)
	print(len(data_distance))


	read = "../tempfiles/K2014Day2ndArea.csv"
	# get intagious day information(2014)
	interval2014 = {}
	with open(read, 'r') as file:
		allrows = csv.reader(file)
		for i, row in enumerate(allrows, 1):
			if i > 1:
			# if i >= 13 and i <= 18:
				# print(row[0])
				interval2014[row[0]] = contagiousInterval(row)
	print(len(interval2014))

	read = "../tempfiles/K2015Day2ndArea.csv"
	# get intagious day information(2015)
	interval2015 = {}
	with open(read, 'r') as file:
		allrows = csv.reader(file)
		for i, row in enumerate(allrows, 1):
			if i > 1:
				# print(row[0])
				interval2015[row[0]] = contagiousInterval(row)
	print(len(interval2015))

	
	# observation relation between distance(1-5) and sustained infection length
	result2014 = feature_distance(data_distance, interval2014)
	print(result2014)

	# write to file
	write = "../tempfiles/daycase-distance.csv"
	with open(write, 'w') as file:
		w = csv.writer(file)
		Title = "observarion in 2014 day case in diff distance when propagation"
		w.writerow([Title])
		header = ["distance", "propagation time", "avg. interval length"]
		w.writerow(header)
		for k in result2014:
			w.writerow([k, result2014[k][0], result2014[k][2]])


	# result2015 = feature_distance(data_distance, interval2015)
	# print(result2015)

def contagiousInterval(alldays):
	# input all days list of an area, return contagious interval
	interval = []
	i = 1
	while i < len(alldays):
		# print(i)
		if alldays[i] == "V":
			# print(i, alldays[i])
			start = end = i
			while alldays[end] == 'V':
				end += 1
				# avoid indexerror
				if end == len(alldays):
					break
			end -= 1
			sustain = end - start + 1
			# print(start,end,sustain)
			interval.append({"start":start,"end":end,"sustain":sustain})
			i += sustain
		else:
			i += 1

	return interval


def feature_distance(data_distance, intervals):
	# assume the specific time that start no later than an interval
	# ex:[_vvvvvvvvv____________]
	#	 [__(________________)_]
	# start in () is valid, toleration parameter after ending
	delta_time_for_end = 10 
	dict = {}	# sustain length, init = 0
	for i in range(6):
		dict[i] = [0, 0, 0]		# (propagation count, length total, avg severity=[1]/[0])
	print(len(intervals))
	test = 0
	for k1 in intervals:
		print(k1)
		print(k1, intervals[k1])
		for interval_src in intervals[k1]:
			# if we seen the interval as source, evaluate its length
			print("source:",interval_src)
			dict[0][0] += 1
			dict[0][1] += interval_src["sustain"]
			print(dict[0])

			for k2 in intervals:
				# check distinct area that make sure influence
				if k2 != k1:
					distance = lookup_distance(k1, k2, data_distance)
					if distance is not None:
						print("distance", distance, k1, k2)
						for interval_dest in intervals[k2]:
							print("need to check",k1, interval_src,k2, interval_dest)
							check = SucceedPropagate(interval_src, interval_dest, delta_time_for_end)
							print("check=",check)
							test += 1
							# succeed propagate:
							if check:
								dict[distance][0] += 1
								dict[distance][1] += interval_dest["sustain"]*check
			print('\n')			
		print(k1,"sur finish")
	print(test)
	for k in dict:
		dict[k][2] = dict[k][1]/float(dict[k][0])
	return dict
def lookup_distance(src, des, pairdistance):
	
	# print("lookup", src, des)
	for i in range(1, 6):
		for element in pairdistance[src][str(i)]:
			# print(element)
			if element == des:
				return i
	# can't find, return None
	return None

def SucceedPropagate(interval_src, interval_dest, epson):
	# Based on when to start, return the factor to time to sustain
	if interval_dest["start"] > interval_src["start"] and \
	interval_dest["start"] <= interval_src["end"]:
		return 1
	# in this case, setting linear decay
	elif interval_dest["start"] > interval_src["end"] and \
	interval_dest["start"] <= interval_src["end"] + epson:
		slope = -1.0 / epson
		return (interval_dest["start"]-interval_src["end"])*slope + 1
	# too late
	else:
		return 0

if __name__ == '__main__':
	main()