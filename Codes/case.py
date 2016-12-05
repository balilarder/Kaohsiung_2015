import datetime
import csv

from predict import convert2timeslot

def read_data(graph, base_case2014, base_case2015, T, city):    
    # read case data for base area
    
    if city == "K":
        f2014 = '../inputfiles/Kaohsiung2014_case.csv'
        f2015 = '../inputfiles/Kaohsiung2015_case.csv'
    elif city == "T":
        f2014 = '../inputfiles/Tainan2014_case.csv'
        f2015 = '../inputfiles/Tainan2015_case.csv'

    print "there are %d areas" % len(graph)
    # base_case2014 = area_name: [[week1, level], [week2, level], [week3, level]...]

    for k in graph:
        base_case2014[k] = [[0, 0] for x in range(53)]       #isocalendar may has 53 weeks in a year
        base_case2014[k].append(-1)                          #default not active yet
        
        base_case2015[k] = [[0, 0] for x in range(53)]       #isocalendar may has 53 weeks in a year
        base_case2015[k].append(-1)                          #default not active yet


    #real data for 2014
    import csv
    import re

    print "2014 cases:"
    file = open(f2014, 'r')
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
    file = open(f2015, 'r')
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

    # T is time interval length
    if T > 1:
        # need to modify 2014, 2015case
        temp_2014 = {}
        temp_2015 = {}
        blank = 53 - (T - 1)
        
        for k in graph:
            temp_2014[k] = [[0, 0] for x in range(blank)]                                 
            temp_2015[k] = [[0, 0] for x in range(blank)]       
        # move around time window to accumulate cases
        for k in graph: 
            for i in range(blank):
                start = 0
                end = 0
                # convert interval to week
                start = i
                end = start + (T - 1)
                move_2014 = 0
                move_2015 = 0
                for move in range(start, end + 1):
                    move_2014 += base_case2014[k][move][0]
                    move_2015 += base_case2015[k][move][0]
                temp_2014[k][i][0] = move_2014
                temp_2015[k][i][0] = move_2015

            base_case2014[k] = temp_2014[k]
            base_case2015[k] = temp_2015[k]

def accumulate(base_case2014, base_case2015, level_graph, member, T):
    blank = 53 - (T - 1)
    level_case2014 = {}
    level_case2015 = {}
    for k in level_graph:
        level_case2014[k] = [[0, 0] for x in range(blank)]  
        level_case2015[k] = [[0, 0] for x in range(blank)]
    # accumulate case
    for k in level_case2014:
        for i in range(blank):
            total = 0
            for m in member[k]:
                if m in base_case2014:
                    total += base_case2014[m][i][0]
            level_case2014[k][i][0] = total

    for k in level_case2015:
        for i in range(blank):
            total = 0
            for m in member[k]:
                if m in base_case2015:
                    total += base_case2015[m][i][0]
            level_case2015[k][i][0] = total
    return level_case2014, level_case2015

def output_case(case, fname, T):
    blank = 53 - (T - 1)
    total = 0
    header = [""]
    for i in range(1, blank + 1):
        header.append(str(i))

    file = open(fname,"w")
    w = csv.writer(file)
    w.writerows([header])
    for k in case:
        data = []
        data.append(k)
        for j in range(blank):
            data.append(str(case[k][j][0]))
            total += case[k][j][0]
        w.writerows([data])
    file.close()
    print "total count from csv is %d" %total

def def_situation(case, T):
    blank = 53 - (T - 1)
    # more than average infected people by infected weeks
    situation = {}
    for key in case:
        valid = 0
        total = 0
        for i in range(blank):
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

def computeProbability(graph, case2014, case2015, situation, T, time):
    # based on "time" to learn probability, and need case2015

    blank = 53 - (T - 1)
    s = convert2timeslot(T, time)   # learn 2015 case

    for k in case2014:                  # 2014: learn all
        for w in range(blank - 1):
            if w <= blank - 3:     # check 2 week after
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
    
    print "learn 2015, s=",s
    for k in case2015:                  # 2015: learn some(before predicted time)
        for w in range(s - 1):          # if s=37, just know earlier 36 slots, so learn by 35
            if w <= s - 3:
                if case2015[k][w][0] >= situation[k]:
                    graph[k].Av += 1
                    # check itself
                    if case2015[k][w + 1][0] >= situation[k] or case2015[k][w + 2][0] >= situation[k]:
                        graph[k].toitself.Av2u += 1

                    # check its link
                    for n1 in graph[k].toother:
                        if case2015[n1][w + 1][0] >= situation[n1] or case2015[n1][w + 2][0] >= situation[n1]:
                            graph[k].toother[n1].Av2u += 1


            else:
            # only check last week
                if case2015[k][w][0] >= situation[k]:   
                    graph[k].Av += 1
                    # check itself
                    if case2015[k][w + 1][0] >= situation[k]:
                        graph[k].toitself.Av2u += 1

                    # check its link
                    for n1 in graph[k].toother:
                        if case2015[n1][w + 1][0] >= situation[n1]:
                            graph[k].toother[n1].Av2u += 1  

                            
    """calculate probability by Av2u/Au"""
    # print "calculate probability"

    # to other
    for k in graph:
        for p in graph[k].toother:
            if graph[k].Av != 0:        #avoid dividing zero
                graph[k].toother[p].pv_u_0 = (graph[k].toother[p].Av2u / float(graph[k].Av))
    # to itself
    for k in graph:
        if graph[k].Av != 0:
            graph[k].toitself.pv_u_0 = (graph[k].toitself.Av2u / float(graph[k].Av)) 

def find_p_decay_rate(case2014, case2015, graph, phase, situation):
    avg_decay = {}
    start = phase[0]
    end = phase[1]

    for i in range(start, end):
        avg_decay[i] = []   # will tell influence later then 1, 2 weeks
        later0 = 0
        later1 = 0
        later2 = 0
        print i, i+2
        for k in case2015:
            if case2015[k][i][0] >= situation[k]:

                # check its link in i+1 week: later 0
                for j in graph[k].toother:
                    if case2015[j][i+1][0] >= situation[j]:
                        later0 += 1
                if case2015[k][i+1][0] >= situation[k]:
                    later0 += 1

                # check its link in i+2 week: later 1
                for j in graph[k].toother:
                    if case2015[j][i+2][0] >= situation[j] and case2015[j][i+1][0] < situation[j]:
                        later1 += 1
                if case2015[k][i+2][0] >= situation[k] and case2015[k][i+1][0] < situation[k]:
                    later1 += 1

                # check its link in i+3 week: later 2
                for j in graph[k].toother:
                    if case2015[j][i+3][0] >= situation[j] and case2015[j][i+2][0] < situation[j]\
                    and case2015[j][i+1][0] < situation[j]:
                        later2 += 1
                if case2015[k][i+3][0] >= situation[k] and case2015[k][i+2][0] < situation[k] and case2015[k][i+1][0] < situation[k]:
                    later2 += 1 
        avg_decay[i].append(later0/float(later1))   
        avg_decay[i].append(later1/float(later2)) 
    print avg_decay  

