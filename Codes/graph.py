import sys
import csv
import re
import os.path
import json

from attribute import *
from case import convert2timeslot


# A relation between an area and its neighborhoods
class Cell(object):         # inner
    def __init__(self):
        self.pv_u_0 = 0
        self.tau = 1
        self.Av2u = 0
        self.credit_a = []
    def __repr__(self):
        return "p is %s" %(self.pv_u_0)
# Information collection of an MinArea
class AreaInfo(object):     # outer
    def __init__(self):
        self.Av = 0
        self.toother = {}   # ex:{'A6432-0108-00': Cell1, 'A6432-0104-00': Cell2}
        self.toitself = Cell()
    def show(self):
        print self.toother
        
""" 
get a key as all nodes
"""
def BuildBase(graph, city):
    # read neighbor file and constructure graph with neighbor link
    if city == "K":
        filename = "neighbors_1deg(K).csv"
    elif city == "T":
        filename = "neighbors_1deg(T).csv"
    deg1 = open(filename, 'r')
    lines_1 = deg1.readlines()

    
    total_areas = len(lines_1)

    for i in range(len(lines_1)):   #use regular expression to remove "  " " and " \n "
        lines_1[i] = re.sub('["\n]','',lines_1[i])


    for i in range(1, total_areas):
        segment1 = lines_1[i].split(",")
        segment1.pop()

        graph[segment1[0].strip()] = AreaInfo() # create an object information of area
        
        if i == 10 or i == 11:
            print segment1
        
        for j in range(1, len(segment1)):
            graph[segment1[0].strip()].toother[segment1[j]] = Cell()
        
    deg1.close()

def GraphStructure(member, target_graph, table, base):
    # base is the foundation of higher-level graph(supernode)
    # member is a supernode ingredient

    print "graph strucure"
    for k in member:
        target_graph[k] = AreaInfo()

    # find all bridge between supernodes
    print len(target_graph)
    for k in target_graph:              
        # for each supernode, has a neighbor list    
        bridge = []

        for m in member[k]:
            if m in base:                   # if can find in base graph
                for n in base[m].toother:
                    if n in table:          # if can find in table to larger
                        if table[n] != k:
                            bridge.append(table[n])
      
        # form a cell
        for b in bridge:
           target_graph[k].toother[b] = Cell()


def BuildBigger(base_graph, graph1, graph2, base2first_table, base2secondary_table,
    first2secondary_table, first_member, secondary_member, city):
    # graph1 is first area
    # graph2 is secondary area
    if city == "K":
        fn = "Kaohsiung.json"
    elif city == "T":
        fn = "Tainan.json"

    with open(fn) as data_file:    
        data = json.load(data_file)

    print len(data["features"])
    for i in range(len(data["features"])):
        base = str(data["features"][i]["properties"]["CODEBASE"])
        f = str(data["features"][i]["properties"]["CODE1"])
        s = str(data["features"][i]["properties"]["CODE2"])
        
        base2first_table[base] = f
        base2secondary_table[base] = s
        first2secondary_table[f] = s

        # collect first area's member
        if f not in first_member:
            first_member[f] = []
            first_member[f].append(base)
        elif f in first_member:
            first_member[f].append(base)
        
        # print len(base_graph), len(base2first_table)
        # collect secondary area's member
        if s not in secondary_member:
            secondary_member[s] = []
            secondary_member[s].append(f)
        else:
            secondary_member[s].append(f)



  
    # remove duplicate in secondary member
    for k in secondary_member:
        secondary_member[k] = list(set(secondary_member[k]))

    print len(first_member), len(secondary_member), len(base2first_table), len(first2secondary_table), len(base2secondary_table)

    # graph structure(links)
    # NOTE THAT: first graph use base to find link, second graph use first graph, so as table parameter
    
    GraphStructure(first_member, graph1, base2first_table, base_graph )
    print "graph1 finish"
    GraphStructure(secondary_member, graph2, first2secondary_table, graph1)        
    print "grpah2 finish"
    

    return(graph1, graph2)

