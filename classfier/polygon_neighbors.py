from shapely.geometry import Polygon
import csv
import pandas as pd

'''
Use polygon to find neighbors ot sa0
'''
class Level0(object):
    """docstring for Level0"""
    def __init__(self, sa0, sa1, sa2, shape):
        super(Level0, self).__init__()
        self.level0 = sa0
        self.level1 = sa1
        self.level2 = sa2
        self.polygon = shape

        self.neighbor = []
    def __repr__(self):
        return  "L0 = %s. " %(self.level0) +\
                "L1 = %s. " %(self.level1) +\
                "L2 = %s.\n" % (self.level2) +\
                "neighbor = %s." %(list(self.neighbor))


# reading the json file and form the dict
import json
import pprint

def reading_json_feature_infos(city):
    json1_file = open('../dataset/'+ city +'.json')
    # json1_str = json1_file.read()
    data = json.load(json1_file)
    # pprint.pprint(data['features'][3])
    sa0s = {}
    for area in data['features']:
        # features
        sa0 = area['properties']['CODEBASE']
        sa1 = area['properties']['CODE1']
        sa2 = area['properties']['CODE2']
        shape = area['geometry']['coordinates'][0]
        
        polygon = Polygon(shape)
        # sa0s[sa0] = {'sa1': sa1, 'sa2': sa2, 'polygon': polygon}
        
        CityLevel0s[sa0] = Level0(sa0, sa1, sa2, polygon)
        if sa1 not in CityLevel1s:
            CityLevel1s[sa1] = [sa0]
        else:
            CityLevel1s[sa1].append(sa0)

        if sa2 not in CityLevel2s:
            CityLevel2s[sa2] = [sa1]
        else:
            CityLevel2s[sa2].append(sa1)

    # remove duplicate itmes in dictionary sa1, sa2
    for a in CityLevel1s:
        CityLevel1s[a] = list(set(CityLevel1s[a]))
    for b in CityLevel2s:
        CityLevel2s[b] = list(set(CityLevel2s[b]))

    
def polygon_sa0_neighbor(city):
    # sa0 neighbor graph

    # df = pd.read_csv('../dataset/neighbors_1deg(T).csv')
    
    # create the object of area
    # dictionary = {}
    # data = list(df.itertuples())
    # for i in data:
    #     area = i.codebase.replace(" ", "")
    #     neighbors = i.neighbors.strip(',')
    #     neighbors = neighbors.split(',')
        
    #     dictionary[area] = neighbors


    cnt = 0
    for i in CityLevel0s:
        for j in CityLevel0s:
            if CityLevel0s[i].polygon.touches(CityLevel0s[j].polygon):
                CityLevel0s[i].neighbor.append(j)
        cnt += 1
        print(cnt)
    
    # output to csv
    with open('../dataset/'+ city +'_polygon_sa0_neighbor.csv', 'w') as f:
        w1 = csv.writer(f) 
        w1.writerow(["level0", "neighbors"])
        for sa0 in CityLevel0s:
                data = [sa0, ""]
                for n in CityLevel0s[sa0].neighbor:
                    data[1] = data[1]+n+','
                w1.writerow(data)

def polygon_sa1_neighbor(city):
    # read sa0 graph file to build sa1 graph
    print(CityLevel1s)

    print(len(CityLevel1s))

    df = pd.read_csv('../dataset/'+ city +'_polygon_sa0_neighbor.csv')
    # create the object of area
    data = list(df.itertuples())
    for i in data:
        level0 = i.level0
        if pd.isnull(i.neighbors):
            neighbors = []
        else:
            neighbors = i.neighbors.strip(',')
            neighbors = neighbors.split(',')
            print(level0, neighbors)
        # TainanLevel0s[area] = Level0(area)
        CityLevel0s[level0].neighbor = neighbors



    # sa1 graph
    for sa1 in CityLevel1s:
        CityGraphsa1[sa1] = []       # edge
        
        for sa0 in CityLevel1s[sa1]:
            # print(sa0, TainanLevel0s[sa0].neighbor)
            for n in CityLevel0s[sa0].neighbor:
                if CityLevel0s[n].level1 != sa1 and CityLevel0s[n].level1 != "":
                    CityGraphsa1[sa1].append(CityLevel0s[n].level1)
                    # print("aaa")
    for a in CityGraphsa1:
        CityGraphsa1[a] = list(set(CityGraphsa1[a]))  

    # output to csv
    with open('../dataset/'+ city +'_polygon_sa1_neighbor.csv', 'w') as f:
        w1 = csv.writer(f) 
        w1.writerow(["level1", "neighbors"])
        for sa1 in CityGraphsa1:
                data = [sa1, ""]
                for n in CityGraphsa1[sa1]:
                    data[1] = data[1]+n+','
                w1.writerow(data)  

