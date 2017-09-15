'''
process the data (case.csv -> feature.csv)
'''

import datetime
import csv
import pandas as pd
import sys

class City(object):
    """docstring for City"""
    # counting case
    sa0 = {}
    sa1 = {}
    class sa2(object):
        class year2014(object):
            area = {}
            counting = 0
            case = {}
        class year2015(object):
            area = {}
            counting = 0
            case = {}

alert_threshold_list = range(1, 4)       # decide a week has case or Not a contagious region
young = ['5-9', '2', '10-14']
middle = ['50-54', '55-59', '35-39', '15-19', '25-29', '30-34', '40-44', '45-49',
          '20-24']
old = ['70+', '65-69', '60-64']

def main():

    
    tainan = City()
    kaohsiung = City()

    CityGraphsa0, CityGraphsa1, CityGraphsa2 = read_graph_sturcture('Tainan')
    global young, middle, old



    print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))
    
    # feature of with case
    """
    isocalender: 
    2014 has 52 week, 2015 has 53 week
    """
    read_case("Tainan2014", tainan, 2014, CityGraphsa2)
    output_feature_list("Tainan2014", tainan, 2014, CityGraphsa2)
    print("tainan 2014 finish")

    read_case("Tainan2015", tainan, 2015, CityGraphsa2)
    output_feature_list("Tainan2015", tainan, 2015, CityGraphsa2)
    print("tainan 2015 finish")

    # feature of "no" case
    output_feature_no_case("Tainan2014", tainan, 2014, CityGraphsa2)
    output_feature_no_case("Tainan2015", tainan, 2015, CityGraphsa2)


    # compute label for 2014, 2015 tainan   
    computing_label('Tainan2014', tainan, 2014, CityGraphsa2, 1)
    computing_label('Tainan2015', tainan, 2015, CityGraphsa2, 1)

    # feature for "no" case
    print("start computing Not a contagious region feature")
    computing_label_no_case("Tainan2014", tainan, 2014, CityGraphsa2)
    print("2014 finish")
    computing_label_no_case("Tainan2015", tainan, 2015, CityGraphsa2)
    print("2015 finish")
def read_graph_sturcture(city):

    CityGraphsa0 = {}
    CityGraphsa1 = {}
    CityGraphsa2 = {}
    for graph, level in zip([CityGraphsa0, CityGraphsa1, CityGraphsa2],
                            ['sa0', 'sa1', 'sa2']):
        df = pd.read_csv('../dataset/'+ city +'_polygon_'+ level +'_neighbor.csv')
        # create the object of area
        data = list(df.itertuples())
        
        for i in data:
            area = i[1]
            if pd.isnull(i[2]):
                neighbors = []
            else:
                neighbors = i[2].strip(',')
                neighbors = neighbors.split(',')
            # print(area, neighbors)
            # TainanLevel0s[area] = Level0(area)
            graph[area] = neighbors

    return CityGraphsa0, CityGraphsa1, CityGraphsa2

def read_case(file_name, city, year, CityGraphsa2):
    # Use city.sa2.year2014 or sity.sa2.year2015
    use = '?'
    if year == 2014:
        use = city.sa2.year2014
    elif year == 2015:
        use = city.sa2.year2015

    
    i = 0    
    # read case file
    with open('../dataset/'+file_name+'_case.csv', 'r') as f:
        # form each week(nodes)
        r = f.readlines()
        the_last_date = map(int, r[-1].rstrip().split(',')[2].split('/'))
        w = datetime.date(the_last_date[0], the_last_date[1], the_last_date[2]).isocalendar()[1]
        # scan the case and build the case tree, and get the area set    
        for case in r[1:]:
            segment = case.split(',')
            # find the sa2 of the case (if it has sa2)
            sa2 = segment[12]
            if sa2 != "" and sa2 in CityGraphsa2:
                i += 1
                date = map(int, segment[2].split('/'))
                week = datetime.date(date[0], date[1], date[2]).isocalendar()[1]

                d1 = map(int, segment[0].split('/'))
                d1 = datetime.date(d1[0], d1[1], d1[2])
                d2 = map(int, segment[1].split('/'))
                d2 = datetime.date(d2[0], d2[1], d2[2])

                delay = (d2-d1).days
                data = {'delay': delay, 'gender': segment[3], 'age': segment[4], 'day': segment[2]}
                # the first case in the area
                if sa2 not in use.area:
                    use.area[sa2] = 1
                    use.case[sa2] = {week: [data]}

                else:
                    use.area[sa2] += 1
                    
                    # city.sa2.case[sa2][week].append(data)
                    if week not in use.case[sa2]:
                        use.case[sa2][week] = [data]
                    else:
                        use.case[sa2][week].append(data)

