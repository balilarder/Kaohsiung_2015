
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


## global vars
random_sample_rate_NOCASE = 1
eta = 3

def main():
    # get data, mix feature file with "have case" and "no case"
    with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
         open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
            lines = file1.readlines()[1:]+file2.readlines()[1:]
            # lines = file1.readlines()[1:]

            lines = [line.strip() for line in lines]

            print(len(lines))
        
            training, testing = split_train_test(lines)
            print("split finish")
            print(len(training), len(testing))
            
            ########## TRAIN WITH DIFFERENT LABELS
            ## start train-decision tree
            clf_tree = ClassifyMethod.normal_decision_tree(training)

            # experiment: from0 to 1
            evaluate_from0_to1(clf_tree, testing, eta)



            # ## predict and evaluate
            # performance = evaluate(clf_tree, testing)
            # print("draw plot")
            # print(performance)

            # ## plotting
            # plot = ploting(performance, "decision tree")
            # #=======
            # # ## start train-adaboost
            # # ## start train!
            # # clf_adaboost = ClassifyMethod.adaboost_origin(training)

            # # ## predict and evaluate
            # # performance = evaluate(clf_adaboost, testing)
            # # print("draw plot")
            # # print(performance)

            # # ## plotting
            # # plot = ploting(performance, "adaboost")

            # #=======
            # ## start svm
            # ## start train!
            # clf_svm = ClassifyMethod.svm(training)

            # ## predict and evaluate
            # performance = evaluate(clf_svm, testing)
            # print("draw plot")
            # print(performance)

            # ## plotting
            # plot = ploting(performance, "svm")


            # ######### TRAIN WITHOUT DIFFERENT LABELS:
            # ## start train-decision tree
            # clf_tree = ClassifyMethod.normal_decision_tree(training)

            # ## predict and evaluate
            # precision, recall = evaluate_overall(clf_tree, testing)

            # print(precision)
            # print(recall)




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
    print("train:")
    print(counting)
    print("test:")
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
    print("train:")
    # counting = Counter(training_labels)
    # print(counting)
    print(len(training)) 
    return training, testing  


from sklearn import tree                            # decision tree model
from sklearn.ensemble import AdaBoostClassifier     # adaboost
from sklearn.svm import SVC                         # svm
from sklearn.ensemble import RandomForestClassifier # random forest

class ClassifyMethod(object):
    # to train a decision tree
    @ staticmethod
    def normal_decision_tree(training):
        print("normal decision tree")
        # X = [[0, 0], [1, 1]]
        # Y = [0, 1]
        # clf = tree.DecisionTreeClassifier()
        # clf = clf.fit(X, Y)
        X = [i[2:10] for i in training]    
        Y = [i[-1] for i in training]
        clf = tree.DecisionTreeClassifier(max_depth=2)
        clf = clf.fit(X, Y)

        return clf

    @ staticmethod
    def adaboost_origin(training):
        print("adaboost based on decision tree:")
        X = [i[2:10] for i in training]    
        Y = [i[-1] for i in training]
        clf = AdaBoostClassifier()
        clf = clf.fit(X, Y)

        return clf

    @ staticmethod
    def svm(training):
        print("svm base method:")
        X = [i[2:10] for i in training]    
        Y = [i[-1] for i in training]
        clf = SVC()
        clf = clf.fit(X, Y)

        return clf

    @ staticmethod
    def random_forest(training):
        print("random forest method:")
        X = [i[2:10] for i in training]    
        Y = [i[-1] for i in training]
        clf = RandomForestClassifier(max_depth=2)
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
        print("method: decision tree")

    elif isinstance(clf, AdaBoostClassifier):
        print("method: adaboost")
    # else:
    #     print("else")
    #     return

    truth = [i[-1] for i in testing]
    print(len(truth))
    predict = [i[2:10] for i in testing]
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
        # negative means NaN
        if (performance[key][2]) == 0:
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
 
def evaluate_overall(clf, testing):
    ### evaluate the precision and recall without different labels
    ### just care its 0 or 1

    overall_precision = 0
    overall_recall = 0

    TP = 0
    FP = 0
    FN = 0
    TN = 0
    correct = 0

    truth = [i[-1] for i in testing]
    print(len(truth))
    predict = [i[2:10] for i in testing]
    predict = clf.predict(predict)

    

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

def evaluate_from0_to1(clf, testing, eta):
    print(len(testing), eta)

    truth = [i[-1] for i in testing]
    print(len(truth))
    predict = [i[2:10] for i in testing]
    predict = clf.predict(predict)
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

def ploting(precision_recall, title):
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
    plt.title(title)
    plt.xticks(index + bar_width, [i for i in catagory])
    # plt.legend(loc='upper center', bbox_to_anchor=(.7, 1.05),)
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    # plt.show()
    fig.savefig('../plot/'+title+'.eps', format='eps', dpi=1200) # Use fig. here
    print("a plot finish")




    


if __name__ == '__main__':
    main()