def BuildAttributeTable(attribute, member):
    # "attribute" is given base's attribute table
    # "member" is first or secondary area member
    table = {}
    for k in member:
        total = 0
        for m in member[k]:
            # look up attribute table
            if m in attribute:
                total += attribute[m]
        table[k] = total
    return table
# build more edge graph

def MEgraph(origin, case2014, case2015, T, situation):
    # input orogin graph
    new_graph = {}
    for k in origin:
        new_graph[k] = AreaInfo()
    
    blank = 53 - (T - 1)
    
    c = 0
    l = 0
    for k in case2014:             # 2014: learn all
        # c += 1
        # print c
        for w in range(blank - 1):
            if w <= blank - 3:     # check 2 week after
                if case2014[k][w][0] >= situation[k]:   
                    new_graph[k].Av += 1
                    # check itself
                    if case2014[k][w + 1][0] >= situation[k] or case2014[k][w + 2][0] >= situation[k]:
                        new_graph[k].toitself.Av2u += 1
                    # check others
                    for nodes in origin:
                        if nodes != k:
                            if (case2014[nodes][w + 1][0] > situation[nodes] 
                                or case2014[nodes][w + 2][0] > situation[nodes]):
                                # create link if "there is not link from k-nodes"
                                if nodes not in new_graph[k].toother:
                                    new_graph[k].toother[nodes] = Cell()
                                    # new_graph[k].toother[nodes].Av2u = 1
                                    l += 1
                                # else:
                                    # new_graph[k].toother[nodes].Av2u += 1

                    # graph[k].Av += 1
                    # # check itself
                    # if case2014[k][w + 1][0] >= situation[k] or case2014[k][w + 2][0] >= situation[k]:
                    #     graph[k].toitself.Av2u += 1

                    # # check its link
                    # for n1 in graph[k].toother:
                    #     if case2014[n1][w + 1][0] >= situation[n1] or case2014[n1][w + 2][0] >= situation[n1]:
                    #         graph[k].toother[n1].Av2u += 1
            


            else:           
            # only check 53th week
                if case2014[k][w][0] >= situation[k]:   
                    new_graph[k].Av += 1
                    # check itself
                    if case2014[k][w + 1][0] >= situation[k]:
                        new_graph[k].toitself.Av2u += 1
                    # check others
                    for nodes in origin:
                        if nodes != k:
                            if case2014[nodes][w + 1][0] > situation[nodes]:
                                # create link if "there is not link from k-nodes"
                                if nodes not in new_graph[k].toother:
                                    new_graph[k].toother[nodes] = Cell()
                                    # new_graph[k].toother[nodes].Av2u = 1
                                    l += 1
                                # else:
                                    # new_graph[k].toother[nodes].Av2u += 1

                        # create link if "there is not link from k-nodes"
                        # if nodes not in new_graph[k].toother:
                        #     if nodes != k and (case2014[nodes][w + 1][0] > situation[nodes]):
                        #         new_graph[k].toother[nodes] = Cell()
                                # l += 1
                    # graph[k].Av += 1
                    # # check itself
                    # if case2014[k][w + 1][0] >= situation[k]:
                    #     graph[k].toitself.Av2u += 1

                    # # check its link
                    # for n1 in graph[k].toother:
                    #     if case2014[n1][w + 1][0] >= situation[n1]:
                    #         graph[k].toother[n1].Av2u += 1
            # print l
    print "2014 ME graph"
    print l
   
    # # print "learn 2015, s=",s
    # for k in case2015:                  # 2015: learn some(before predicted time)
    #     for w in range(s - 1):          # if s=37, just know earlier 36 slots, so learn by 35
    #         if w <= s - 3:
    #             if case2015[k][w][0] >= situation[k]:
    #                 new_graph[k].Av += 1
    #                 # check itself
    #                 if case2015[k][w + 1][0] >= situation[k] or case2015[k][w + 2][0] >= situation[k]:
    #                     new_graph[k].toitself.Av2u += 1

    #                 # check others
    #                 for nodes in origin:
    #                     if nodes != k:
    #                         if (case2015[nodes][w + 1][0] > situation[nodes] 
    #                             or case2015[nodes][w + 2][0] > situation[nodes]):
    #                             # create link if "there is not link from k-nodes"
    #                             if nodes not in new_graph[k].toother:
    #                                 new_graph[k].toother[nodes] = Cell()
    #                                 new_graph[k].toother[nodes].Av2u = 1
    #                                 l += 1
    #                             else:
    #                                 new_graph[k].toother[nodes].Av2u += 1

                    
    #                 # for nodes in origin:
    #                 #     # create link if "there is not link from k-nodes"
    #                 #     if nodes not in new_graph[k].toother:
    #                 #         if nodes != k and (case2015[nodes][w + 1][0] > situation[nodes] 
    #                 #             or case2015[nodes][w + 2][0] > situation[nodes]):
    #                 #             new_graph[k].toother[nodes] = Cell()
    #                 # graph[k].Av += 1
    #                 # # check itself
    #                 # if case2015[k][w + 1][0] >= situation[k] or case2015[k][w + 2][0] >= situation[k]:
    #                 #     graph[k].toitself.Av2u += 1

    #                 # check its link
    #                 # for n1 in graph[k].toother:
    #                 #     if case2015[n1][w + 1][0] >= situation[n1] or case2015[n1][w + 2][0] >= situation[n1]:
    #                 #         graph[k].toother[n1].Av2u += 1


    #         else:
    #         # only check last week
    #             if case2015[k][w][0] >= situation[k]:   
    #                 new_graph[k].Av += 1
    #                 # check itself
    #                 if case2015[k][w + 1][0] >= situation[k]:
    #                     new_graph[k].toitself.Av2u += 1
    #                 # check others
    #                 for nodes in origin:
    #                     if nodes != k:
    #                         if case2015[nodes][w + 1][0] > situation[nodes]:
    #                             # create link if "there is not link from k-nodes"
    #                             if nodes not in new_graph[k].toother:
    #                                 new_graph[k].toother[nodes] = Cell()
    #                                 new_graph[k].toother[nodes].Av2u = 1
    #                                 l += 1
    #                             else:
    #                                 new_graph[k].toother[nodes].Av2u += 1

    #         # # only check last week
    #         #     if case2015[k][w][0] >= situation[k]:   
    #         #         for nodes in origin:
    #         #             # create link if "there is not link from k-nodes"
    #         #             if nodes not in new_graph[k].toother:
    #         #                 if nodes != k and (case2015[nodes][w + 1][0] > situation[nodes]):
    #         #                     new_graph[k].toother[nodes] = Cell()
    #                 # graph[k].Av += 1
    #                 # # check itself
    #                 # if case2015[k][w + 1][0] >= situation[k]:
    #                 #     graph[k].toitself.Av2u += 1

    #                 # # check its link
    #                 # for n1 in graph[k].toother:
    #                 #     if case2015[n1][w + 1][0] >= situation[n1]:
    #                 #         graph[k].toother[n1].Av2u += 1  
    # print "2015 ME graph"
    # print l

                     
    # """calculate probability by Av2u/Au"""
    # # print "calculate probability"

    # # to other
    # for k in new_graph:
    #     for p in new_graph[k].toother:
    #         if new_graph[k].Av != 0:        #avoid dividing zero
    #             new_graph[k].toother[p].pv_u_0 = (new_graph[k].toother[p].Av2u / float(new_graph[k].Av))
    # # to itself
    # for k in new_graph:
    #     if new_graph[k].Av != 0:
    #         new_graph[k].toitself.pv_u_0 = (new_graph[k].toitself.Av2u / float(new_graph[k].Av)) 
    return new_graph