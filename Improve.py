from predictMethod import *



def IfImprove(method, graph1, graph2, week, week_in_2015, parameter):
    
    # method is a fuction to predictMethod
    catagory1 = {}  # with improvement
    catagory2 = {}  # without improvement
    for k in week_in_2015:
        catagory1[k] = 0
        catagory2[k] = 0
    
    thresholds_list = range(41)
    for thres in thresholds_list:
        # call a method for graph 1, get result1
        result1 = method(graph1, float(thres) / 40, week_in_2015, week, parameter)

        # call a method for graph 2, get result2
        result2 = method(graph2, float(thres) / 40, week_in_2015, week, parameter)
        
        # compare result1, result2 with real(check every node)
        for k in week_in_2015:
            if (result1[k] == 0 and result2[k] == 1 and week_in_2015[k] >= 1) or \
                (result1[k] == 1 and result2[k] == 0 and week_in_2015[k] == 0):
                # the case with improvement
                catagory1[k] += 1
            else:
                # the case without improvement
                catagory2[k] += 1
    return (catagory1, catagory2)           