def output_feature_list(file_name, city, year, CityGraphsa2):
    # Use city.sa2.year2014 or sity.sa2.year2015
    use = '?'
    if year == 2014:
        use = city.sa2.year2014
    elif year == 2015:
        use = city.sa2.year2015

    # output feature file
    with open('../dataset/'+file_name+'_feature.csv', 'w') as f:
        w = csv.writer(f)
        title = ['area', 'week', 'male', 'female', 'delay(avg)', 'young', 'middle', 'old', 'total', 'neighbor-total', 'result_label']
        w.writerow(title)
        # each area, each week data
        for area in use.case:
            for week in use.case[area]:

                if week >= 53:
                    continue
                
                data = {x:0 for x in title}

                data['area'] = area
                data['week'] = week
                data['result_label'] = 'x'
                data['total'] = len(use.case[area][week])    

                # check neighbor-total:
                neighbor_total = 0
                # print(area)
                if area in CityGraphsa2:
                    for neighbor in CityGraphsa2[area]:
                        print(neighbor, week)
                        if neighbor in use.case: 
                            if week in use.case[neighbor]:
                                print(week, len(use.case[neighbor][week])) 
                                neighbor_total += len(use.case[neighbor][week])     
                # print(neighbor_total)
                # print
                data['neighbor-total'] = neighbor_total
                
                # check gender, age, delay
                total_delay_avg = 0
                for case in use.case[area][week]:
                    # check gender
                    if case['gender'] == '\xe7\x94\xb7':
                        data['male'] += 1
                    else:
                        data['female'] += 1
                    # check age
                    if case['age'] in young:
                        data['young'] += 1
                    elif case['age'] in middle:
                        data['middle'] += 1
                    elif case['age'] in old:
                        data['old'] += 1
                    # check delay
                    total_delay_avg += case['delay']

                data['delay(avg)'] = total_delay_avg / float(len(use.case[area][week]))

                row = [data['area'], data['week'], data['male'], data['female'], data['delay(avg)'], data['young'], data['middle'], 
                       data['old'], data['total'], data['neighbor-total'], data['result_label']]
                w.writerow(row)


    print("A feature output finish")

def output_feature_no_case(file_name, city, year, CityGraphsa2):
    """
    output a feature file of "this week without case"
    """
    # Use city.sa2.year2014 or sity.sa2.year2015
    use = '?'
    if year == 2014:
        use = city.sa2.year2014
    elif year == 2015:
        use = city.sa2.year2015

    # output feature file
    print("Not a contagious region feature file")
    with open('../dataset/'+file_name+'_feature(no case).csv', 'w') as f:
        w = csv.writer(f)
        # title = ['area', 'week', 'neighbor-total', 'result_label']
        title = ['area', 'week', 'male', 'female', 'delay(avg)', 'young', 'middle', 'old', 'total', 'neighbor-total', 'result_label']

        w.writerow(title)

        # where and when has Not a contagious region?
        for area in CityGraphsa2:
            for i in range(1, 53):
                if area in use.case:
                    if i not in use.case[area]:
                        data = {x:0 for x in title}

                        data['area'] = area
                        data['week'] = i
                        data['result_label'] = 'x'

                        # check neighbor-total:
                        neighbor_total = 0
                        print(area)
                        if area in CityGraphsa2:
                            for neighbor in CityGraphsa2[area]:
                                print(neighbor, i)
                                if neighbor in use.case: 
                                    if i in use.case[neighbor]:
                                        print(i, len(use.case[neighbor][i])) 
                                        neighbor_total += len(use.case[neighbor][i])     
                        print(neighbor_total)
                        print
                        data['neighbor-total'] = neighbor_total

                        # row = [data['area'], data['week']]
                        row = [data['area'], data['week'], data['male'], data['female'], data['delay(avg)'], data['young'], data['middle'], 
                               data['old'], data['total'], data['neighbor-total'], data['result_label']]
                        w.writerow(row)

                else:       # has Not a contagious region in a whole year
                    data = {x:0 for x in title}

                    data['area'] = area
                    data['week'] = i
                    data['result_label'] = 'x'

                    # check neighbor-total:
                    neighbor_total = 0
                    print(area)
                    if area in CityGraphsa2:
                        for neighbor in CityGraphsa2[area]:
                            print(neighbor, i)
                            if neighbor in use.case: 
                                if i in use.case[neighbor]:
                                    print(i, len(use.case[neighbor][i])) 
                                    neighbor_total += len(use.case[neighbor][i])     
                    print(neighbor_total)
                    print
                    data['neighbor-total'] = neighbor_total

                    # row = [data['area'], data['week']]
                    row = [data['area'], data['week'], data['male'], data['female'], data['delay(avg)'], data['young'], data['middle'], 
                           data['old'], data['total'], data['neighbor-total'], data['result_label']]
                    w.writerow(row)

