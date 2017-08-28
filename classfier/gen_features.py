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

    '''counting SA0-2 per week'''

    tainan = City()
    kaohsiung = City()

    global young, middle, old

    CityGraphsa0, CityGraphsa1, CityGraphsa2 = read_graph_sturcture('Tainan')
    young = ['5-9', '2', '10-14']
    middle = ['50-54', '55-59', '35-39', '15-19', '25-29', '30-34', '40-44', '45-49',
              '20-24']
    old = ['70+', '65-69', '60-64']

    print(len(CityGraphsa0), len(CityGraphsa1), len(CityGraphsa2))
    
    output_feature_list("Tainan2014", tainan, 2014)
    print("tainan 2014 finish")
    output_feature_list("Tainan2015", tainan, 2015)
    print("tainan 2015 finish")

    sys.exit(0)

    # compute label for 2014, 2015 tainan   
    '''
    computing_label('Tainan2014_feature.csv', tainan)
    
    '''
    # computing_label('Tainan2015_feature.csv', tainan)

    # print(df)
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
            print(area, neighbors)
            # TainanLevel0s[area] = Level0(area)
            graph[area] = neighbors

    return CityGraphsa0, CityGraphsa1, CityGraphsa2

def output_feature_list(file_name, city, year):
    # Use city.sa2.year2014 or sity.sa2.year2015
    use = '?'
    if year == 2014:
        use = city.sa2.year2014
    elif year == 2015:
        use = city.sa2.year2015

    i = 0       # counter tainan case(sa2)
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
    # print(use.case)
    for area in use.case:
        # print(area)
        # print(use.case[area])
        for week in use.case[area]:
            # print(week, use.case[area][week])
            for case in use.case[area][week]:
                # print(week, case)
                # print(case['age'])
                if case['age'] not in age_categories:
                    age_categories.append(case['age'])
    # print(age_categories)
    # split age to young, middle, old

    # output 2014 feature
    with open('../dataset/'+file_name+'_feature.csv', 'w') as f:
        w = csv.writer(f)
        title = ['area', 'week', 'male', 'female', 'delay(avg)', 'young', 'middle', 'old', 'total', 'result_label']
        w.writerow(title)
        # each area, each week data
        for area in use.case:
            for week in use.case[area]:
                
                data = {x:0 for x in title}

                data['area'] = area
                data['week'] = week
                data['result_label'] = 'x'
                data['total'] = len(use.case[area][week])

                # print(area, week)
                

                total_delay_avg = 0
                for case in use.case[area][week]:
                    print('\t'+str(case))
                    # check gender
                    if case['gender'] == '\xe7\x94\xb7':
                        data['male'] += 1
                    else:
                        data['female'] += 1
                    # check age
                    # data[case['age']] += 1
                    if case['age'] in young:
                        data['young'] += 1
                    elif case['age'] in middle:
                        data['middle'] += 1
                    elif case['age'] in old:
                        data['old'] += 1
                    # check delay
                    total_delay_avg += case['delay']

                    data['delay(avg)'] = total_delay_avg / float(len(use.case[area][week]))

                # print(data)
                row = [data['area'], data['week'], data['male'], data['female'], data['delay(avg)'], data['young'], data['middle'], 
                       data['old'], data['total'], data['result_label']]
                w.writerow(row)


    print("A feature output finish")
    
def computing_label(feature_file, city):
    import pandas as pd
    # import neighbor012      # use to know the graph structure to compute labels
    import polygon_neighbors

    df = pd.read_csv(feature_file)
    print(df.ix[3][0])
    row, col = (df.shape[0], df.shape[1])

    also = 0                # next week also has case
    also_neighbor = 0       # next week also has AND its neighbor also has one
    no = 0                  # next week no
    no_neighbor = 0         # next week no BUT its neighbor has

    for i in range(row):
        ### compute the label
        a, w = (df.iloc[i]['area'], df.iloc[i]['week'])
        # print(i, a, w)
        # print(city.sa2.year2014.case[a][w])
        # print("the result is based on "+ str(w+1)+ " of " + a)
        label = "?"
        
        try:
            # neighbors = neighbor012.TainanGraphsa2[a]
            neighbors = polygon_neighbors.CityGraphsa2[a]
        except KeyError as e:
            print("keyerror")
            print(e)
            

        # print(neighbors)

        try:
            check_next_week = city.sa2.year2014.case[a][w+1]
            # print(check_next_week, "next week also")
            # print(i)
            label = "Still has case"
            print(label)
            also += 1

        except KeyError as e:
            # print("next week no", e.args[0])
            no += 1
            label = "No case"
            # if any(w+1 in city.sa2.year2014.case[n] for n in neighbors):
            #     label = "no BUT neighbor has"   
            #     no_neighbor += 1 

        if label == "Still has case":
            neighbors = [n for n in neighbors if n in city.sa2.year2014.case]
            if any(w+1 in city.sa2.year2014.case[n] for n in neighbors):
                label = "self and neighbor both"
                print(i, label)
                also_neighbor += 1

        elif label == "No case":
            neighbors = [n for n in neighbors if n in city.sa2.year2014.case]
            if any(w+1 in city.sa2.year2014.case[n] for n in neighbors):
                # label = "No case BUT neighbor has"
                
                print(i, label)
                no_neighbor += 1

        df.iloc[i, df.columns.get_loc('result_label')] = label
    # df.iloc[3, df.columns.get_loc('female')] = 1234
    
    print(also, also_neighbor, no, no_neighbor)
    print(row)
    df.to_csv(feature_file, index=False)

            
if __name__ == '__main__':
    main()