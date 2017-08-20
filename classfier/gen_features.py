'''
process the data (case.csv -> feature.csv)
'''

import datetime
import csv
import pandas as pd
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

    CityGraphsa0, CityGraphsa1, CityGraphsa2 = read_graph_sturcture('Tainan')
    young = ['5-9', '2', '10-14']
    middle = ['50-54', '55-59', '35-39', '15-19', '25-29', '30-34', '40-44', '45-49',
              '20-24']
    old = ['70+', '65-69', '60-64']

    i = 0       # counter tainan case(sa2)
    with open('../dataset/Tainan2014_case.csv', 'r') as f:
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
                if sa2 not in tainan.sa2.year2014.area:
                    tainan.sa2.year2014.area[sa2] = 1

                    tainan.sa2.year2014.case[sa2] = {week: [data]}

                else:
                    tainan.sa2.year2014.area[sa2] += 1
                    
                    # tainan.sa2.case[sa2][week].append(data)
                    if week not in tainan.sa2.year2014.case[sa2]:
                        tainan.sa2.year2014.case[sa2][week] = [data]
                    else:
                        tainan.sa2.year2014.case[sa2][week].append(data)                
    # find the all age categories
    age_categories = []
    print(tainan.sa2.year2014.case)
    for area in tainan.sa2.year2014.case:
        print(area)
        # print(tainan.sa2.year2014.case[area])
        for week in tainan.sa2.year2014.case[area]:
            # print(week, tainan.sa2.year2014.case[area][week])
            for case in tainan.sa2.year2014.case[area][week]:
                # print(week, case)
                # print(case['age'])
                if case['age'] not in age_categories:
                    age_categories.append(case['age'])
    print(age_categories)
    # split age to young, middle, old


    # output 2014 feature
    with open('../dataset/Tainan2014_feature.csv', 'w') as f:
        w = csv.writer(f)
        title = ['area', 'week', 'male', 'female', 'delay(avg)']+age_categories+['total', 'result_label']
        w.writerow(title)
        # each area, each week data
        for area in tainan.sa2.year2014.case:
            for week in tainan.sa2.year2014.case[area]:
                
                data = {x:0 for x in title}

                data['area'] = area
                data['week'] = week
                data['result_label'] = 'x'
                data['total'] = len(tainan.sa2.year2014.case[area][week])

                print(area, week)
                

                total_delay_avg = 0
                for case in tainan.sa2.year2014.case[area][week]:
                    print('\t'+str(case))

                    if case['gender'] == '\xe7\x94\xb7':
                        data['male'] += 1
                    else:
                        data['female'] += 1
                    data[case['age']] += 1

                    total_delay_avg += case['delay']

                    data['delay(avg)'] = total_delay_avg / float(len(tainan.sa2.year2014.case[area][week]))

                print(data)
                row = [data['area'], data['week'], data['male'], data['female'], data['delay(avg)']]+[data[x] for x in age_categories]+\
                    [data['total'], data['result_label']]
                w.writerow(row)
    
    # 2015
    with open('../dataset/Tainan2015_case.csv', 'r') as f:
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
                if sa2 not in tainan.sa2.year2015.area:
                    tainan.sa2.year2015.area[sa2] = 1

                    tainan.sa2.year2015.case[sa2] = {week: [data]}

                else:
                    tainan.sa2.year2015.area[sa2] += 1
                    
                    # tainan.sa2.case[sa2][week].append(data)
                    if week not in tainan.sa2.year2015.case[sa2]:
                        tainan.sa2.year2015.case[sa2][week] = [data]
                    else:
                        tainan.sa2.year2015.case[sa2][week].append(data)                
    # find the all age categories
    age_categories = []
    print(tainan.sa2.year2015.case)
    for area in tainan.sa2.year2015.case:
        print(area)
        # print(tainan.sa2.year2014.case[area])
        for week in tainan.sa2.year2015.case[area]:
            # print(week, tainan.sa2.year2014.case[area][week])
            for case in tainan.sa2.year2015.case[area][week]:
                # print(week, case)
                # print(case['age'])
                if case['age'] not in age_categories:
                    age_categories.append(case['age'])
    print(age_categories)
    # output 2015 feature
    with open('../dataset/Tainan2015_feature.csv', 'w') as f:
        w = csv.writer(f)
        title = ['area', 'week', 'male', 'female', 'delay(avg)']+age_categories+['total','result_label']
        w.writerow(title)
        # each area, each week data
        for area in tainan.sa2.year2015.case:
            for week in tainan.sa2.year2015.case[area]:
                
                data = {x:0 for x in title}

                data['area'] = area
                data['week'] = week
                data['result_label'] = 'x'
                data['total'] = len(tainan.sa2.year2015.case[area][week])
                print(area, week)
                

                total_delay_avg = 0
                for case in tainan.sa2.year2015.case[area][week]:
                    print('\t'+str(case))

                    if case['gender'] == '\xe7\x94\xb7':
                        data['male'] += 1
                    else:
                        data['female'] += 1
                    data[case['age']] += 1

                    total_delay_avg += case['delay']

                    data['delay(avg)'] = total_delay_avg / float(len(tainan.sa2.year2015.case[area][week]))

                print(data)
                row = [data['area'], data['week'], data['male'], data['female'], data['delay(avg)']]+[data[x] for x in age_categories]+\
                    [data['total'], data['result_label']]
                w.writerow(row)    


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