def polygon_sa2_neighbor(city):
    # read sa0 graph file to build sa1 graph
    print(CityLevel2s)

    print(len(CityLevel2s))

    df = pd.read_csv('../dataset/'+ city +'_polygon_sa0_neighbor.csv')
    # create the object of area
    data = list(df.itertuples())
    for i in data:
        level0 = i.level0
        if pd.isnull(i.neighbors):
            neighbors = []
        else:
            neighbors = i.neighbors.strip(',')
            neighbors = neighbors.split(',')
            print(level0, neighbors)
        # TainanLevel0s[area] = Level0(area)
        CityLevel0s[level0].neighbor = neighbors



    # sa1 graph
    for sa1 in CityLevel1s:
        CityGraphsa1[sa1] = []       # edge
        
        for sa0 in CityLevel1s[sa1]:
            # print(sa0, TainanLevel0s[sa0].neighbor)
            for n in CityLevel0s[sa0].neighbor:
                if CityLevel0s[n].level1 != sa1 and CityLevel0s[n].level1 != "":
                    CityGraphsa1[sa1].append(CityLevel0s[n].level1)
                    # print("aaa")
    for a in CityGraphsa1:
        CityGraphsa1[a] = list(set(CityGraphsa1[a]))  


    # sa2 graph
    for sa2 in CityLevel2s:
        CityGraphsa2[sa2] = []       # edge
        # print(sa2)
        for sa1 in CityLevel2s[sa2]:
            # print(sa1)
            for sa0 in CityLevel1s[sa1]:
                # print(sa0)
                for n in CityLevel0s[sa0].neighbor:
                    # print("---"+str(n))
                    if CityLevel0s[n].level2 != sa2 and CityLevel0s[n].level2 != "":
                        CityGraphsa2[sa2].append(CityLevel0s[n].level2)
    for a in CityGraphsa2:
        CityGraphsa2[a] = list(set(CityGraphsa2[a]))

    # output to csv
    with open('../dataset/'+ city +'_polygon_sa2_neighbor.csv', 'w') as f:
        w1 = csv.writer(f) 
        w1.writerow(["level2", "neighbors"])
        for sa2 in CityGraphsa2:
                data = [sa2, ""]
                for n in CityGraphsa2[sa2]:
                    data[1] = data[1]+n+','
                w1.writerow(data)  

if __name__ == '__main__':
    # sa0 information: objects
    CityLevel0s = {}

    CityLevel1s = {}
    CityLevel2s = {}

    CityGraphsa1 = {}
    CityGraphsa2 = {}

    # reading_json_feature_infos('Tainan')
    # polygon_sa0_neighbor('Tainan')
    # polygon_sa1_neighbor('Tainan')
    # polygon_sa2_neighbor('Tainan')
    # print(len(CityLevel0s), len(CityLevel1s), len(CityGraphsa2))

    reading_json_feature_infos('Kaohsiung')
    # polygon_sa0_neighbor('Kaohsiung')
    polygon_sa1_neighbor('Kaohsiung')
    polygon_sa2_neighbor('Kaohsiung')
    print(len(CityLevel0s), len(CityLevel1s), len(CityGraphsa2))


    # clear data for the next city... 
    CityLevel0s.clear()

    CityLevel1s.clear()
    CityLevel2s.clear()

    CityGraphsa1.clear()
    CityGraphsa2.clear()



