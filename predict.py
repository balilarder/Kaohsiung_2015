"""
* read the graph
* learn the probabiliy when need 
* predcit by 12 method with "predictMethod"
* analyze and output 12 result
"""
import re
import csv
from graph import Cell, AreaInfo, read_data
from predictMethod import *
from ReadGraph import read_graph_MoreEdge, read_graph_Neighbor
from Attribute import *
from Improve import IfImprove

        
"""
compute probabiliy(when assuming p is not constant)
"""
def computeProbability(graph, week_in_2014):
    
    for k in week_in_2014:
        for w in range(52):
            if w <= 50:     # check 2 week after
                if week_in_2014[k][w][0] > 0:   
                    graph[k].Av += 1
                    # check itself
                    if week_in_2014[k][w + 1][0] > 0 or week_in_2014[k][w + 2][0] > 0:
                        graph[k].toitself.Av2u += 1

                    # check its link
                    for n1 in graph[k].toother:
                        if week_in_2014[n1][w + 1][0] > 0 or week_in_2014[n1][w + 2][0] > 0:
                            graph[k].toother[n1].Av2u += 1
            else:           # only check 53th week
                if week_in_2014[k][w][0] > 0:   
                    graph[k].Av += 1
                    # check itself
                    if week_in_2014[k][w + 1][0] > 0:
                        graph[k].toitself.Av2u += 1

                    # check its link
                    for n1 in graph[k].toother:
                        if week_in_2014[n1][w + 1][0] > 0:
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
    

def clearGraph(graph):
    # reset information but remain graph shape
    for k in graph:
        graph[k].Av = 0
        graph[k].toitself.Av2u = 0
        graph[k].toitself.pv_u_0 = 0
        for link in graph[k].toother:
            graph[k].toother[link].Av2u = 0
            graph[k].toother[link].pv_u_0 = 0
def analyze(prediction, week_in_2015, week, out, data, graph):
    real = {}
    for k in prediction:
        if week_in_2015[k][week][0] >= 1:
            real[k] = 1
        else:
            real[k] = 0

    TP = 0
    FP = 0
    FN = 0
    TN = 0

    # neighbor_infected = 0
    # neighbor_notinfected = 0
    # infected = 0
    # notinfected = 0 

    # for k in prediction:
    #   if all(real[x] == 0 for x in list_1_2_deg[k].toother):
    #       neighbor_notinfected += 1
    #   else:
    #       neighbor_infected += 1
    # print neighbor_notinfected + neighbor_infected
    case1 = 0
    case2 = 0
    # compute 2 case when guess wrong
    for k in prediction:
        if (prediction[k] == 1 and real[k] == 1):
            TP += 1
            
        elif(prediction[k] == 1 and real[k] == 0):
            FP += 1
            if not all(real[x] == 0 for x in graph[k].toother):
                case2 += 1
        elif (prediction[k] == 0 and real[k] == 1):
            FN += 1
            if all(real[x] == 0 for x in graph[k].toother):
                case1 += 1
        elif (prediction[k] == 0 and real[k] == 0):
            TN += 1
            
    
    FPR = FP / float(FP + TN)
    TPR = TP / float(TP + FN)
    distance = ((FPR - 0) ** 2 + (TPR - 1) ** 2) ** 0.5
    # if neighbor_notinfected != 0:
    #   case1 = float(infected) / neighbor_notinfected 
    # else:
    #   case1 = 0
    # if neighbor_infected != 0:
    #   case2 = float(notinfected) / neighbor_infected
    # else:
    #   case2 = 0
    case1 = float(case1) / (FP + FN)
    case2 = float(case2) / (FP + FN)
    # print "TP=%d,FP=%d, FN=%d, TN=%d" %(TP, FP, FN, TN)
    # print "The result of week%d. TPR=%f, FPR=%f, distance=%f" %(week, TPR, FPR, distance)

    
    w = csv.writer(out)
    data.extend((FPR, TPR, distance, case1,case2, "", "", ""))
    #w.writerow(data)
    return data
