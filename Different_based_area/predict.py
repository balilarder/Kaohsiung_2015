"""
* read the graph
* learn the probabiliy when need 
* predcit by 12 method with "predictMethod"
* analyze and output 12 result
"""
import re
import csv
from graph import *
from case import *
from predictMethod import *
        
def clearGraph(graph):
    # reset information but remain graph shape
    for k in graph:
        graph[k].Av = 0
        graph[k].toitself.Av2u = 0
        graph[k].toitself.pv_u_0 = 0
        for link in graph[k].toother:
            graph[k].toother[link].Av2u = 0
            graph[k].toother[link].pv_u_0 = 0

def analyze(prediction, case2015, week, out, data, graph, situation):
    real = {}
    for k in prediction:
        if case2015[k][week][0] >= situation[k]:
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
def OutputROC(filename, constant_list, graph, case2015, iteration, situation):
    
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
                prediction = iteration(graph, float(thres) / 40, case2015, week, parameter, situation)
                #print "finish once"
                data = []
                #print "thresholds is %f" %(float(thres) / 40)
                data.append(float(thres) / 40)
                analyze(prediction, case2015, week, out, data, graph, situation)
                if len(all_rows) == 0:
                    w.writerow(data)
                else:
                    w.writerow(all_rows[row_index] + data)
                    row_index += 1

            w.writerows(["\n"])
            row_index += 1

        out.close()


if __name__ == '__main__':

    # do ROC file
    # 1-12 methods
    methods = [predictMethod1, predictMethod2, predictMethod3, predictMethod4,
    predictMethod5, predictMethod6, predictMethod7, predictMethod8,
    predictMethod9, predictMethod10, predictMethod11, predictMethod12]              
    # different-based graph
    graph_pair = [(first_graph, first_case2014, first_case2015, first_situation), 
    (secondary_graph, secondary_case2014, secondary_case2015, secondary_situation)]
    
    

    """
    for g in graph_pair:
        
        for iteration in methods:
            name = "g" + str(graph_pair.index(g) + 1) + " method-" + iteration.__name__[13:] + ".csv"

            # output a file
            const_parameter = [0.5]
            OutputROC(name, const_parameter, g[0], g[2], iteration, g[3])
            
            # clear Av, Av2u, and recalculate probability graph
            clearGraph(g[0])
            computeProbability(g[0], g[1], g[3])
            print name + " is finish"
    """


