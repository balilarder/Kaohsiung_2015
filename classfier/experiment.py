import gen_features
import classify
import ic_model

alert_threshold_list = range(1, 11)

def main():
    tainan = gen_features.City()
    kaohsiung = gen_features.City()
    global young, middle, old

    ### overall precision and recall

    

    """
    isocalender: 
    2014 has 52 week, 2015 has 53 week
    """

    # ### Tainan -- set alert threshold(classifiers, icmodel, just_use_last_week)
    precision_decisiontree = []
    recall_decisiontree = []
    accuracy_decisiontree = []
    from0to1_precision_decisiontree = []
    from0to1_recall_decisiontree = []

    precision_svm = []
    recall_svm = []
    accuracy_svm = []
    from0to1_precision_svm = []
    from0to1_recall_svm = []

    precision_adaboost = []
    recall_adaboost = []
    accuracy_adaboost = []
    from0to1_precision_adaboost = []
    from0to1_recall_adaboost = []

    precision_icmodel = []
    recall_icmodel = []
    accuracy_icmodel = []
    from0to1_precision_icmodel = []
    from0to1_recall_icmodel = []

    precision_just = []
    recall_just = []
    accuracy_just = []

    precision_randomforest = []
    recall_randomforest = []
    accuracy_randomforest = []
    from0to1_precision_randomforest = []
    from0to1_recall_ranfomforest = []


    CityGraphsa0, CityGraphsa1, CityGraphsa2 = gen_features.read_graph_sturcture('Tainan')
    print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))

    # # feature of with case
    gen_features.read_case("Tainan2014", tainan, 2014, CityGraphsa2)
    # # gen_features.output_feature_list("Tainan2014", tainan, 2014, CityGraphsa2)
    # # print("tainan 2014 finish")

    gen_features.read_case("Tainan2015", tainan, 2015, CityGraphsa2)
    # gen_features.output_feature_list("Tainan2015", tainan, 2015, CityGraphsa2)
    # print("tainan 2015 finish")

    # # feature of "no" case
    # gen_features.output_feature_no_case("Tainan2014", tainan, 2014, CityGraphsa2)
    # gen_features.output_feature_no_case("Tainan2015", tainan, 2015, CityGraphsa2)

    for alert_threshold in alert_threshold_list:
        # compute label for 2014, 2015 tainan  
        print(alert_threshold) 

    #     ### classify- decision tree
    #     with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
    #          open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
    #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    #             # lines = file1.readlines()[1:]

    #             lines = [line.strip() for line in lines]

    #             print(len(lines))
            
    #             training, testing = classify.split_train_test(lines)
                
    # #     #         ## start train-decision tree
    # #     #         clf_tree = classify.ClassifyMethod.normal_decision_tree(training)

    # #     #         ## predict and evaluate
    # #     #         performance = classify.evaluate(clf_tree, testing)
    # #     #         print("draw plot")
    # #     #         print(performance)

    # #     #         ## plotting
    # #     #         plot = classify.ploting(performance, "Tainan decision tree- alert threshold=%d" %(alert_threshold))

        
    #     ### classify- decision tree- overall, precision, recall
    #     with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
    #          open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
    #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    #             # lines = file1.readlines()[1:]

    #             lines = [line.strip() for line in lines]

    #             print(len(lines))
            
    #             training, testing = classify.split_train_test(lines)
                
    #             ## start train-decision tree
    #             clf_tree = classify.ClassifyMethod.normal_decision_tree(training)

    #             ## predict and evaluate
    #             precision, recall, accuracy = classify.evaluate_overall(clf_tree, testing)

    #             precision_decisiontree.append(precision)
    #             recall_decisiontree.append(recall)
    #             accuracy_decisiontree.append(accuracy)


        ### classify- decision tree- FROM 0 to 1, precision, recall
        with open('../dataset/Tainan2015_feature-eta'+str(alert_threshold)+'.csv', 'r') as file1, \
             open('../dataset/Tainan2015_feature(no case)-eta'+str(alert_threshold)+'.csv', 'r') as file2:
                lines = file1.readlines()[1:]+file2.readlines()[1:]
                # lines = file1.readlines()[1:]

                lines = [line.strip() for line in lines]

                print(len(lines))
            
                training, testing = classify.split_train_test(lines)
                
                ## start train-decision tree
                clf_tree = classify.ClassifyMethod.normal_decision_tree(training)

                ## predict and evaluate
                precision, recall = classify.evaluate_from0_to1(clf_tree, testing, alert_threshold)

                from0to1_precision_decisiontree.append(precision)
                from0to1_recall_decisiontree.append(recall)
        




    # #     # ### classify- svm
    # #     # with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
    # #     #      open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
    # #     #         lines = file1.readlines()[1:]+file2.readlines()[1:]
    # #     #         # lines = file1.readlines()[1:]

    # #     #         lines = [line.strip() for line in lines]

    # #     #         print(len(lines))
            
    # #     #         training, testing = classify.split_train_test(lines)
                
    # #     #         ## start train-svm
    # #     #         clf_svm = classify.ClassifyMethod.svm(training)

    # #     #         ## predict and evaluate
    # #     #         performance = classify.evaluate(clf_svm, testing)
    # #     #         print("draw plot")
    # #     #         print(performance)

    # #     #         ## plotting
    # #     #         plot = classify.ploting(performance, "Tainan svm- alert threshold=%d" %(alert_threshold))

    #     ### classify- svm- overall, precision, recall
    #     with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
    #          open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
    #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    #             # lines = file1.readlines()[1:]

    #             lines = [line.strip() for line in lines]

    #             print(len(lines))
            
    #             training, testing = classify.split_train_test(lines)
                
    #             ## start train-svm
    #             clf_svm = classify.ClassifyMethod.svm(training)

    #             ## predict and evaluate
    #             precision, recall, accuracy = classify.evaluate_overall(clf_svm, testing)
    #             precision_svm.append(precision)
    #             recall_svm.append(recall)
    #             accuracy_svm.append(accuracy)



        ### classify- svm- FROM 0 to 1, precision, recall
        with open('../dataset/Tainan2015_feature-eta'+str(alert_threshold)+'.csv', 'r') as file1, \
             open('../dataset/Tainan2015_feature(no case)-eta'+str(alert_threshold)+'.csv', 'r') as file2:
                lines = file1.readlines()[1:]+file2.readlines()[1:]
                # lines = file1.readlines()[1:]

                lines = [line.strip() for line in lines]

                print(len(lines))
            
                training, testing = classify.split_train_test(lines)
                
                ## start train-svm
                clf_svm = classify.ClassifyMethod.svm(training)

                ## predict and evaluate
                precision, recall = classify.evaluate_from0_to1(clf_svm, testing, alert_threshold)

                from0to1_precision_svm.append(precision)
                from0to1_recall_svm.append(recall)



    # #     # ## classify- adaboost
    # #     # with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
    # #     #      open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
    # #     #         lines = file1.readlines()[1:]+file2.readlines()[1:]
    # #     #         # lines = file1.readlines()[1:]

    # #     #         lines = [line.strip() for line in lines]

    # #     #         print(len(lines))
            
    # #     #         training, testing = classify.split_train_test(lines)
                
    # #     #         ## start train-svm
    # #     #         clf_adaboost = classify.ClassifyMethod.adaboost_origin(training)

    # #     #         ## predict and evaluate
    # #     #         performance = classify.evaluate(clf_adaboost, testing)
    # #     #         print("draw plot")
    # #     #         print(performance)

    # #     #         ## plotting
    # #     #         plot = classify.ploting(performance, "Tainan adaboost- alert threshold=%d" %(alert_threshold))

    #     ##### adaboost -overall
    #     with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
    #          open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
    #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    #             # lines = file1.readlines()[1:]

    #             lines = [line.strip() for line in lines]

    #             print(len(lines))
            
    #             training, testing = classify.split_train_test(lines)
                
    #             ## start train-decision tree
    #             clf_adaboost = classify.ClassifyMethod.adaboost_origin(training)

    #             ## predict and evaluate
    #             precision, recall, accuracy = classify.evaluate_overall(clf_adaboost, testing)

    #             precision_adaboost.append(precision)
    #             recall_adaboost.append(recall)
    #             accuracy_adaboost.append(accuracy)

        ### classify- adaboost- FROM 0 to 1, precision, recall
        with open('../dataset/Tainan2015_feature-eta'+str(alert_threshold)+'.csv', 'r') as file1, \
             open('../dataset/Tainan2015_feature(no case)-eta'+str(alert_threshold)+'.csv', 'r') as file2:
                lines = file1.readlines()[1:]+file2.readlines()[1:]
                # lines = file1.readlines()[1:]

                lines = [line.strip() for line in lines]

                print(len(lines))
            
                training, testing = classify.split_train_test(lines)
                
                ## start train-adaboost
                clf_adaboost = classify.ClassifyMethod.adaboost_origin(training)

                ## predict and evaluate
                precision, recall = classify.evaluate_from0_to1(clf_adaboost, testing, alert_threshold)

                from0to1_precision_adaboost.append(precision)
                from0to1_recall_adaboost.append(recall)

    # #     ## classify- random forest
    # #     with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
    # #          open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
    # #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    # #             # lines = file1.readlines()[1:]

    # #             lines = [line.strip() for line in lines]

    # #             print(len(lines))
            
    # #             training, testing = classify.split_train_test(lines)
                
    # #             ## start train-svm
    # #             clf_randomforest = classify.ClassifyMethod.random_forest(training)

    # #             ## predict and evaluate
    # #             performance = classify.evaluate(clf_randomforest, testing)
    # #             print("draw plot")
    # #             print(performance)

    # #             ## plotting
    # #             plot = classify.ploting(performance, "Tainan random forest- alert threshold=%d" %(alert_threshold))

    #     ## classify- random forest- overall
    #     with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
    #          open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
    #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    #             # lines = file1.readlines()[1:]

    #             lines = [line.strip() for line in lines]

    #             print(len(lines))
            
    #             training, testing = classify.split_train_test(lines)
                
    #             ## start train-svm
    #             clf_randomforest = classify.ClassifyMethod.random_forest(training)

    #             ## predict and evaluate
    #             precision, recall, accuracy = classify.evaluate_overall(clf_randomforest, testing)
    #             precision_randomforest.append(precision)
    #             recall_randomforest.append(recall)
    #             accuracy_randomforest.append(accuracy)

        ### classify- randomforest- FROM 0 to 1, precision, recall
        with open('../dataset/Tainan2015_feature-eta'+str(alert_threshold)+'.csv', 'r') as file1, \
             open('../dataset/Tainan2015_feature(no case)-eta'+str(alert_threshold)+'.csv', 'r') as file2:
                lines = file1.readlines()[1:]+file2.readlines()[1:]
                # lines = file1.readlines()[1:]

                lines = [line.strip() for line in lines]

                print(len(lines))
            
                training, testing = classify.split_train_test(lines)
                
                ## start train-randomforest
                clf_randomforest = classify.ClassifyMethod.random_forest(training)

                ## predict and evaluate
                precision, recall = classify.evaluate_from0_to1(clf_randomforest, testing, alert_threshold)

                from0to1_precision_randomforest.append(precision)
                from0to1_recall_ranfomforest.append(recall)


        # ### ic model
        # # get data, training and testing
        # training, testing = ic_model.get_data("Tainan2015", tainan, 2015, CityGraphsa2)
        # print(len(training), len(testing))

        # # learing
        # ic_graph = ic_model.computing_propagation_rate("Tainan2015", tainan, 2015, CityGraphsa2, training, alert_threshold)
        # print("finish train 2015 ic model")

        # # predict: a round decide all area yes or no.
        # # Use testing data to compare predict result
        # threshold = 0.5
        # testing_week = list(set([t[1] for t in testing]))

        # all_predict_result = {}
        # for week in testing_week:
        #     all_predict_result[week] = ic_model.predict(tainan, 2015, int(week), ic_graph, threshold)

        # labels = ic_model.computing_label_for_testing(tainan, 2015, testing, all_predict_result, CityGraphsa2)
        # # evaluate stage
        # performance = ic_model.evaluate(labels, testing)
        # plot = classify.ploting(performance, "Tainan IC model, threshod=%f, alertthreshold=%d" %(threshold, alert_threshold))



    # #     # ### ic model--- overall precision, recall
    #     # get data, training and testing
    #     training, testing = ic_model.get_data("Tainan2015", tainan, 2015, CityGraphsa2)
    #     print(len(training), len(testing))

    #     # learing
    #     ic_graph = ic_model.computing_propagation_rate("Tainan2015", tainan, 2015, CityGraphsa2, training, alert_threshold)
    #     print("finish train 2015 ic model")

    #     # predict: a round decide all area yes or no.
    #     # Use testing data to compare predict result
    #     threshold = 0.5
    #     testing_week = list(set([t[1] for t in testing]))

    #     all_predict_result = {}
    #     for week in testing_week:
    #         all_predict_result[week] = ic_model.predict(tainan, 2015, int(week), ic_graph, threshold)

    #     labels = ic_model.computing_label_for_testing(tainan, 2015, testing, all_predict_result, CityGraphsa2)
    #     # evaluate stage
    #     precision, recall, accuracy = ic_model.evaluate_overall(labels, testing)
    #     precision_icmodel.append(precision)
    #     recall_icmodel.append(recall)
    #     accuracy_icmodel.append(accuracy)



        # # ### ic model- from0 to 1
        # # get data, training and testing
        # training, testing = ic_model.get_data("Tainan2015", tainan, 2015, CityGraphsa2, alert_threshold)
        # print(len(training), len(testing))

        # # learing
        # ic_graph = ic_model.computing_propagation_rate("Tainan2015", tainan, 2015, CityGraphsa2, training, alert_threshold)
        # print("finish train 2015 ic model")

        # # predict: a round decide all area yes or no.
        # # Use testing data to compare predict result
        # threshold = 0.5
        # testing_week = list(set([t[1] for t in testing]))

        # all_predict_result = {}
        # for week in testing_week:
        #     all_predict_result[week] = ic_model.predict(tainan, 2015, int(week), ic_graph, threshold)

        # labels = ic_model.computing_label_for_testing(tainan, 2015, testing, all_predict_result, CityGraphsa2)
        # precision, recall = ic_model.evaluate_from0_to1(labels, testing, alert_threshold)
        # from0to1_precision_icmodel.append(precision)
        # from0to1_recall_icmodel.append(recall)


    # # evaluate stage
    # performance = ic_model.evaluate(labels, testing)
    # plot = classify.ploting(performance, "Tainan IC model, threshod=%f, alertthreshold=%d" %(threshold, alert_threshold))




    # #     # ### just use last week:
    # #     # training, testing = ic_model.get_data("Tainan2015", tainan, 2015, CityGraphsa2)
    # #     # testing_week = list(set([t[1] for t in testing]))
    # #     # labels = ic_model.just_use_last_week(tainan, 2015, testing, training, CityGraphsa2, alert_threshold)
    # #     # performance = ic_model.evaluate(labels, testing)
    # #     # plot = classify.ploting(performance, "Tainan just use the last week, alertthreshold=%d" %(alert_threshold))
    


    #     # ### just use last week:-- overall precision recall
    #     training, testing = ic_model.get_data("Tainan2015", tainan, 2015, CityGraphsa2)
    #     testing_week = list(set([t[1] for t in testing]))
    #     labels = ic_model.just_use_last_week(tainan, 2015, testing, training, CityGraphsa2, alert_threshold)
    #     precision, recall, accuracy = ic_model.evaluate_overall(labels, testing)
    #     precision_just.append(precision)
    #     recall_just.append(recall)
    #     accuracy_just.append(accuracy)




    print(precision_adaboost)
    print(precision_svm)
    print(precision_randomforest)
    print(precision_decisiontree)
    print(precision_icmodel)
    print(precision_just)
    print
    print(recall_adaboost)
    print(recall_svm)
    print(recall_randomforest)
    print(recall_decisiontree)  
    print(recall_icmodel)
    print(recall_just)
    print
    print(accuracy_adaboost)
    print(accuracy_svm)
    print(accuracy_randomforest)
    print(accuracy_decisiontree)
    print(accuracy_icmodel)
    print(accuracy_just)
    print
    print("from 0 to 1")

    print(from0to1_precision_decisiontree)
    print(from0to1_recall_decisiontree)

    print(from0to1_precision_svm)
    print(from0to1_recall_svm)

    print(from0to1_precision_randomforest)
    print(from0to1_recall_ranfomforest)

    print(from0to1_precision_adaboost)
    print(from0to1_recall_adaboost)

    print(from0to1_precision_icmodel)
    print(from0to1_recall_icmodel)


    

    #########################################################

    # ### Kaohsiung -- set alert threshold(classifiers, icmodel, just_use_last_week)

    # precision_decisiontree = []
    # recall_decisiontree = []
    # accuracy_decisiontree = []

    # precision_svm = []
    # recall_svm = []
    # accuracy_svm = []

    # precision_adaboost = []
    # recall_adaboost = []
    # accuracy_adaboost = []

    # precision_icmodel = []
    # recall_icmodel = []
    # accuracy_icmodel = []

    # precision_just = []
    # recall_just = []
    # accuracy_just = []

    # precision_randomforest = []
    # recall_randomforest = []
    # accuracy_randomforest = []
    # CityGraphsa0, CityGraphsa1, CityGraphsa2 = gen_features.read_graph_sturcture('Kaohsiung')
    # print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))


    # gen_features.read_case("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
    # gen_features.output_feature_list("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
    # print("kaohsiung 2015 finish")

    # # feature of "no" case
    # gen_features.output_feature_no_case("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)

    # for alert_threshold in alert_threshold_list:
    #     print(alert_threshold) 
    #     gen_features.computing_label('Kaohsiung2015', kaohsiung, 2015, CityGraphsa2, alert_threshold)

    #     # feature for "no" case
    #     print("start computing no case feature")
    #     gen_features.computing_label_no_case("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2, alert_threshold)
    #     print("2015 finish")

    #     ### classify- decision tree
    #     with open('../dataset/Kaohsiung2015_feature.csv', 'r') as file1, \
    #          open('../dataset/Kaohsiung2015_feature(no case).csv', 'r') as file2:
    #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    #             # lines = file1.readlines()[1:]

    #             lines = [line.strip() for line in lines]

    #             print(len(lines))
            
    #             training, testing = classify.split_train_test(lines)
                
    #     #         ## start train-decision tree
    #     #         clf_tree = classify.ClassifyMethod.normal_decision_tree(training)

    #     #         ## predict and evaluate
    #     #         performance = classify.evaluate(clf_tree, testing)
    #     #         print("draw plot")
    #     #         print(performance)

    #     #         ## plotting
    #     #         plot = classify.ploting(performance, "Kaohsiung decision tree- alert threshold=%d" %(alert_threshold))


        ## classify- decision tree- overall, precision, recall
        # with open('../dataset/Kaohsiung2015_feature.csv', 'r') as file1, \
        #      open('../dataset/Kaohsiung2015_feature(no case).csv', 'r') as file2:
        #         lines = file1.readlines()[1:]+file2.readlines()[1:]
        #         # lines = file1.readlines()[1:]

        #         lines = [line.strip() for line in lines]

        #         print(len(lines))
            
        #         training, testing = classify.split_train_test(lines)
                
        #         ## start train-decision tree
        #         clf_tree = classify.ClassifyMethod.normal_decision_tree(training)

        #         ## predict and evaluate
        #         precision, recall, accuracy = classify.evaluate_overall(clf_tree, testing)

        #         precision_decisiontree.append(precision)
        #         recall_decisiontree.append(recall)
        #         accuracy_decisiontree.append(accuracy)
        

    #     # ### classify- svm
    #     # with open('../dataset/Kaohsiung2015_feature.csv', 'r') as file1, \
    #     #      open('../dataset/Kaohsiung2015_feature(no case).csv', 'r') as file2:
    #     #         lines = file1.readlines()[1:]+file2.readlines()[1:]
    #     #         # lines = file1.readlines()[1:]

    #     #         lines = [line.strip() for line in lines]

    #     #         print(len(lines))
            
    #     #         training, testing = classify.split_train_test(lines)
                
    #     #         ## start train-svm
    #     #         clf_svm = classify.ClassifyMethod.svm(training)

    #     #         ## predict and evaluate
    #     #         performance = classify.evaluate(clf_svm, testing)
    #     #         print("draw plot")
    #     #         print(performance)

    #     #         ## plotting
    #     #         plot = classify.ploting(performance, "Kaohsiung svm- alert threshold=%d" %(alert_threshold))

    #     ### classify- svm- overall, precision, recall
    #     with open('../dataset/Kaohsiung2015_feature.csv', 'r') as file1, \
    #          open('../dataset/Kaohsiung2015_feature(no case).csv', 'r') as file2:
    #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    #             # lines = file1.readlines()[1:]

    #             lines = [line.strip() for line in lines]

    #             print(len(lines))
            
    #             training, testing = classify.split_train_test(lines)
                
    #             ## start train-svm
    #             clf_svm = classify.ClassifyMethod.svm(training)

    #             ## predict and evaluate
    #             precision, recall, accuracy = classify.evaluate_overall(clf_svm, testing)
    #             precision_svm.append(precision)
    #             recall_svm.append(recall)
    #             accuracy_svm.append(accuracy)





    # #     # ## classify- adaboost
    # #     # with open('../dataset/Kaohsiung2015_feature.csv', 'r') as file1, \
    # #     #      open('../dataset/Kaohsiung2015_feature(no case).csv', 'r') as file2:
    # #     #         lines = file1.readlines()[1:]+file2.readlines()[1:]
    # #     #         # lines = file1.readlines()[1:]

    # #     #         lines = [line.strip() for line in lines]

    # #     #         print(len(lines))
            
    # #     #         training, testing = classify.split_train_test(lines)
                
    # #     #         ## start train-svm
    # #     #         clf_adaboost = classify.ClassifyMethod.adaboost_origin(training)

    # #     #         ## predict and evaluate
    # #     #         performance = classify.evaluate(clf_adaboost, testing)
    # #     #         print("draw plot")
    # #     #         print(performance)

    # #     #         ## plotting
    # #     #         plot = classify.ploting(performance, "Kaohsiung adaboost- alert threshold=%d" %(alert_threshold))


    #     ##### adaboost -overall
    #     with open('../dataset/Kaohsiung2015_feature.csv', 'r') as file1, \
    #          open('../dataset/Kaohsiung2015_feature(no case).csv', 'r') as file2:
    #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    #             # lines = file1.readlines()[1:]

    #             lines = [line.strip() for line in lines]

    #             print(len(lines))
            
    #             training, testing = classify.split_train_test(lines)
                
    #             ## start train-decision tree
    #             clf_adaboost = classify.ClassifyMethod.adaboost_origin(training)

    #             ## predict and evaluate
    #             precision, recall, accuracy = classify.evaluate_overall(clf_adaboost, testing)

    #             precision_adaboost.append(precision)
    #             recall_adaboost.append(recall)
    #             accuracy_adaboost.append(accuracy)



    # #     # ## classify- random forest
    # #     # with open('../dataset/Kaohsiung2015_feature.csv', 'r') as file1, \
    # #     #      open('../dataset/Kaohsiung2015_feature(no case).csv', 'r') as file2:
    # #     #         lines = file1.readlines()[1:]+file2.readlines()[1:]
    # #     #         # lines = file1.readlines()[1:]

    # #     #         lines = [line.strip() for line in lines]

    # #     #         print(len(lines))
            
    # #     #         training, testing = classify.split_train_test(lines)
                
    # #     #         ## start train-svm
    # #     #         clf_randomforest = classify.ClassifyMethod.random_forest(training)

    # #     #         ## predict and evaluate
    # #     #         performance = classify.evaluate(clf_randomforest, testing)
    # #     #         print("draw plot")
    # #     #         print(performance)

    # #     #         ## plotting
    # #     #         plot = classify.ploting(performance, "Kaohsiung random forest- alert threshold=%d" %(alert_threshold))


    #     ## classify- random forest- overall
    #     with open('../dataset/Kaohsiung2015_feature.csv', 'r') as file1, \
    #          open('../dataset/Kaohsiung2015_feature(no case).csv', 'r') as file2:
    #             lines = file1.readlines()[1:]+file2.readlines()[1:]
    #             # lines = file1.readlines()[1:]

    #             lines = [line.strip() for line in lines]

    #             print(len(lines))
            
    #             training, testing = classify.split_train_test(lines)
                
    #             ## start train-svm
    #             clf_randomforest = classify.ClassifyMethod.random_forest(training)

    #             ## predict and evaluate
    #             precision, recall, accuracy = classify.evaluate_overall(clf_randomforest, testing)
    #             precision_randomforest.append(precision)
    #             recall_randomforest.append(recall)
    #             accuracy_randomforest.append(accuracy)



    # #     # ### ic model
    # #     # # get data, training and testing
    # #     # training, testing = ic_model.get_data("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
    # #     # print(len(training), len(testing))

    # #     # # learing
    # #     # ic_graph = ic_model.computing_propagation_rate("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2, training, alert_threshold)
    # #     # print("finish train 2015 ic model")

    # #     # # predict: a round decide all area yes or no.
    # #     # # Use testing data to compare predict result
    # #     # threshold = 0.5
    # #     # testing_week = list(set([t[1] for t in testing]))

    # #     # all_predict_result = {}
    # #     # for week in testing_week:
    # #     #     all_predict_result[week] = ic_model.predict(kaohsiung, 2015, int(week), ic_graph, threshold)

    # #     # labels = ic_model.computing_label_for_testing(kaohsiung, 2015, testing, all_predict_result, CityGraphsa2)
    # #     # # evaluate stage
    # #     # performance = ic_model.evaluate(labels, testing)
    # #     # plot = classify.ploting(performance, "Kaohsiung IC model, threshod=%f, alertthreshold=%d" %(threshold, alert_threshold))



    # #     # ### ic model--- overall precision, recall
    #     # get data, training and testing
    #     training, testing = ic_model.get_data("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
    #     print(len(training), len(testing))

    #     # learing
    #     ic_graph = ic_model.computing_propagation_rate("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2, training, alert_threshold)
    #     print("finish train 2015 ic model")

    #     # predict: a round decide all area yes or no.
    #     # Use testing data to compare predict result
    #     threshold = 0.5
    #     testing_week = list(set([t[1] for t in testing]))

    #     all_predict_result = {}
    #     for week in testing_week:
    #         all_predict_result[week] = ic_model.predict(kaohsiung, 2015, int(week), ic_graph, threshold)

    #     labels = ic_model.computing_label_for_testing(kaohsiung, 2015, testing, all_predict_result, CityGraphsa2)
    #     # evaluate stage
    #     precision, recall, accuracy = ic_model.evaluate_overall(labels, testing)
    #     precision_icmodel.append(precision)
    #     recall_icmodel.append(recall)
    #     accuracy_icmodel.append(accuracy)


    # #     ### just use last week:
    # #     training, testing = ic_model.get_data("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
    # #     testing_week = list(set([t[1] for t in testing]))
    # #     labels = ic_model.just_use_last_week(kaohsiung, 2015, testing, training, CityGraphsa2, alert_threshold)
    # #     performance = ic_model.evaluate(labels, testing)
    # #     plot = classify.ploting(performance, "Kaohsiung just use the last week, alertthreshold=%d" %(alert_threshold))


    #     # ### just use last week:-- overall precision recall
    #     training, testing = ic_model.get_data("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
    #     testing_week = list(set([t[1] for t in testing]))
    #     labels = ic_model.just_use_last_week(kaohsiung, 2015, testing, training, CityGraphsa2, alert_threshold)
    #     precision, recall, accuracy = ic_model.evaluate_overall(labels, testing)
    #     precision_just.append(precision)
    #     recall_just.append(recall)
    #     accuracy_just.append(accuracy)


    # print(precision_adaboost)
    # print(precision_svm)
    # print(precision_randomforest)
    # print(precision_decisiontree)
    # print(precision_icmodel)
    # print(precision_just)
    # print
    # print(recall_adaboost)
    # print(recall_svm)
    # print(recall_randomforest)
    # print(recall_decisiontree)  
    # print(recall_icmodel)
    # print(recall_just)
    # print
    # print(accuracy_adaboost)
    # print(accuracy_svm)
    # print(accuracy_randomforest)
    # print(accuracy_decisiontree)
    # print(accuracy_icmodel)
    # print(accuracy_just)   





if __name__ == '__main__':
    main()