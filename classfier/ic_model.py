import gen_features
import classify

import networkx as nx
import operator
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
plt.rc('font', weight='bold')



def main():
    alert_threshold = 5
    tainan = gen_features.City()
    kaohsiung = gen_features.City()


    # tainan
    CityGraphsa0, CityGraphsa1, CityGraphsa2 = gen_features.read_graph_sturcture('Tainan')
    print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))

    gen_features.read_case("Tainan2014", tainan, 2014, CityGraphsa2)
    gen_features.read_case("Tainan2015", tainan, 2015, CityGraphsa2)

    # get data, training and testing
    training, testing = get_data("Tainan2015", tainan, 2015, CityGraphsa2, alert_threshold)
    print(len(training), len(testing))

    # learing
    ic_graph = computing_propagation_rate("Tainan2015", tainan, 2015, CityGraphsa2, training, alert_threshold)
    print("finish train 2015 ic model")


    # predict test:
    testing_week = list(set([t[1] for t in testing]))
    print(testing_week)
    threshold = 0.5
    all_predict_result = {}
    for week in testing_week:
        all_predict_result[week] = predict(tainan, 2015, int(week), ic_graph, threshold)

    ###############
    # # predict: a round decide all area yes or no.
    # # Use testing data to compare predict result
    # alert_threshold = 1
    # # threshold = 0.9
    # for threshold in np.arange(0.05, 0.99, 0.05):
    #     testing_week = list(set([t[1] for t in testing]))
    #     print(testing_week)


    #     all_predict_result = {}
    #     for week in testing_week:
    #         all_predict_result[week] = predict(tainan, 2015, int(week), ic_graph, threshold)

    #     labels = computing_label_for_testing(tainan, 2015, testing, all_predict_result, CityGraphsa2)
        
    #     # evaluate stage
    #     performance = evaluate(labels, testing)
    #     plot = classify.ploting(performance, "IC model, threshod=%f, alertthreshold=%d" %(threshold, alert_threshold))
    #################


    # # Tainan Roc curve 2015(week=32 39 45)
    # print("tainan roc curve:")
    # early = roc_curve(testing, 32, tainan, 2015, ic_graph)    
    # middle = roc_curve(testing, 39, tainan, 2015, ic_graph)
    # later = roc_curve(testing, 45, tainan, 2015, ic_graph)
    # print("plot tainan:")
    # roc_plot(early[0], early[1], middle[0], middle[1], later[0], later[1], "Tainan ROC, eta=%d" %(eta))

    ## Tainan just use last week
    # testing_week = list(set([t[1] for t in testing]))
    # labels = just_use_last_week(tainan, 2015, testing, training)


    ### Tainan's early, middle, later topk(IC model+clf)
    # clf = decision tree



    # clf = classify.ClassifyMethod.normal_decision_tree(training)
    # alpha = 2
    # print("Tainan topk")
    # topk = []
    # # for k in range(5, 51, 5):
    # for k in range(1, 21):
    #     k_precision = topk_precision(tainan, 2015, 39, ic_graph, testing, k, clf, alpha)
    #     print(k_precision)
    #     topk.append(k_precision)
    # print(topk)


    # k_precision = topk_precision(tainan, 2015, 39, ic_graph, testing, 'k=?', clf, alpha)



    ## Kaohsiung ROC
    # CityGraphsa0, CityGraphsa1, CityGraphsa2 = gen_features.read_graph_sturcture('Kaohsiung')
    # print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))

    # gen_features.read_case("Kaohsiung2014", kaohsiung, 2014, CityGraphsa2)
    # gen_features.read_case("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)

    # # get data, training and testing
    # training, testing = get_data("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
    # print(len(training), len(testing))

    # # learing
    # ic_graph = computing_propagation_rate("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2, training, eta)
    # print("finish kaohsiung 2015 ic model")



    ### kaohsiung's early, middle, later topk
    # print("Kaohsiung topk")
    # topk = []
    # # for k in range(5, 51, 5):
    # for k in range(1, 21):
    #     k_precision = topk_precision(kaohsiung, 2015, 48, ic_graph, testing, k)
    #     print(k_precision)
    #     topk.append(k_precision)
    # print(topk)


    # # Kaohsiung Roc curve 2015(week = 40, 46, 48)
    # print("kaohsiung roc curve:")
    # early = roc_curve(testing, 40, kaohsiung, 2015, ic_graph)    
    # middle = roc_curve(testing, 46, kaohsiung, 2015, ic_graph)
    # later = roc_curve(testing, 48, kaohsiung, 2015, ic_graph)
    # print("plot kaohsiung:")
    # roc_plot(early[0], early[1], middle[0], middle[1], later[0], later[1], "Kaohsiung ROC, eta=%d" %(eta))


