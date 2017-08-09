'''
base on sa0 neighbor information and case data, create a table for sa1, sa2
neighbor data
'''

class Level0(object):
    """docstring for Level0"""
    def __init__(self, name):
        super(Level0, self).__init__()
        self.name = name
        self.level1 = ""
        self.level2 = ""

        self.neighbor = []
    def __repr__(self):
        return "name = %s. " %(self.name) +\
                "L1 = %s. " %(self.level1) +\
                "L2 = %s.\n" % (self.level2) +\
                "neighbor = %s." %(list(self.neighbor))
TainanLevel0s = {}
TainanLevel1s = {}
TainanLevel2s = {}

TainanGraphsa1 = {}
TainanGraphsa2 = {}

# read data, neighbor and case data

import pandas as pd
import csv

with open('../dataset/Tainan2014_case.csv', 'r') as case2014,\
    open('../dataset/Tainan2015_case.csv', 'r') as case2015:
        df = pd.read_csv('../dataset/neighbors_1deg(T).csv')
        
        # create the object of area
        data = list(df.itertuples())
        for i in data:
            area = i.codebase.replace(" ", "")
            neighbors = i.neighbors.strip(',')
            neighbors = neighbors.split(',')
            
            TainanLevel0s[area] = Level0(area)
            TainanLevel0s[area].neighbor = neighbors
        # print(TainanLevel0s['A6733-0878-00'])

        count = 0
        data = case2014.readlines()
        for i in data[1:]:
            i = i.split(',')
            sa0, sa1, sa2 = (i[8], i[11], i[12])
            if any(x == "" for x in [sa0, sa1, sa2]):
                continue
            if sa0 in TainanLevel0s:
                
                if sa1 not in TainanLevel1s:
                    TainanLevel1s[sa1] = [sa0]
                else:
                    TainanLevel1s[sa1].append(sa0)

                if sa2 not in TainanLevel2s:
                    TainanLevel2s[sa2] = [sa1]
                else:
                    TainanLevel2s[sa2].append(sa1)


                TainanLevel0s[sa0].level1 = sa1
                TainanLevel0s[sa0].level2 = sa2
        data = case2015.readlines()
        for i in data[1:]:
            i = i.split(',')
            sa0, sa1, sa2 = (i[8], i[11], i[12])
            if any(x == "" for x in [sa0, sa1, sa2]):
                continue
            if sa0 in TainanLevel0s:
                
                if sa1 not in TainanLevel1s:
                    TainanLevel1s[sa1] = [sa0]
                else:
                    TainanLevel1s[sa1].append(sa0)

                if sa2 not in TainanLevel2s:
                    TainanLevel2s[sa2] = [sa1]
                else:
                    TainanLevel2s[sa2].append(sa1)


                TainanLevel0s[sa0].level1 = sa1
                TainanLevel0s[sa0].level2 = sa2

# remove duplicate itmes in dictionary sa1, sa2
for a in TainanLevel1s:
    TainanLevel1s[a] = list(set(TainanLevel1s[a]))
for b in TainanLevel2s:
    TainanLevel2s[b] = list(set(TainanLevel2s[b]))

# sa1 graph
for sa1 in TainanLevel1s:
    TainanGraphsa1[sa1] = []       # edge
    
    for sa0 in TainanLevel1s[sa1]:
        # print(sa0, TainanLevel0s[sa0].neighbor)
        for n in TainanLevel0s[sa0].neighbor:
            if TainanLevel0s[n].level1 != sa1 and TainanLevel0s[n].level1 != "":
                TainanGraphsa1[sa1].append(TainanLevel0s[n].level1)
for a in TainanGraphsa1:
    TainanGraphsa1[a] = list(set(TainanGraphsa1[a]))
# sa2 graph
for sa2 in TainanLevel2s:
    TainanGraphsa2[sa2] = []       # edge
    # print(sa2)
    for sa1 in TainanLevel2s[sa2]:
        # print(sa1)
        for sa0 in TainanLevel1s[sa1]:
            # print(sa0)
            for n in TainanLevel0s[sa0].neighbor:
                # print("---"+str(n))
                if TainanLevel0s[n].level2 != sa2 and TainanLevel0s[n].level2 != "":
                    TainanGraphsa2[sa2].append(TainanLevel0s[n].level2)
for a in TainanGraphsa2:
    TainanGraphsa2[a] = list(set(TainanGraphsa2[a]))

# print sa1, sa2 graph:
print(len(TainanGraphsa1), len(TainanGraphsa2))
with open('../dataset/Tainan_level1_graph.csv', 'w') as f1, \
    open('../dataset/Tainan_level2_graph.csv', 'w') as f2:
    w1 = csv.writer(f1)
    w2 = csv.writer(f2)

    w1.writerow(["level1", "neighbors"])
    for sa1 in TainanGraphsa1:
        data = [sa1, ""]
        for n in TainanGraphsa1[sa1]:
            data[1] = data[1]+n+','
        w1.writerow(data)
    w2.writerow(["level2", "neighbors"])
    for sa2 in TainanGraphsa2:
        data = [sa2, ""]
        for n in TainanGraphsa2[sa2]:
            data[1] = data[1]+n+','
        w2.writerow(data)

