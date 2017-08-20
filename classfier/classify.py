
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


## global vars
random_sample_rate_NOCASE = 0.002


def split_train_test(dataset):
    # out= train and test
    print(len(dataset))
    '''
    split method options:
    1. odd month -> train
       even month -> testing
    2. just split two part by given ratio

    then get the testing data without processing,
    but 'random sampling' the training data with 'no case' label to avoid bias
    '''


    # odd/even month week:
    training = []
    testing = []

    
    import random

    training_labels = []
    testing_labels = []


    odd = range(1,5)+range(9,13)+range(17,21)+range(25,29)+range(33,37)+range(41,45)+range(49,53)
    even = range(5,9)+range(13,17)+range(21,25)+range(29,33)+range(37,41)+range(45,49)
    for data in dataset:
        data = data.split(',')
        if int(data[1]) in odd:
            training.append(data)
            training_labels.append(data[-1])
        elif int(data[1]) in even:
            testing.append(data)
            testing_labels.append(data[-1])

    print(len(training), len(testing))

    ## processing with training data
    
    counting = Counter(training_labels)
    print(counting)
    counting = Counter(testing_labels)
    print(counting)

    training_ = []
    for data in training:
        if data[-1] == "No case":
            r = random.random()
            if r < random_sample_rate_NOCASE:
                training_.append(data)
        else:
            training_.append(data)
    training = training_
    training_labels = [x[-1] for x in training]
    counting = Counter(training_labels)
    print(counting)
    print(len(training)) 
    return training, testing  


from sklearn import tree            # decision tree model

class ClassifyDecisionTree(object):
    # to train a decision tree
    @ staticmethod
    def normal(training):
        print("normal decision tree")
        # X = [[0, 0], [1, 1]]
        # Y = [0, 1]
        # clf = tree.DecisionTreeClassifier()
        # clf = clf.fit(X, Y)
        X = [i[2:25] for i in training]    
        Y = [i[-1] for i in training]
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, Y)

        return clf
    
def evaluate(clf, testing):
    # in=classifer, testing
    # out=precision//recall...
    # a bar chart to show precision/recall for each label in testing data
    performance = {}        # label: [precision, recall]
    print("evaluating")
    print(len(testing))
    # use the property method to predict label
    if isinstance(clf, tree.DecisionTreeClassifier):
        truth = [i[-1] for i in testing]
        print(len(truth))
        predict = [i[2:25] for i in testing]
        predict = clf.predict(predict)

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

def ploting(precision_recall):
    print(precision_recall)
    
    precision = [precision_recall[i][0] for i in precision_recall]
    recall = [precision_recall[i][1] for i in precision_recall]
    catagory = [i for i in precision_recall]
    print(precision, recall)
    print
    print(catagory)

    n_groups = len(catagory)
    

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    # print(index)
    bar_width = 0.2
    opacity = 0.8

    rects1 = plt.bar(index , precision, bar_width,
                 alpha=opacity,
                 color='b',
                 label='precision')
 
    rects2 = plt.bar(index + bar_width, recall, bar_width,
                 alpha=opacity,
                 color='g',
                 label='recall')
    # add value in the bar
    for ii,rect in enumerate(rects1):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%.2f'% (precision[ii]),
                ha='center', va='bottom', color='b', size=15)
    for ii,rect in enumerate(rects2):
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%.2f'% (recall[ii]),
                ha='center', va='bottom', color='g', size=15)

    plt.xlabel('Labels')
    plt.ylabel('precision/recall')
    plt.title('decision tree')
    plt.xticks(index + bar_width, [i for i in catagory])
    plt.legend(loc='upper left')
     
    plt.tight_layout()
    plt.show()


def main():
    with open('Tainan2015_feature.csv', 'r') as file:
        lines = file.readlines()[1:]
        lines = [line.strip() for line in lines]

        training, testing = split_train_test(lines)
        print("split finish")
        print(len(training), len(testing))

        ## start train!
        clf_tree = ClassifyDecisionTree.normal(training)

        ## predict and evaluate
        performance = evaluate(clf_tree, testing)
        print("draw plot")
        print(performance)

        ## plotting
        plot = ploting(performance)

if __name__ == '__main__':
    main()