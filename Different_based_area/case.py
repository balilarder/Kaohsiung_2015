"""
* The goal is to get case for nodes,
  then compute probability for links.
"""
from graph import *

import datetime

def read_data(graph, base_case2014, base_case2015):    
    # read case data for base area

    print "there are %d areas" % len(graph)
    # base_case2014 = area_name: [[week1, level], [week2, level], [week3, level]..., active?]

    for k in graph:
        base_case2014[k] = [[0, 0] for x in range(53)]       #isocalendar may has 53 weeks in a year
        base_case2014[k].append(-1)                          #default not active yet
        
        base_case2015[k] = [[0, 0] for x in range(53)]       #isocalendar may has 53 weeks in a year
        base_case2015[k].append(-1)                          #default not active yet


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
            
            if(segment[8] in base_case2014 ):    
                    
                valid_case += 1 

                if tuple[0] == 2014:
                    base_case2014[segment[8]][week - 1][0] += 1
                else:       
                    #although it is 2014, but it seem as 2015
                    base_case2015[segment[8]][week - 1][0] += 1
                
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
            
            if(segment[8] in base_case2015 ):    
                    
                valid_case += 1 

                if tuple[0] == 2015:
                    base_case2015[segment[8]][week - 1][0] += 1
                
    print  "there are %d valid cases" %valid_case
    file.close()

def accumulate(base_case2014, base_case2015, level_graph, member):
    level_case2014 = {}
    level_case2015 = {}
    for k in level_graph:
        level_case2014[k] = [[0, 0] for x in range(53)]  
        level_case2015[k] = [[0, 0] for x in range(53)]
    # accumulate case
    for k in level_case2014:
        for i in range(53):
            total = 0
            for m in member[k]:
                total += base_case2014[m][i][0]
            level_case2014[k][i][0] = total

    for k in level_case2015:
        for i in range(53):
            total = 0
            for m in member[k]:
                total += base_case2015[m][i][0]
            level_case2015[k][i][0] = total
    return level_case2014, level_case2015

def output_case(case, fname):
    total = 0
    header = [""]
    for i in range(1, 54):
        header.append(str(i))

    file = open(fname,"w")
    w = csv.writer(file)
    w.writerows([header])
    for k in case:
        data = []
        data.append(k)
        for j in range(53):
            data.append(str(case[k][j][0]))
            total += case[k][j][0]
        w.writerows([data])
    file.close()
    print "total count from csv is %d" %total

def def_situation(case):
    # more than average infected people by infected weeks
    situation = {}
    for key in case:
        valid = 0
        total = 0
        for i in range(53):
            if case[key][i][0] > 0:
                valid += 1
                total += case[key][i][0]
        if valid == 0:
            # none case, so threshold is inf
            situation[key] = float("inf")
        else:
            # threshold is average
            situation[key] = float(total) / valid
    return situation

def computeProbability(graph, case2014, situation):
    
    for k in case2014:
        for w in range(52):
            if w <= 50:     # check 2 week after
                if case2014[k][w][0] >= situation[k]:   
                    graph[k].Av += 1
                    # check itself
                    if case2014[k][w + 1][0] >= situation[k] or case2014[k][w + 2][0] >= situation[k]:
                        graph[k].toitself.Av2u += 1

                    # check its link
                    for n1 in graph[k].toother:
                        if case2014[n1][w + 1][0] >= situation[n1] or case2014[n1][w + 2][0] >= situation[n1]:
                            graph[k].toother[n1].Av2u += 1
            else:           
            # only check 53th week
                if case2014[k][w][0] >= situation[k]:   
                    graph[k].Av += 1
                    # check itself
                    if case2014[k][w + 1][0] >= situation[k]:
                        graph[k].toitself.Av2u += 1

                    # check its link
                    for n1 in graph[k].toother:
                        if case2014[n1][w + 1][0] >= situation[n1]:
                            graph[k].toother[n1].Av2u += 1
    

    """calculate probability by Av2u/Au"""
    print "calculate probability"
    
    # to other
    for k in graph:
        for p in graph[k].toother:
            if graph[k].Av != 0:        #avoid dividing zero
                graph[k].toother[p].pv_u_0 = graph[k].toother[p].Av2u / float(graph[k].Av)
    # to itself
    for k in graph:
        if graph[k].Av != 0:
            graph[k].toitself.pv_u_0 = graph[k].toitself.Av2u / float(graph[k].Av) 

"""
global work
"""
base_case2014 = {}
base_case2015 = {}
read_data(base_graph, base_case2014, base_case2015)

# compute higher level case accumulation
first_case2014, first_case2015 = accumulate(base_case2014, base_case2015, first_graph, first_member)
secondary_case2014, secondary_case2015 = accumulate(first_case2014, first_case2015, secondary_graph, secondary_member)

# output
output_case(base_case2014, "base_case2014.csv")
output_case(base_case2015, "base_case2015.csv")

output_case(first_case2014, "first_case2014.csv")
output_case(first_case2015, "first_case2015.csv")

output_case(secondary_case2014, "secondary_case2014.csv")
output_case(secondary_case2015, "secondary_case2015.csv")

# define "how many seen as infected -> for first & secondary"
first_situation = def_situation(first_case2014)
secondary_situation = def_situation(secondary_case2014)

# compute probability - for first and secondary
computeProbability(first_graph, first_case2014, first_situation)
computeProbability(secondary_graph, secondary_case2014, secondary_situation)