def OutputROC(filename, constant_list, graph, week_in_2015, iteration):
    
    open(name, 'w').close()

    for parameter in constant_list:
        out = open(name,"r+")
        
        w = csv.writer(out)
        r = csv.reader(out)
        
        print "start predict"
        all_rows = []
        row_index = 0
        for rows in r:
            all_rows.append(rows)
        out.seek(0)


        print len(all_rows)
        if len(all_rows) == 0:
            w.writerow(["baseline method, p=" + str(parameter), "","","", "", "", "", "", ""] )
        else:
            w.writerow(all_rows[row_index] + ["baseline method, p=" + str(parameter), "","","", "", "" ,"", "", ""] )
            row_index += 1

        check_week = [37, 45, 51]
        
        for week in check_week:

            if len(all_rows) == 0:
                w.writerow(["The result of " + str(week) + " prediction:", "","","", "", "", "", "", ""] )
                w.writerow(["threshold", "FPR", "TPR", "distance", "case1 rate", "case2 rate","", "", ""])
            else:
                w.writerow(all_rows[row_index] + ["The result of " + str(week) + " prediction:", "","","", "", "", "", "", ""] )
                row_index += 1
                w.writerow(all_rows[row_index] + ["threshold", "FPR", "TPR", "distance","case1 rate","case2 rate","","", ""])
                row_index += 1

            thresholds_list = range(41)
            for thres in thresholds_list:
                prediction = iteration(graph, float(thres) / 40, week_in_2015, week, parameter)
                #print "finish once"
                data = []
                #print "thresholds is %f" %(float(thres) / 40)
                data.append(float(thres) / 40)
                analyze(prediction, week_in_2015, week, out, data, graph)
                if len(all_rows) == 0:
                    w.writerow(data)
                else:
                    w.writerow(all_rows[row_index] + data)
                    row_index += 1

            w.writerows(["\n"])
            row_index += 1

        out.close()

def classifier(cg1, cg2, cg3, cg4, week_in_2014):
    for k in week_in_2014:
        # do somthing...
        w = 0
        while w <= 52:
            if week_in_2014[k][w][0] > 0:
                break
            else:
                w += 1

        if w >= 0 and w <= 37:
            cg1.append(k)
        elif w >= 38 and w <= 45:
            cg2.append(k)
        elif w >= 38 and w <= 52:
            cg3.append(k)
        elif w == 53:
            cg4.append(k)