def computing_label(feature_file_name, city, year, CityGraphsa2, alert_threshold):
    import pandas as pd

    use = '?'
    if year == 2014:
        use = city.sa2.year2014
    elif year == 2015:
        use = city.sa2.year2015

    df = pd.read_csv('../dataset/'+feature_file_name+'_feature.csv')
    # print(df.ix[3][0])
    row, col = (df.shape[0], df.shape[1])
    
    # define labels
    yes = 0                         # next week has case
    yes_self_yes_neighbor = 0       # next week has AND its neighbor has one
    no = 0                          # next week no
    no_self_yes_neighbor = 0        # next week no BUT its neighbor has

    for i in range(row):
        ### compute the label
        a, w = (df.iloc[i]['area'], df.iloc[i]['week'])
        label = "?"

        if a in CityGraphsa2:
            neighbors = CityGraphsa2[a]
        else:
            neighbors = []
            
        # next week: self
        if w == 52 and year == 2014:        # the case check 2015 first week!
            print("check 2015 first week!!")
            if a in city.sa2.year2015.case:
                if 1 in city.sa2.year2015.case[a]:
                    if len(city.sa2.year2015.case[a][1]) >= alert_threshold:
                        label = "Only self is contagious region"
                        yes += 1
                        # check neighbor
                        neighbors = [n for n in neighbors if n in city.sa2.year2015.case]
                        # if any(1 in city.sa2.year2015.case[n] for n in neighbors):
                        #     label = "Both are contagious region"
                        #     yes_self_yes_neighbor += 1
                        for n in neighbors:
                            if 1 in city.sa2.year2015.case[n]:
                                if len(city.sa2.year2015.case[n][1]) >= alert_threshold:
                                    label = 'Both are contagious region'
                                    yes_self_yes_neighbor += 1
                                    break
                    else:
                        label = "Not a contagious region"
                        no += 1
                else:
                    label = "Not a contagious region"
                    no += 1
            else:
                label = "Not a contagious region"
                no += 1

            if label == "Not a contagious region":
                neighbors = [n for n in neighbors if n in city.sa2.year2015.case]
                # if any(1 in city.sa2.year2015.case[n] for n in neighbors):
                #     no_self_yes_neighbor += 1
                for n in neighbors:
                    if 1 in city.sa2.year2015.case[n]:
                        if len(city.sa2.year2015.case[n][1]) >= alert_threshold:
                            no_self_yes_neighbor += 1
                            break
            print(label)

        else:
            try:
                check_next_week = use.case[a][w+1]
                if len(use.case[a][w+1]) >= alert_threshold:
                    label = "Only self is contagious region"
                    yes += 1
                else:
                    label = "Not a contagious region"
                    no += 1
            except KeyError as e:
                # print("next week no", e.args[0])
                no += 1
                label = "Not a contagious region"

            # next week: neighbor
            if label == "Only self is contagious region":
                neighbors = [n for n in neighbors if n in use.case]

                for n in neighbors:
                    if w+1 in use.case[n]:
                        if len(use.case[n][w+1]) >= alert_threshold:
                            label = "Both are contagious region"
                            yes_self_yes_neighbor += 1
                            break

                # if any(w+1 in use.case[n] for n in neighbors):
                #     label = "Both are contagious region"
                #     # print(i, label)
                #     yes_self_yes_neighbor += 1
            elif label == "Not a contagious region":
                neighbors = [n for n in neighbors if n in use.case]
                # if any(w+1 in use.case[n] for n in neighbors):
                #     no_self_yes_neighbor += 1
                for n in neighbors:
                    if w+1 in use.case[n]:
                        if len(use.case[n][w+1]) >= alert_threshold:
                            no_self_yes_neighbor += 1
                            break
        # print(i, a, w, label)
        df.iloc[i, df.columns.get_loc('result_label')] = label
    # df.iloc[3, df.columns.get_loc('female')] = 1234
    
    print(yes, yes_self_yes_neighbor, no, no_self_yes_neighbor)
    print(row)

    df.to_csv('../dataset/'+feature_file_name+'_feature.csv', index=False)

