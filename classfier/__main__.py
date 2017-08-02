'''
process the data (case.csv -> feature.csv)
'''

import datetime
import csv
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
    fn = [
        'Tainan2014_SA0_week',
        'Tainan2014_SA1_week',
        'Tainan2014_SA2_week',

        'Tainan2015_SA0_week',
        'Tainan2015_SA1_week',
        'Tainan2015_SA2_week',
    ]
    tainan = City()
    kaohsiung = City()

    Tainan2014 = []
    Tainan2015 = []
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

    # output 2014 feature
    with open('../dataset/Tainan2014_feature.csv', 'w') as f:
        w = csv.writer(f)
        title = ['area', 'week', 'male', 'female', 'delay(avg)']+age_categories+['result_label']
        w.writerow(title)
        # each area, each week data
        for area in tainan.sa2.year2014.case:
            for week in tainan.sa2.year2014.case[area]:
                
                data = {x:0 for x in title}

                data['area'] = area
                data['week'] = week
                data['result_label'] = 'x'

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
                    [data['result_label']]
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
        title = ['area', 'week', 'male', 'female', 'delay(avg)']+age_categories+['result_label']
        w.writerow(title)
        # each area, each week data
        for area in tainan.sa2.year2015.case:
            for week in tainan.sa2.year2015.case[area]:
                
                data = {x:0 for x in title}

                data['area'] = area
                data['week'] = week
                data['result_label'] = 'x'

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
                    [data['result_label']]
                w.writerow(row)    

    # compute label for 2014, 2015 tainan   



            
if __name__ == '__main__':
    main()