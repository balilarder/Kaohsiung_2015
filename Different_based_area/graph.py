"""
* The goal is to form different based area with their attributes
* (min, first, secondary)
"""
import sys
import csv
import re
import os.path
import json
from Attribute import *


# A relation between an area and its neighborhoods
class Cell(object):
    def __init__(self):
        self.pv_u_0 = 0
        self.tau = 1
        self.Av2u = 0
        self.credit_a = []
    def __repr__(self):
        return "p is %s" %(self.pv_u_0)
# Information collection of an MinArea
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
def BuildBase(graph):
    # read neighbor file and constructure graph with neighbor link
    deg1 = open('neighbors_1deg.csv', 'r')
    lines_1 = deg1.readlines()

    
    total_areas = len(lines_1)

    for i in range(len(lines_1)):   #use regular expression to remove "  " " and " \n "
        lines_1[i] = re.sub('["\n]','',lines_1[i])


    for i in range(1, total_areas):
        segment1 = lines_1[i].split(",")
        segment1.pop()
        graph[segment1[0]] = AreaInfo() # create an object information of area
        
        
        for j in range(1, len(segment1)):
            graph[segment1[0]].toother[segment1[j]] = Cell()
        
    deg1.close()

def GraphStructure(member, target_graph, table, base):
    # base is the foundation of higher-level graph(supernode)
    # member is a supernode ingredient
    for k in member:
        target_graph[k] = AreaInfo()

    # find all bridge between supernodes
    print len(target_graph)
    for k in target_graph:              
        # for each supernode, has a neighbor list    
        bridge = []
        for m in member[k]:
            for n in base[m].toother:
                if table[n] != k:
                    bridge.append(table[n])
      
        # form a cell
        for b in bridge:
           target_graph[k].toother[b] = Cell()


def BuildBigger(base_graph, graph1, graph2):
    # graph1 is first area
    # graph2 is secondary area
    with open('opendata.json') as data_file:    
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
        
        # collect secondary area's member
        if s not in secondary_member:
            secondary_member[s] = []
            secondary_member[s].append(f)
        else:
            secondary_member[s].append(f)

    # remove duplicate in secondary member
    for k in secondary_member:
        secondary_member[k] = list(set(secondary_member[k]))

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


"""
global work
"""
first_member = {}
secondary_member = {}
base2first_table = {}
base2secondary_table = {}
first2secondary_table = {}

base_graph = {}
first_graph = {}
secondary_graph = {}
BuildBase(base_graph)
BuildBigger(base_graph, first_graph, secondary_graph)
# test
print len(base_graph)
print len(first_member)
print len(secondary_member)

print first_member["A6405-54-006"]
print first_member["A6418-03-010"]

# print graph to file
g1 = open("first-graph.txt", "w")
for k in first_graph:
    print >> g1, "%s:" %k,
    for f in first_graph[k].toother:
        print >> g1, "%s," %f,
    print >> g1
g1.close()
g2 = open("second-graph.txt", "w")
for k in secondary_graph:
    print >> g2, "%s:" %k,
    for f in secondary_graph[k].toother:
        print >> g2, "%s," %f,
    print >> g2
g2.close()

# get attribute table
base_populationTable = read_population()
base_homeTable = read_home()
base_areaTable = read_area()

first_populationTable = BuildAttributeTable(base_populationTable, first_member)
first_homeTable = BuildAttributeTable(base_homeTable, first_member)
first_areaTable = BuildAttributeTable(base_areaTable, first_member)

secondary_populationTable = BuildAttributeTable(first_populationTable, secondary_member)
secondary_homeTable = BuildAttributeTable(first_homeTable, secondary_member)
secondary_areaTable = BuildAttributeTable(first_areaTable, secondary_member)
    