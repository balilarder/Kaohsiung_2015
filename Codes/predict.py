"""
* read the graph
* learn the probabiliy when need 
* predict by 12 method with "predictMethod"
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
    print "real is", len(real)
    TP = 0
    FP = 0
    FN = 0
    TN = 0
    print "check week",week
    for k in prediction:
        if (prediction[k] == 1 and real[k] == 1):
            TP += 1
            
        elif(prediction[k] == 1 and real[k] == 0):
            FP += 1
            
        elif (prediction[k] == 0 and real[k] == 1):
            FN += 1
            
        elif (prediction[k] == 0 and real[k] == 0):
            TN += 1
            
    
    # divide 0 error
    if TP + FN == 0:
        print week
 
    FPR = FP / float(FP + TN)
    TPR = TP / float(TP + FN)
    distance = ((FPR - 0) ** 2 + (TPR - 1) ** 2) ** 0.5

    w = csv.writer(out)
    data.extend((FPR, TPR, distance, "", "", ""))
    #w.writerow(data)
    return data

def convert2timeslot(T, p):
    if T == 1:
        w = p
    elif T % 2 != 0:        # odd
        w = p - (T-1)/2
        # bounding
        if w < 0:
            w = 0
        elif w > 53 - (T - 1) - 1:
            w = 53 - (T - 1) - 1
    elif T % 2 == 0:        # even
        begin = T / 2
        end = 52 - begin
        if p >= begin and p <= end:
            w = p - (T / 2 - 1)
        elif p < begin:
            w = 0
        elif p > end:
            w = 53 - (T - 1) - 1
    return w


def OutputROC(filename, const, model, case2015, iteration, situation, T, phase):
    
    open(filename, 'w').close()

    out = open(filename,"r+")
    
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
        w.writerow(["ROCfile","", "", "", "", "", ""] )
    else:
        w.writerow(all_rows[row_index] + ["ROCfile","", "", "" ,"", "", ""] )
        row_index += 1

    # check_week = [37, 45, 51]
    
    for week in phase:

        convert = convert2timeslot(T, week)
        
        if len(all_rows) == 0:
            w.writerow(["The result of " + str(week) + " prediction:","", "", "", "", "", ""] )
            w.writerow(["threshold", "FPR", "TPR", "distance","", "", ""])
        else:
            w.writerow(all_rows[row_index] + ["The result of " + str(week) + " prediction:","", "", "", "", "", ""] )
            row_index += 1
            w.writerow(all_rows[row_index] + ["threshold", "FPR", "TPR", "distance","","", ""])
            row_index += 1

        thresholds_list = range(41)
        for thres in thresholds_list:

            id = phase.index(week)
            print "id =",id

            prediction = iteration(model[id], float(thres) / 40, case2015, convert, const, situation)
            #print "finish once"
            data = []
            #print "thresholds is %f" %(float(thres) / 40)
            data.append(float(thres) / 40)
            analyze(prediction, case2015, convert, out, data, model[id], situation)
            if len(all_rows) == 0:
                w.writerow(data)
            else:
                w.writerow(all_rows[row_index] + data)
                row_index += 1

        w.writerows(["\n"])
        row_index += 1

    out.close()


def baseline(const, model, case2015, method, situation, T, phase, ths):
    print "baseline method"
    accuracy_model = []
    accuracy_simi = []
    for t in phase:
        convert = convert2timeslot(T, t)
        id = phase.index(t)
        prediction = method(model[id], ths, case2015, convert, const, situation)
        # print prediction
        
        # model accuracy, given thres
        acc = accuracy(case2015, prediction, situation, convert)
        accuracy_model.append(acc)

        # baseline accuracy just the last week
        for k in prediction:
            if case2015[k][convert-1][0] >= situation[k]:
                prediction[k] = 1
            elif case2015[k][convert-1][0] < situation[k]:
                prediction[k] = 0
        acc = accuracy(case2015, prediction, situation, convert)
        accuracy_simi.append(acc)
    print accuracy_model
    print accuracy_simi


# compute accuracy for our model and 
# slot is the slot num converted from week
def accuracy(case2015, prediction, situation, slot):
    bingo = 0
    a = 0
    b = 0
    c = 0
    d = 0
    for k in prediction:
        if (case2015[k][slot][0] >= situation[k] and prediction[k] == 1):
            bingo += 1
            a += 1
            # tp
        if (case2015[k][slot][0] < situation[k] and prediction[k] == 0):
            bingo += 1
            b += 1
            # np
        if (case2015[k][slot][0] >= situation[k] and prediction[k] == 0):
            c += 1
        if (case2015[k][slot][0] < situation[k] and prediction[k] == 1):
            d += 1
    # print a,b,c,d
    print bingo
    return a/float(a+c)
    # return bingo/float(len(prediction))
if __name__ == '__main__':

    # do ROC file
    # 1-12 methods
    methods = [predictMethod1, predictMethod2, predictMethod3, predictMethod4,
    predictMethod5, predictMethod6, predictMethod7, predictMethod8,
    predictMethod9, predictMethod10, predictMethod11, predictMethod12]              
    # different-based graph
    graph_pair = [(first_graph, first_case2014, first_case2015, first_situation), 
    (secondary_graph, secondary_case2014, secondary_case2015, secondary_situation)]
    
    

    
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
    


