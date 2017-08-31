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
def main():

    tainan = City()
    kaohsiung = City()

    global young, middle, old

    CityGraphsa0, CityGraphsa1, CityGraphsa2 = read_graph_sturcture('Tainan')
    young = ['5-9', '2', '10-14']
    middle = ['50-54', '55-59', '35-39', '15-19', '25-29', '30-34', '40-44', '45-49',
              '20-24']
    old = ['70+', '65-69', '60-64']

    print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))
    
    output_feature_list("Tainan2014", tainan, 2014, CityGraphsa2)
    print("tainan 2014 finish")
    output_feature_list("Tainan2015", tainan, 2015, CityGraphsa2)
    print("tainan 2015 finish")

    # compute label for 2014, 2015 tainan   
    computing_label('Tainan2014', tainan, 2014, CityGraphsa2)
    computing_label('Tainan2015', tainan, 2015, CityGraphsa2)
    
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
            neighbors = i[2].strip(',')
            neighbors = neighbors.split(',')
            # print(area, neighbors)
            # TainanLevel0s[area] = Level0(area)
            graph[area] = neighbors

    return CityGraphsa0, CityGraphsa1, CityGraphsa2

def output_feature_list(file_name, city, year, CityGraphsa2):
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
            if sa2 != "":
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
    # find the all age categories
    age_categories = []
    for area in use.case:
        for week in use.case[area]:
            for case in use.case[area][week]:
                if case['age'] not in age_categories:
                    age_categories.append(case['age'])
    # split age to young, middle, old

    # output feature file
    with open('../dataset/'+file_name+'_feature.csv', 'w') as f:
        w = csv.writer(f)
        title = ['area', 'week', 'male', 'female', 'delay(avg)', 'young', 'middle', 'old', 'total', 'neighbor-total', 'result_label']
        w.writerow(title)
        # each area, each week data
        for area in use.case:
            for week in use.case[area]:
                
                data = {x:0 for x in title}

                data['area'] = area
                data['week'] = week
                data['result_label'] = 'x'
                data['total'] = len(use.case[area][week])    

                # check neighbor-total:
                neighbor_total = 0
                print(area)
                if area in CityGraphsa2:
                    for neighbor in CityGraphsa2[area]:
                        print(neighbor, week)
                        if neighbor in use.case: 
                            if week in use.case[neighbor]:
                                print(week, len(use.case[neighbor][week])) 
                                neighbor_total += len(use.case[neighbor][week])     
                print(neighbor_total)
                print
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

def computing_label(feature_file_name, city, year, CityGraphsa2):
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
    also = 0                # next week also has case
    also_neighbor = 0       # next week also has AND its neighbor also has one
    no = 0                  # next week no
    no_neighbor = 0         # next week no BUT its neighbor has

    for i in range(row):
        ### compute the label
        a, w = (df.iloc[i]['area'], df.iloc[i]['week'])
        label = "?"

        if a in CityGraphsa2:
            neighbors = CityGraphsa2[a]
        else:
            neighbors = []
            
        # next week: self
        try:
            check_next_week = use.case[a][w+1]
            label = "Still has case"
            also += 1
        except KeyError as e:
            # print("next week no", e.args[0])
            no += 1
            label = "No case"

        # next week: neighbor
        if label == "Still has case":
            neighbors = [n for n in neighbors if n in use.case]
            if any(w+1 in use.case[n] for n in neighbors):
                label = "self and neighbor both"
                # print(i, label)
                also_neighbor += 1
        elif label == "No case":
            neighbors = [n for n in neighbors if n in use.case]
            if any(w+1 in use.case[n] for n in neighbors):
                # label = "No case BUT neighbor has"
                
                no_neighbor += 1
        # print(i, a, w, label)
        df.iloc[i, df.columns.get_loc('result_label')] = label
    # df.iloc[3, df.columns.get_loc('female')] = 1234
    
    print(also, also_neighbor, no, no_neighbor)
    print(row)
    df.to_csv('../dataset/'+feature_file_name+'_feature.csv', index=False)

            
if __name__ == '__main__':
    main()