def get_data(file_name, city, year, graph, alert_threshold):
    with open('../dataset/'+file_name+'_feature-eta'+str(alert_threshold)+'.csv', 'r') as file1, \
         open('../dataset/'+file_name+'_feature(no case)-eta'+str(alert_threshold)+'.csv', 'r') as file2:
            lines = file1.readlines()[1:]+file2.readlines()[1:]
            lines = [line.strip() for line in lines]

            training, testing = classify.split_train_test(lines)
            print("split finish")

            return training, testing  


def computing_propagation_rate(file_name, city, year, graph, training_data, alert_threshold):
    
    # init graph
    n = 0
    ic_graph = nx.DiGraph()
    for area in graph:
        ic_graph.add_node(area, Av=0)
        ic_graph.add_edge(area, area, p=0, Av2u=0)

        for neighbor in graph[area]:
            ic_graph.add_edge(area, neighbor, p=0, Av2u=0)
            n += 1

    # compute probalility-use training data
    print("training data: compute probability")
    # features: "this week no case" is useless
    training_data = [x for x in training_data if int(x[8]) >= alert_threshold]
    for x in training_data:
        x[1] = int(x[1])

    training_data = sorted(training_data, key = operator.itemgetter(1))
    actions = [x[1] for x in training_data]
    actions = Counter(actions)

    current_action_id = 0
    # possible action id is 1,2,3,9,10,11,17,18,19
    # because the multiple of 4, such as 4, it means 4-5 week, but the week 5 is not in training data
    check = 0
    a = 0
    b = 0
    for i in range(len(training_data)):
    # for i in range(300):

        # propagation starter
        if training_data[i][1] % 4 == 0:
            continue
        starter = training_data[i][0]
        current_action_id = training_data[i][1]
        ic_graph.node[starter]['Av'] += 1
        
        # propagation influenced
        for j in range(i+1, len(training_data)):
        # for j in range(i+1, 300):
            receiver = training_data[j][0]
            week = training_data[j][1]
            if week - current_action_id == 1:
                # print(i+1, j+1, "CHECK THE PROPGATAION SUCCESS OR NOT", starter, receiver)
                # check neighbor, p, self, Av2u...
                if receiver in graph[starter]:
                    # print("  pass to neighbor")
                    # ic_graph.edge(starter, receiver)['Av2u'] += 1
                    ic_graph.edge[starter][receiver]['Av2u'] += 1
                elif receiver == starter:
                    # print("  self to self")
                    # ic_graph.edge(starter, starter)['Av2u'] += 1
                    ic_graph.edge[starter][starter]['Av2u'] += 1
            if week - current_action_id >= 2:
                break
    # compute action ratio to get probalility
    probalilitys = []
    for edge in ic_graph.edges():
        v = edge[0]
        u = edge[1]
        try:
            ic_graph.edge[v][u]['p'] = ic_graph.edge[v][u]['Av2u'] / float(ic_graph.node[v]['Av'])
        except ZeroDivisionError:
            pass
        probalilitys.append(ic_graph.edge[v][u]['p'])
    print(Counter(probalilitys))
    Avs = [ic_graph.node[n]['Av'] for n in ic_graph.nodes()]
    # print(Counter(Avs), len(Avs))
    return ic_graph

def predict(city, year, week, ic_graph, threshold):
    # Use week to predict week+1 (next week)

    use = '?'
    if year == 2014:
        use = city.sa2.year2014
    elif year == 2015:
        use = city.sa2.year2015

    predict_result = {}
    for area in ic_graph.nodes():
        probalilitys_on_edges = []
        for v, u, attr in ic_graph.edges(data=True):
            if u == area:
                if v not in use.case:
                    probalilitys_on_edges.append(0)
                elif week in use.case[v]:    
                    probalilitys_on_edges.append(attr['p'])
                else:
                    probalilitys_on_edges.append(0)
        # print(probalilitys_on_edges, area)
        probability = 1
        for p in probalilitys_on_edges:
            probability = probability * (1-p)
        probability = 1 - probability

        if probability >= threshold:
            print(area, week, probability)
        
        if probability >= threshold:
            predict_result[area] = 'yes'
        else:
            predict_result[area] = 'no'
    # print("yes or no", week)
    # print(Counter(predict_result))
    return predict_result

