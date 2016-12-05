"""
compute AUC, efficiency?
"""
import pandas as pd
def computeAUC(filename):
	print "start compute AUC..."
	AUClist = []
	
	df = pd.read_csv(filename)
	# df is a dataframe of pandas, wants two column: "Unnamed: 1" means FPR, and "Unnamed: 2" means TPR
	# to compute AUC
	THRESlist = df["ROCfile"]	# the column of threshold
	FPRlist = df["Unnamed: 1"]
	TPRlist = df["Unnamed: 2"]
	initialLine = [3, 47, 91]
	for line in initialLine:
		# line means early, middle, last time's line in file
		print THRESlist[line], FPRlist[line], TPRlist[line]
		small_area = []
		for time in range(40):
			# compute 40 times small area, finally total them
			small_area.append(((float(TPRlist[line+time-1]))+(float(TPRlist[line+time])))*\
				((float(FPRlist[line+time-1]))-(float(FPRlist[line+time])))/2.0)
		print len(small_area)
		# total small_area is AUC
		total = 0
		for a in small_area:
			total += a
		AUClist.append(total)
	
	return AUClist

if __name__ == '__main__':
	result = computeAUC("method1-g0.csv") 

	