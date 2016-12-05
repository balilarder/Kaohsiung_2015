import heapq
import operator
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
def compute_confidence(All_contribution, graph):
    confidence = {}
    ubound = 1000    # if more than upper bound, the confidence is satisfy, that is 1 
    for k in graph:
        sour_des = []
        # a node has a source-destination list contain their #case,
        # based on list total(Av), compute confidence
        sour_des.append(graph[k].Av)
        for n in graph[k].toother:
            sour_des.append(graph[n].Av)
        s = sum(sour_des)

        if s >= ubound:
            confidence[k] = 1
        else:
            confidence[k] = (s / float(ubound)) ** 0.5

    return confidence

def display(d):
    distrubution = {}

    # while True:
    #     pass
    for i in [x/10.0+0.1 for x in range(10)]:
        distrubution[i] = 0


    for k in d:
        for i in [x/10.0+0.1 for x in range(10)]:
            if i >= d[k]:
                distrubution[i] += 1
                break
    print "display", distrubution

def precisionkMethod1(want_k, graph, week_in_2015, 
    week, constant, situation):

    convertToConstant(graph, constant)

    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod2(want_k, graph, week_in_2015, 
    week, constant, situation):
    
    convertToConstant(graph, constant)

    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod3(want_k, graph, week_in_2015, 
    week, constant, situation):
    
    convertToConstant(graph, constant)

    contribution = {}   # Now, contribution is dictionary
    for k in graph:
        contribution[k] = []
    for k in graph:
        
        
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        
    All_contribution = all_contribution(contribution)
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod4(want_k, graph, week_in_2015, 
    week, constant, situation):
    
    convertToConstant(graph, constant)

    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod5(want_k, graph, week_in_2015, 
    week, constant, situation):
    
    # other is constant
    for k in graph:
        for p in graph[k].toother:
            graph[k].toother[p].pv_u_0 = constant

    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod6(want_k, graph, week_in_2015, 
    week, constant, situation):
    
    # self is constant
    for k in graph:
        graph[k].toitself.pv_u_0 = constant

    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod7(want_k, graph, week_in_2015, 
    week, constant, situation):
    
    
    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod8(want_k, graph, week_in_2015, 
    week, constant, situation):
    contribution = {}   # Now, contribution is dictionary
    for k in graph:
        contribution[k] = []
    for k in graph:
        
        
        # other
        if week_in_2015[k][week - 1][0] >= situation[k]:
            for each in graph[k].toother:
                contribution[each].append(graph[k].toother[each].pv_u_0)
        

    All_contribution = all_contribution(contribution)
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod9(want_k, graph, week_in_2015, 
    week, constant, situation):
    
    # other is constant
    for k in graph:
        for p in graph[k].toother:
            graph[k].toother[p].pv_u_0 = constant

    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod10(want_k, graph, week_in_2015, 
    week, constant, situation):
    
    # self is constant
    for k in graph:
        graph[k].toitself.pv_u_0 = constant

    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)

    if want_k == 20:
        print All_contribution
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

def precisionkMethod11(want_k, graph, week_in_2015, 
    week, constant, situation, ifconf, newly):
    
    decay = 1/2.0
    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # display distrubution
    # display(All_contribution)
    # compute really small will not infected?
    a = 0
    b = 0
    for k in All_contribution:
        if All_contribution[k] >= 0 and All_contribution[k] <= 0.1:
            a += 1
            if week_in_2015[k][week][0] < situation[k]:
                b += 1
    print "The invert obsevation is ", b/float(a)
    
    """
    probability*confidence
    """
    if ifconf:
        confidence = compute_confidence(All_contribution, graph)
    else:
        confidence = {}
        for k in graph:
            confidence[k] = 1

    # print confidence

    # The new rank for precision k
    ranking = {}

    for k in All_contribution:
        ranking[k] = All_contribution[k] * confidence[k]

    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, ranking, key=ranking.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in ranking:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del ranking[k]
    # print "len", len(ranking)

    if want_k == 20:
        new = sorted(ranking.items(), key=operator.itemgetter(1), reverse = True)
        i = 1
        for a in new:
            print a[1], All_contribution[a[0]],confidence[a[0]], i
            i += 1
        print

    # compute precision
    if newly == 0:
        really_infect = 0
        for k in ranking:
            if week_in_2015[k][week][0] >= situation[k]:
                really_infect += 1
    else:
        really_infect = 0
        for k in ranking:
            if week_in_2015[k][week][0] >= situation[k] and week_in_2015[k][week-1][0] < situation[k]:
                really_infect += 1

    """
    print 3 values: #infected, #newly infected, #uninfected, print out when k=20
    """
    if want_k == 20:
        inf = 0
        ninf = 0
        uninf = 0
        for k in week_in_2015:
            if week_in_2015[k][week][0] >= situation[k]:
                inf += 1
                if week_in_2015[k][week-1][0] < situation[k]:
                    ninf += 1
            else:
                uninf += 1
        print "inf, ninfm uninf=", inf, ninf, uninf
    # endif

    presicion = (really_infect)/float(want_k)
    return presicion


def precisionkMethod12(want_k, graph, week_in_2015, 
    week, constant, situation):
   
    contribution = {}   # Now, contribution is dictionary
    for k in graph:
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
    
    # precision k 
    k_keys_sorted = heapq.nlargest(want_k, All_contribution, key=All_contribution.get)
    
    delete_list = []    # out of presicion k, don't care
    for k in All_contribution:
        if k not in k_keys_sorted:
            delete_list.append(k)

    for k in delete_list:
        del All_contribution[k]
    # print "len", len(All_contribution)
    
    # compute precision
    really_infect = 0
    for k in All_contribution:
        if week_in_2015[k][week][0] >= situation[k]:
            really_infect += 1


    presicion = (really_infect)/float(want_k)
    return presicion

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

def computeK(T, k, const, model, case_2015, method, situation, period, ifconf, newly):
    precision_list = []
    for p in period:
        # p needs to convert to correspond slot when T>1
        w = convert2timeslot(T, p)
        id = period.index(p)
        precision_list.append(method(k, model[id], case_2015, w, const, situation, ifconf, newly))
        # add a precision to list
    print k
    return precision_list