def computing_label_for_testing(city, year, testing_data, all_predict_result, CityGraphsa2):
    labels = []
    print("compute testing data labels:")
    for data in testing_data:

        area = data[0]
        week = data[1]
        truth = data[-1]
        predict = all_predict_result[week][area]
        if predict == 'no':
            predict_label = 'Not a contagious region'
            labels.append(predict_label)
        elif predict == 'yes':
            # both or only self
            if any(all_predict_result[week][neighbor] == 'yes' for neighbor in CityGraphsa2[area]):
                predict_label = 'Both are contagious region'
                labels.append(predict_label)
            else:
                predict_label = 'Only self is contagious region'
                labels.append(predict_label)

        # print(area, week, truth, predict_label)
    return labels

def just_use_last_week(city, year, testing_data, training_data, CityGraphsa2, alert_threshold):
    print("Use the last week to predict LABEL:")
    use = '?'
    if year == 2014:
        use = city.sa2.year2014
    elif year == 2015:
        use = city.sa2.year2015

    labels = []
    total_data = testing_data + training_data
    print(len(total_data))

    testing_week = list(set([t[1] for t in testing_data]))
    for i in testing_data:
        if i[1] in testing_week:
            area = i[0]
            week = int(i[1])
            for find in total_data:
                if find[0] == area and int(find[1]) == week-1:
                    labels.append(find[-1])
                    break
    return labels

def evaluate(predict, testing):
    performance = {}        # label: [precision, recall]
    print("evaluating")
    print(len(testing))

    truth = [i[-1] for i in testing]

    truth_label = Counter(truth)
    predict_label = Counter(predict)
    print("truth/predict label")
    print(truth_label)
    print(predict_label)

    performance = {k: [0, 0, 0] for k in truth_label}       # [#bingo, #truth, #guess]
    print(performance)

    # compute bars for precision/recall
    for i, j in zip(truth, predict):
        if i == j:
            performance[i][0] += 1
        performance[i][1] += 1
        performance[j][2] += 1
    print(performance)
    for key in performance:
        if float(performance[key][2]) == 0:
            precision = -0.1
        else:
            precision = performance[key][0] / float(performance[key][2])
        if float(performance[key][1]) == 0:
            recall = -0.1
        else:
            recall = performance[key][0] / float(performance[key][1])
        performance[key] = (precision, recall)
    # print(performance)
    return performance

def evaluate_overall(predict, testing):
    overall_precision = 0
    overall_recall = 0

    TP = 0
    FP = 0
    FN = 0
    TN = 0
    correct = 0

    truth = [i[-1] for i in testing]
    print(len(truth))

    # compute precision, recall by FPR, TPR
    for i,j in zip(truth, predict):
        # print(i, j)
        if (i == 'Both are contagious region' or i == "Only self is contagious region") and \
        (j == 'Both are contagious region' or j == "Only self is contagious region"):
            TP += 1
            correct += 1
        elif (i == 'Both are contagious region' or i == "Only self is contagious region") and \
        j == "Not a contagious region":
            FN += 1
        elif i == "Not a contagious region" and \
        (j == 'Both are contagious region' or j == "Only self is contagious region"):
            FP += 1
        elif i == "Not a contagious region" and j == "Not a contagious region" :
            TN += 1
            correct += 1
        # print(TP, FN, FP, TN)

    if TP+FP == 0:
        overall_precision = float('NaN')
    else:
        overall_precision = TP/float(TP+FP)
    
    if TP+FN == 0:
        overall_recall = float('NaN')
    else:
        overall_recall = TP/float(TP+FN)

    accuracy = correct/float(len(truth))

    return overall_precision, overall_recall, accuracy


def evaluate_from0_to1(predict, testing, eta):
    print(len(testing), eta)

    truth = [i[-1] for i in testing]
    print(len(truth))
    
    
    # print(predict)

    ## from 0 to 1's recall
    recall = 0
    son = 0
    mom = 0
    
    for t, p in zip(testing, predict):
        
        if int(t[-3]) < eta and \
            (t[-1] == "Both are contagious region" or t[-1] == "Only self is contagious region"):
                mom += 1
                if p == "Both are contagious region" or p == "Only self is contagious region":
                    son += 1

    if mom == 0:
        recall = float('NaN')
    else:
        recall = son/float(mom)
    # print(recall)

    ## from 0 to 1's precision
    precision = 0
    son = 0
    mom = 0

    for t, p in zip(testing, predict):
        if p == "Both are contagious region" or p == "Only self is contagious region":
            mom += 1
            if int(t[-3]) < eta and \
                (t[-1] == "Both are contagious region" or t[-1] == "Only self is contagious region"):
                    son += 1

    if mom == 0:
        precision = float('NaN')
    else:
        precision  = son/float(mom)
    # print(precision)
    return precision, recall



