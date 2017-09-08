import gen_features
import classify

import networkx as nx
import operator
from collections import Counter


def main():
    tainan = gen_features.City()
    kaohsiung = gen_features.City()

    CityGraphsa0, CityGraphsa1, CityGraphsa2 = gen_features.read_graph_sturcture('Tainan')
    print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))

    gen_features.read_case("Tainan2014", tainan, 2014, CityGraphsa2)
    gen_features.read_case("Tainan2015", tainan, 2015, CityGraphsa2)

    # get data, training and testing
    training, testing = get_data("Tainan2015", tainan, 2015, CityGraphsa2)
    print(len(training), len(testing))

    # learing
    ic_graph = computing_propagation_rate("Tainan2015", tainan, 2015, CityGraphsa2, training)
    print("finish train 2015 ic model")

    # predict: a round decide all area yes or no.
    # Use testing data to compare predict result
    threshold = 0.5
    testing_week = list(set([t[1] for t in testing]))

    all_predict_result = {}
    for week in testing_week:
        all_predict_result[week] = predict(tainan, 2015, int(week), ic_graph, threshold)

    labels = computing_label_for_testing(tainan, 2015, testing, all_predict_result, CityGraphsa2)
    # evaluate stage
    performance = evaluate(labels, testing)
    plot = classify.ploting(performance, "IC model, threshod=%f" %(threshold))


def get_data(file_name, city, year, graph):
    with open('../dataset/'+file_name+'_feature.csv', 'r') as file1, \
         open('../dataset/'+file_name+'_feature(no case).csv', 'r') as file2:
            lines = file1.readlines()[1:]+file2.readlines()[1:]
            lines = [line.strip() for line in lines]

            training, testing = classify.split_train_test(lines)
            print("split finish")

            return training, testing  


def computing_propagation_rate(file_name, city, year, graph, training_data):
    
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
    training_data = [x for x in training_data if x[8] != '0']
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
    # print(Counter(probalilitys))
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
        probability = 1
        for p in probalilitys_on_edges:
            probability = probability * (1-p)
        probability = 1 - probability
        
        if probability > threshold:
            predict_result[area] = 'yes'
        else:
            predict_result[area] = 'no'
    return predict_result

def computing_label_for_testing(city, year, tesing_data, all_predict_result, CityGraphsa2):
    labels = []
    print("compute testing data labels:")
    for data in tesing_data:
        area = data[0]
        week = data[1]
        truth = data[-1]
        predict = all_predict_result[week][area]
        if predict == 'no':
            predict_label = 'No case'
            labels.append(predict_label)
        elif predict == 'yes':
            # both or only self
            if any(all_predict_result[week][neighbor] == 'yes' for neighbor in CityGraphsa2[area]):
                predict_label = 'Both have case'
                labels.append(predict_label)
            else:
                predict_label = 'Only self has case'
                labels.append(predict_label)

        # print(area, week, truth, predict_label)
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
        precision = performance[key][0] / float(performance[key][2])
        recall = performance[key][0] / float(performance[key][1])
        performance[key] = (precision, recall)
    # print(performance)
    return performance
if __name__ == '__main__':
    main()