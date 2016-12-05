"""
prediction method:12 methods
Each method output a set of prediction result.
A week has 41 threshold, so need to predict 41 times
"""
import heapq
# 36,37 44,45 50,51's 
def convertToConstant(graph, constant):
    # to other
    for k in graph:
        for p in graph[k].toother:
            graph[k].toother[p].pv_u_0 = constant
    # to itself
    for k in graph:
        graph[k].toitself.pv_u_0 = constant

def all_contribution(contribution):
    All_contribution = {}
    for k in contribution:
        expection = 1.0
        for i in contribution[k]:
            expection = expection * (1 - i)
        expection = 1 - expection
        All_contribution[k] = expection

    return All_contribution
def predictResult(prediction, All_contribution, thresholds):
    print "in func", len(All_contribution)


    for k in All_contribution:
        # expection = 1.0
        # for i in contribution[k]:
        #     expection = expection * (1 - i)
        # expection = 1 - expection
        #print expection
        
        if thresholds == 0:     # all infected
            prediction[k] = 1
        elif thresholds == 1:   # all uninfected
            prediction[k] = 0

        else:
            if All_contribution[k] >= thresholds:
                
                prediction[k] = 1
            else:

                prediction[k] = 0


def predictMethod1(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    convertToConstant(graph, constant)

    prediction = {}
    contribution = {}   # Now, contribution is dictionary

    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        # self
        if week_in_2015[k][week - 1][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0 * 0.5)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0 * 0.25)
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)
    
    
    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod2(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    convertToConstant(graph, constant)

    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        # self
        if week_in_2015[k][week - 1][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0)
        
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        


    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod3(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    convertToConstant(graph, constant)

    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        
    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod4(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    convertToConstant(graph, constant)

    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod5(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    # other is constant
    for k in graph:
        for p in graph[k].toother:
            graph[k].toother[p].pv_u_0 = constant

    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        # self
        if week_in_2015[k][week - 1][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0)
        
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        
    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod6(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    # self is constant
    for k in graph:
        graph[k].toitself.pv_u_0 = constant

    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        # self
        if week_in_2015[k][week - 1][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0)
        
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        

    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod7(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        # self
        if week_in_2015[k][week - 1][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0)
        
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        

    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod8(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        

    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod9(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    # other is constant
    for k in graph:
        for p in graph[k].toother:
            graph[k].toother[p].pv_u_0 = constant

    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        # self
        if week_in_2015[k][week - 1][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0 * 0.5)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0 * 0.25)
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod10(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    # self is constant
    for k in graph:
        graph[k].toitself.pv_u_0 = constant

    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        # self
        if week_in_2015[k][week - 1][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0 * 0.5)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0 * 0.25)
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction

def predictMethod11(graph, thresholds, week_in_2015, 
    week, constant, situation):
    
    decay = 1/2.0
    count = 0
    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        
        # self
        if week_in_2015[k][week - 1][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0 * decay)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            contribution[k].append(graph[k].toitself.pv_u_0 * decay * decay)
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * decay)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * decay * decay)

    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction


def predictMethod12(graph, thresholds, week_in_2015, 
    week, constant, situation):
    count = 0
    prediction = {}
    contribution = {}   # Now, contribution is dictionary
    
    for k in graph:
        prediction[k] = "?"
        contribution[k] = []
    for k in graph:
        

        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        if week_in_2015[k][week - 2][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.5)
        if week_in_2015[k][week - 3][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0 * 0.25)

    All_contribution = all_contribution(contribution)
    predictResult(prediction, All_contribution, thresholds)
    return prediction