def roc_curve(testing_data, week, city, year, ic_graph):
    print(week)
    testing_data = [t for t in testing_data if int(t[1]) == week]
    # when threshold is min, get point(1, 1)
    FPR = [1]
    TPR = [1]

    for threshold in np.arange(0.05, 0.99, 0.05):
        TP = 0
        FP = 0
        FN = 0
        TN = 0
        print("do a predict by %f and compute FPR, TPR" %(threshold))
        predict_a_week = predict(city, year, week, ic_graph, threshold)
        
        for td in testing_data:
            area = td[0]
            truth_label = td[-1]
            if (truth_label == 'Both are contagious region' or truth_label == 'Only self is contagious region') \
            and predict_a_week[area] == 'yes':
                TP += 1
            elif (truth_label == 'Both are contagious region' or truth_label == 'Only self is contagious region') \
            and predict_a_week[area] == 'no':
                FN += 1
            elif truth_label == 'Not a contagious region' and predict_a_week[area] == 'yes':
                FP += 1
            elif truth_label == 'Not a contagious region' and predict_a_week[area] == 'no':
                TN += 1

        print("TP=%d, FP=%d, FN=%d, TN=%d" %(TP, FP, FN, TN))

        FPR.append(FP / float(FP+TN))
        TPR.append(TP / float(TP+FN))
    # when threshold is max, get point(0, 0)
    FPR.append(0)
    TPR.append(0)

    return FPR, TPR


def topk_precision(city, year, week, ic_graph, testing_data, k, clf, alpha):
    print("choose top k for the contagious region:")
    use = '?'
    if year == 2014:
        use = city.sa2.year2014
    elif year == 2015:
        use = city.sa2.year2015

    testing_data = [t for t in testing_data if int(t[1]) == week]

    ## predict: clf
    clf_result = {}
    areas = [i[0] for i in testing_data]
    predict = [i[2:10] for i in testing_data]
    predict = clf.predict(predict)
    # print(len(areas))
    # print(len(predict))
    for i, j in zip(areas, predict):
        if j == "Not a contagious region":
            clf_result[i] = 0
        elif j == "Both are contagious region" or j == "Only self is contagious region":
            clf_result[i] = alpha
    # print(clf_result)
    # print(len(clf_result))
    
    ## predict: IC model
    predict_result = {}
    for area in ic_graph.nodes():
        probalilitys_on_edges = []
        for v, u, attr in ic_graph.edges(data=True):
            if u == area:
                if v not in use.case:
                    probalilitys_on_edges.append(0)
                elif week in use.case[v]:    
                    probalilitys_on_edges.append(attr['p'])
                else:
                    probalilitys_on_edges.append(0)
        probability = 1
        for p in probalilitys_on_edges:
            probability = probability * (1-p)
        probability = 1 - probability
        
        predict_result[area] = probability

    score = {}
    for i in clf_result:
        if clf_result[i] != 0:
            score[i] = clf_result[i] + predict_result[i]
        else:
            score[i] = predict_result[i]

    # sort_score = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
    choose_topk = dict(sorted(score.iteritems(), key=operator.itemgetter(1), reverse=True)[:k])

    # print(sort_score)
    # while 1:
    #     pass
    # print(choose_topk)
    
    testing_data_label = {}
    for i in testing_data:
        if i[-1] == 'Not a contagious region':
            testing_data_label[i[0]] = 0
        elif i[-1] == 'Both are contagious region' or i[-1] == "Only self is contagious region":
            testing_data_label[i[0]] = 1


    bingo = 0
    for area in choose_topk:
        if testing_data_label[area] == 1:
            bingo += 1

    return bingo/float(len(choose_topk))

    # return precision

def roc_plot(early_fpr, early_tpr, middle_fpr, middle_tpr, later_fpr, later_tpr, title):
    line1, = plt.plot(early_fpr, early_tpr, label='early stage', linewidth=3, linestyle='-')
    line2, = plt.plot(middle_fpr, middle_tpr, label='middle stage', linewidth=3, linestyle=':')
    line3, = plt.plot(later_fpr, later_tpr, label='later stage', linewidth=3, linestyle='-.')

    plt.xlabel('FPR',fontweight='bold')
    plt.ylabel('TPR',fontweight='bold')
    
    plt.legend(loc='lower right', frameon=False)
    plt.savefig('../plot/'+title+'.eps', format='eps', dpi=1200)
    plt.close()
    print(early_fpr)
    print(early_tpr)
    print(middle_fpr)
    print(middle_tpr)
    print(later_fpr)
    print(later_tpr)

if __name__ == '__main__':
    main()