"""
* baseline2: not by neignbor, but actually contagion nodes

* This program will output a graph file "Contagiouns graph.txt"
"""
import sys
import csv
import re
import os.path


# A relation between an area and its neighborhoods
class Cell(object):
    def __init__(self):
        self.pv_u_0 = 0
        self.tau = 1
        self.Av2u = 0
        self.credit_a = []
    def __repr__(self):
        return "p is %s" %(self.pv_u_0)
    
# Information collection of an area
class AreaInfo(object):
    def __init__(self):
        self.Av = 0
        self.toother = {}   # ex:{'A6432-0108-00': Cell1, 'A6432-0104-00': Cell2}
        self.toitself = Cell()
    def show(self):
        print self.toother
        
""" 
get a key as all nodes
"""
def getAllNode():
    deg1 = open('neighbors_1deg.csv', 'r')
    lines_1 = deg1.readlines()

    
    total_areas = len(lines_1)
    print total_areas
    
    for i in range(len(lines_1)):   #use regular expression to remove "  " " and " \n "
        lines_1[i] = re.sub('["\n]','',lines_1[i])
        
    list_1_2_deg = {}                       

    for i in range(1, total_areas):
        segment1 = lines_1[i].split(",")
        segment1.pop()
        list_1_2_deg[segment1[0]] = AreaInfo()  # create an object information of area
        
    deg1.close()
    return list_1_2_deg

"""
Read real data in order to find where links are
"""
import datetime
def read_data(list_1_2_deg, week_in_2014, week_in_2015):    
    
    print "there are %d areas" % len(list_1_2_deg)
    # week_in_2014 = area_name: [[week1, level], [week2, level], [week3, level]..., active?]

    for k in list_1_2_deg:
        week_in_2014[k] = [[0, 0] for x in range(53)]       #isocalendar may has 53 weeks in a year
        week_in_2014[k].append(-1)                          #default not active yet
        
        week_in_2015[k] = [[0, 0] for x in range(53)]       #isocalendar may has 53 weeks in a year
        week_in_2015[k].append(-1)                          #default not active yet


    #real data for 2014
    import csv
    import re

    print "2014 cases:"
    file = open('Kaohsiung2014_case.csv', 'r')
    lines = file.readlines()
    for i in range(len(lines)): #use regular expression to remove" \n "
        lines[i] = re.sub('[\n]','',lines[i])
    print "there are %d case" %(len(lines) - 1)
    count = 0

    no_match = 0
    valid_case = 0

    trace = 0

    for i in range(1, len(lines)):
        segment = lines[i].split(",")

        year = 0
        month = 0
        day = 0
        week = 0
        tuple = ()

        year = segment[2].split("/")[0]
        month = segment[2].split("/")[1]
        day = segment[2].split("/")[2]
        tuple = datetime.date(int(year), int(month), int(day)).isocalendar()
        week = tuple[1]
        

        
        if(segment[8] != "" ):
            
            if(segment[8] in week_in_2014 ):    
                    
                valid_case += 1 

                if tuple[0] == 2014:
                    week_in_2014[segment[8]][week - 1][0] += 1
                else:       
                    #although it is 2014, but it seem as 2015
                    week_in_2015[segment[8]][week - 1][0] += 1
                
    print  "there are %d valid cases" %valid_case
    file.close()
    print

    #real data for 2015
    print "2015 cases:"
    file = open('Kaohsiung2015_case.csv', 'r')
    lines = file.readlines()
    for i in range(len(lines)): #use regular expression to remove" \n "
        lines[i] = re.sub('[\n]','',lines[i])
    print "there are %d case" %(len(lines) - 1)
    count = 0

    no_match = 0
    valid_case = 0

    trace = 0

    for i in range(1, len(lines)):
        segment = lines[i].split(",")

        year = 0
        month = 0
        day = 0
        week = 0
        tuple = ()

        year = segment[2].split("/")[0]
        month = segment[2].split("/")[1]
        day = segment[2].split("/")[2]
        tuple = datetime.date(int(year), int(month), int(day)).isocalendar()
        week = tuple[1]
        

        
        if(segment[8] != "" ):
            
            if(segment[8] in week_in_2015 ):    
                    
                valid_case += 1 

                if tuple[0] == 2015:
                    week_in_2015[segment[8]][week - 1][0] += 1
                
    print  "there are %d valid cases" %valid_case
    file.close()

"""
Find link between nodes(if has been contagious once, then has a edge)
"""
def getAllLink(list_1_2_deg, week_in_2014):
    
    
    count = 0
    for k in week_in_2014:
        for w in range(52):
            
            if w <= 50:     # check 2 week after
                if week_in_2014[k][w][0] > 0:   
                    # check all node, and build links
                    for nodes in list_1_2_deg:
                        if nodes != k and (week_in_2014[nodes][w + 1][0] > 0 or week_in_2014[nodes][w + 2][0] > 0):
                            list_1_2_deg[k].toother[nodes] = Cell()
                            #print "%s -> %s" %(k, nodes)

            else:           # only check 53th week
                if week_in_2014[k][w][0] > 0:   
                    # check all node, and build links
                    for nodes in list_1_2_deg:
                        if nodes != k and week_in_2014[nodes][w + 1][0] > 0:
                            list_1_2_deg[k].toother[nodes] = Cell()
                            #print "%s -> %s" %(k, nodes)
        count += 1
        #print count
    print "finish graph~"
    file = open("Contagious graph.txt", "w")
    for k in list_1_2_deg:
        print >> file, "%s:" %k,
        for nodes in list_1_2_deg[k].toother:
            print >> file, "%s," %nodes,
        print >> file
    # print len(list_1_2_deg["A6430-0017-00"].toother)
    # print len(list_1_2_deg["A6434-0043-00"].toother)
    # print len(list_1_2_deg["A6412-0723-00"].toother)
    # print len(list_1_2_deg["A6405-0201-00"].toother)
    print len(list_1_2_deg["A6405-1215-00"].toother)


if __name__ == "__main__":
    
    list_1_2_deg = getAllNode()

    week_in_2014 = {}
    week_in_2015 = {}
    read_data(list_1_2_deg, week_in_2014, week_in_2015)
    
    want_to_predict = [37, 45, 51]
    getAllLink(list_1_2_deg, week_in_2014)