def computing_label_no_case(feature_file_name, city, year, CityGraphsa2, alert_threshold):
    import pandas as pd

    use = '?'
    if year == 2014:
        use = city.sa2.year2014
    elif year == 2015:
        use = city.sa2.year2015


    df = pd.read_csv('../dataset/'+feature_file_name+'_feature(no case).csv')
    # print(df.ix[3][0])
    row, col = (df.shape[0], df.shape[1])
    
    # define labels
    yes = 0                         # next week has case
    yes_self_yes_neighbor = 0       # next week has AND its neighbor has one
    no = 0                          # next week no
    no_self_yes_neighbor = 0        # next week no BUT its neighbor has

    for i in range(row):
        ### compute the label
        a, w = (df.iloc[i]['area'], df.iloc[i]['week'])
        label = "?"

        if a in CityGraphsa2:
            neighbors = CityGraphsa2[a]
        else:
            neighbors = []

        # check 2015 first week
        if w == 52 and year == 2014:
            if a in city.sa2.year2015.case:
                if 1 in city.sa2.year2015.case[a]:
                    if len(city.sa2.year2015.case[a][1]) >= alert_threshold:
                        label = "Only self is contagious region"
                        yes += 1
                        neighbors = [n for n in neighbors if n in city.sa2.year2015.case]
                        # if any(1 in city.sa2.year2015.case[n] for n in neighbors):
                        #     label = "Both are contagious region"
                        #     yes_self_yes_neighbor += 1
                        for n in neighbors:
                            if 1 in city.sa2.year2015.case[n]:
                                if len(city.sa2.year2015.case[n][1]) >= alert_threshold:
                                    label = 'Both are contagious region'
                                    yes_self_yes_neighbor += 1
                                    break
                    else:
                        label = "Not a contagious region"
                        no += 1
                else:
                    label = "Not a contagious region"
                    no += 1
            else:
                label = "Not a contagious region"
                no += 1

            if label == "Not a contagious region":
                neighbors = [n for n in neighbors if n in city.sa2.year2015.case]
                # if any(1 in city.sa2.year2015.case[n] for n in neighbors):
                #     no_self_yes_neighbor += 1
                for n in neighbors:
                    if 1 in city.sa2.year2015.case[n]:
                        if len(city.sa2.year2015.case[n][1]) >= alert_threshold:
                            no_self_yes_neighbor += 1
                            break

        # just check the next week
        else:
            if a in use.case:
                try:
                    check_next_week = use.case[a][w+1]
                    if len(use.case[a][w+1]) >= alert_threshold:
                        label = "Only self is contagious region"
                        yes += 1
                    else:
                        label = "Not a contagious region"
                        no += 1
                except KeyError as e:
                    # print("next week no", e.args[0])
                    no += 1
                    label = "Not a contagious region"

                # next week: neighbor
                if label == "Only self is contagious region":
                    neighbors = [n for n in neighbors if n in use.case]
                    # if any(w+1 in use.case[n] for n in neighbors):
                    #     label = "Both are contagious region"
                    #     # print(i, label)
                    #     yes_self_yes_neighbor += 1

                    for n in neighbors:
                        if w+1 in use.case[n]:
                            if len(use.case[n][w+1]) >= alert_threshold:
                                label = "Both are contagious region"
                                yes_self_yes_neighbor += 1
                                break

                elif label == "Not a contagious region":
                    neighbors = [n for n in neighbors if n in use.case]
                    # if any(w+1 in use.case[n] for n in neighbors):
                    #     no_self_yes_neighbor += 1
                    for n in neighbors:
                        if w+1 in use.case[n]:
                            if len(use.case[n][w+1]) >= alert_threshold:
                                no_self_yes_neighbor += 1
                                break
            else:
                # label must=="Not a contagious region"
                label = "Not a contagious region"
                no += 1
                neighbors = [n for n in neighbors if n in use.case]
                # if any(w+1 in use.case[n] for n in neighbors):
                #     no_self_yes_neighbor += 1
                for n in neighbors:
                    if w+1 in use.case[n]:
                        if len(use.case[n][w+1]) >= alert_threshold:
                            no_self_yes_neighbor += 1
                            break

        df.iloc[i, df.columns.get_loc('result_label')] = label
    
    print(yes, yes_self_yes_neighbor, no, no_self_yes_neighbor)
    print(row)

    df.to_csv('../dataset/'+feature_file_name+'_feature(no case).csv', index=False)

if __name__ == '__main__':
    main()