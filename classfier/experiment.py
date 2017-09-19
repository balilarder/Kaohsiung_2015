import gen_features
import classify
import ic_model

alert_threshold_list = range(1, 11)

def main():
    tainan = gen_features.City()
    kaohsiung = gen_features.City()
    global young, middle, old

    """
    isocalender: 
    2014 has 52 week, 2015 has 53 week
    """

    # Tainan -- set alert threshold(classifiers, icmodel, just_use_last_week)
    CityGraphsa0, CityGraphsa1, CityGraphsa2 = gen_features.read_graph_sturcture('Tainan')
    print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))

    # feature of with case
    # gen_features.read_case("Tainan2014", tainan, 2014, CityGraphsa2)
    # gen_features.output_feature_list("Tainan2014", tainan, 2014, CityGraphsa2)
    # print("tainan 2014 finish")

    gen_features.read_case("Tainan2015", tainan, 2015, CityGraphsa2)
    gen_features.output_feature_list("Tainan2015", tainan, 2015, CityGraphsa2)
    print("tainan 2015 finish")

    # feature of "no" case
    # gen_features.output_feature_no_case("Tainan2014", tainan, 2014, CityGraphsa2)
    gen_features.output_feature_no_case("Tainan2015", tainan, 2015, CityGraphsa2)

    for alert_threshold in alert_threshold_list:
        # compute label for 2014, 2015 tainan  
        print(alert_threshold) 
        # gen_features.computing_label('Tainan2014', tainan, 2014, CityGraphsa2, alert_threshold)
        gen_features.computing_label('Tainan2015', tainan, 2015, CityGraphsa2, alert_threshold)

        # feature for "no" case
        print("start computing no case feature")
        # gen_features.computing_label_no_case("Tainan2014", tainan, 2014, CityGraphsa2, alert_threshold)
        # print("2014 finish")
        gen_features.computing_label_no_case("Tainan2015", tainan, 2015, CityGraphsa2, alert_threshold)
        print("2015 finish")

        # ### classify- decision tree
        # with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
        #      open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
        #         lines = file1.readlines()[1:]+file2.readlines()[1:]
        #         # lines = file1.readlines()[1:]

        #         lines = [line.strip() for line in lines]

        #         print(len(lines))
            
        #         training, testing = classify.split_train_test(lines)
                
        #         ## start train-decision tree
        #         clf_tree = classify.ClassifyMethod.normal_decision_tree(training)

        #         ## predict and evaluate
        #         performance = classify.evaluate(clf_tree, testing)
        #         print("draw plot")
        #         print(performance)

        #         ## plotting
        #         plot = classify.ploting(performance, "Tainan decision tree- alert threshold=%d" %(alert_threshold))
        

        # ### classify- svm
        # with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
        #      open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
        #         lines = file1.readlines()[1:]+file2.readlines()[1:]
        #         # lines = file1.readlines()[1:]

        #         lines = [line.strip() for line in lines]

        #         print(len(lines))
            
        #         training, testing = classify.split_train_test(lines)
                
        #         ## start train-svm
        #         clf_svm = classify.ClassifyMethod.svm(training)

        #         ## predict and evaluate
        #         performance = classify.evaluate(clf_svm, testing)
        #         print("draw plot")
        #         print(performance)

        #         ## plotting
        #         plot = classify.ploting(performance, "Tainan svm- alert threshold=%d" %(alert_threshold))

        # ## classify- adaboost
        # with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
        #      open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
        #         lines = file1.readlines()[1:]+file2.readlines()[1:]
        #         # lines = file1.readlines()[1:]

        #         lines = [line.strip() for line in lines]

        #         print(len(lines))
            
        #         training, testing = classify.split_train_test(lines)
                
        #         ## start train-svm
        #         clf_adaboost = classify.ClassifyMethod.adaboost_origin(training)

        #         ## predict and evaluate
        #         performance = classify.evaluate(clf_adaboost, testing)
        #         print("draw plot")
        #         print(performance)

        #         ## plotting
        #         plot = classify.ploting(performance, "Tainan adaboost- alert threshold=%d" %(alert_threshold))


        ## classify- random forest
        with open('../dataset/Tainan2015_feature.csv', 'r') as file1, \
             open('../dataset/Tainan2015_feature(no case).csv', 'r') as file2:
                lines = file1.readlines()[1:]+file2.readlines()[1:]
                # lines = file1.readlines()[1:]

                lines = [line.strip() for line in lines]

                print(len(lines))
            
                training, testing = classify.split_train_test(lines)
                
                ## start train-svm
                clf_randomforest = classify.ClassifyMethod.random_forest(training)

                ## predict and evaluate
                performance = classify.evaluate(clf_randomforest, testing)
                print("draw plot")
                print(performance)

                ## plotting
                plot = classify.ploting(performance, "Tainan random forest- alert threshold=%d" %(alert_threshold))


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

        # ### just use last week:
        # training, testing = ic_model.get_data("Tainan2015", tainan, 2015, CityGraphsa2)
        # testing_week = list(set([t[1] for t in testing]))
        # labels = ic_model.just_use_last_week(tainan, 2015, testing, training, CityGraphsa2, alert_threshold)
        # performance = ic_model.evaluate(labels, testing)
        # plot = classify.ploting(performance, "Tainan just use the last week, alertthreshold=%d" %(alert_threshold))
         
    #########################################################
    ## Kaohsiung -- set alert threshold(classifiers, icmodel)
    # CityGraphsa0, CityGraphsa1, CityGraphsa2 = gen_features.read_graph_sturcture('Kaohsiung')
    # print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))

    # feature with case
    # gen_features.read_case("Kaohsiung2014", kaohsiung, 2014, CityGraphsa2)
    # gen_features.output_feature_list("Kaohsiung2014", kaohsiung, 2014, CityGraphsa2)
    # print("kaohsiung 2014 finish")

    # gen_features.read_case("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
    # gen_features.output_feature_list("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
    # print("Kaohsiung 2015 finish")

    # # feature of "no" case
    # gen_features.output_feature_no_case("Kaohsiung2014", kaohsiung, 2014, CityGraphsa2)
    # gen_features.output_feature_no_case("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)

    # for alert_threshold in alert_threshold_list:
    #     print(alert_threshold) 
    #     gen_features.computing_label('Kaohsiung2014', kaohsiung, 2014, CityGraphsa2, alert_threshold)
    #     gen_features.computing_label('Kaohsiung2015', kaohsiung, 2015, CityGraphsa2, alert_threshold)

    #     # feature for "no" case
    #     print("start computing no case feature")
    #     gen_features.computing_label_no_case("Kaohsiung2014", kaohsiung, 2014, CityGraphsa2, alert_threshold)
    #     print("2014 finish")
    #     gen_features.computing_label_no_case("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2, alert_threshold)
    #     print("2015 finish")

        # ## classify- decision tree
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
        #         performance = classify.evaluate(clf_tree, testing)
        #         print("draw plot")
        #         print(performance)

        #         ## plotting
        #         plot = classify.ploting(performance, "Kaohsiung "+"decision tree- alert threshold=%d" %(alert_threshold))


        ### ic model
        # get data, training and testing
        # training, testing = ic_model.get_data("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2)
        # print(len(training), len(testing))

        # # learing
        # ic_graph = ic_model.computing_propagation_rate("Kaohsiung2015", kaohsiung, 2015, CityGraphsa2, training, alert_threshold)
        # print("finish train 2015 ic model")

        # # predict: a round decide all area yes or no.
        # # Use testing data to compare predict result
        # threshold = 0.5
        # testing_week = list(set([t[1] for t in testing]))

        # all_predict_result = {}
        # for week in testing_week:
        #     all_predict_result[week] = ic_model.predict(kaohsiung, 2015, int(week), ic_graph, threshold)

        # labels = ic_model.computing_label_for_testing(kaohsiung, 2015, testing, all_predict_result, CityGraphsa2)
        # # evaluate stage
        # performance = ic_model.evaluate(labels, testing)
        # plot = classify.ploting(performance, "Kaohsiung IC model, threshod=%f, alertthreshold=%d" %(threshold, alert_threshold))


if __name__ == '__main__':
    main()