if __name__ == '__main__':

    # get attribute tables
    populationTable = read_population()
    homeTable = read_home()
    areaTable = read_area()
    
    # read 2 kinds of graph as input
    graph_MoreEdge = {}
    graph_NeighborEdge = {}
    
    read_graph_MoreEdge(graph_MoreEdge)
    read_graph_Neighbor(graph_NeighborEdge)
    # compute moreDegTable, neighborDegTable
    moreDegTable = compute_deg(graph_MoreEdge)
    neighborDegTable = compute_deg(graph_NeighborEdge)

    # read real data to get week in 2014, 2015
    week_in_2014 = {}
    week_in_2015 = {}
    read_data(graph_NeighborEdge, week_in_2014, week_in_2015)
    
    # compute probability for two graphs
    computeProbability(graph_MoreEdge, week_in_2014)
    computeProbability(graph_NeighborEdge, week_in_2014)

    
    # do ROC file
    """
    methods = [predictMethod1, predictMethod2, predictMethod3, predictMethod4,
    predictMethod5, predictMethod6, predictMethod7, predictMethod8,
    predictMethod9, predictMethod10, predictMethod11, predictMethod12]              # 1-12
    graph_kind = [graph_NeighborEdge, graph_MoreEdge]                   # 2 kinds
    
    for g in graph_kind:
        
        for iteration in methods:
            name = "g" + str(graph_kind.index(g) + 1) + " method-" + iteration.__name__[13:] + ".csv"

            # output a file
            const_parameter = [0.5]
            OutputROC(name, const_parameter, g, week_in_2015, iteration)
            
            # clear Av, Av2u, and recalculate probability graph
            clearGraph(g)
            computeProbability(g, week_in_2014)
            print name + " is finish"
    """   
        
    
    # try to observe 
    """
    methods = [predictMethod11]

    check_week = [37, 45, 51]
    const_list = [0.5]
    csvFile = open("attribute file.csv", "w")
    w = csv.writer(csvFile)
    for method in methods:
        for parameter in const_list:
            ImproveResult = {}
            for week in check_week:
                ImproveResult[week] = IfImprove(method, graph_NeighborEdge, graph_MoreEdge, week, week_in_2015,
                    parameter)
            # print ImproveResult[37][0]["A6402-0374-00"], ImproveResult[37][1]["A6402-0374-00"]
            print "improve"
            for k in ImproveResult[37][0]:
                if ImproveResult[37][0][k] > 0:
                    print k, ImproveResult[37][0][k]
            # test an attribute for 3 weeks
            for week in ImproveResult:
                w.writerow(["week = " + str(week)])
                populationTotal = {}
                for k in graph_NeighborEdge:    
                    if k in populationTable:
                        # count with/without improvement time
                        if not(populationTable[k] in populationTotal):
                            populationTotal[populationTable[k]] = [ImproveResult[week][0][k], ImproveResult[week][1][k]]
                        else:
                            
                            populationTotal[populationTable[k]][0] += ImproveResult[week][0][k]
                            populationTotal[populationTable[k]][1] += ImproveResult[week][1][k]
                print "total finish a week"
                print len(populationTotal)
                for key in sorted(populationTotal.iterkeys()):
                    print key, populationTotal[key][0], populationTotal[key][1]
                    w.writerow([key, populationTotal[key][0],populationTotal[key][1]])
                w.writerow(["\n"])

        # do 2 ROC file

        clearGraph(graph_NeighborEdge)
        computeProbability(graph_NeighborEdge, week_in_2014)
        clearGraph(graph_MoreEdge)
        computeProbability(graph_MoreEdge, week_in_2014)
    csvFile.close()
    """

    print "analyze 4 kinds of nodes..."
    # devide nodes into 4 catagories:
    # firstly infected in early, middle, last time, and never
    cg1 = []
    cg2 = []
    cg3 = []
    cg4 = []
    # There total must be 17387
    print len(populationTable), len(homeTable), len(areaTable),\
    len(moreDegTable), len(neighborDegTable)
    print "check correctence"
    print populationTable['A6421-0167-00']
    print homeTable['A6421-0254-00']
    print areaTable['A6427-0083-00']
    print moreDegTable['A6409-0046-00'], moreDegTable['A6405-1215-00']
    print neighborDegTable['A6412-1644-00']

    classifier(cg1, cg2, cg3, cg4, week_in_2014)
    print "after classify"
    print len(cg1), len(cg2), len(cg3), len(cg4)
    # A file show 4 catagories
    catagoryFile = open("catagory.csv", "w")
    w = csv.writer(catagoryFile)
    
    catagory = 1
    for cg in [cg1, cg2, cg3, cg4]:
        w.writerow(["catagory " + str(catagory)])
        w.writerow(["key", "population", "home", "area", "moreDeg", "neighborDeg"])
        for k in cg:
            data = []
            p = ""
            h = ""
            a = ""
            mD = ""
            nD = ""
            if k in populationTable:
                p = populationTable[k]
            if k in homeTable:
                h = homeTable[k]
            if k in areaTable:
                a = areaTable[k]
            if k in moreDegTable:
                mD = moreDegTable[k]
            if k in neighborDegTable:
                nD = neighborDegTable[k]  
            data.extend((k, p, h, a, mD, nD))
            w.writerow(data)
            
        catagory += 1
        w.writerow(["\n"])

    catagoryFile.close()

