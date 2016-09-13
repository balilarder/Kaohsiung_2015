def read_home():
    # return a dictionary of home
    nodes = {}
    file = open('kao_popu.csv', 'r')
    allLines = file.readlines()

    total_areas = len(allLines)

    for i in range(1, total_areas):
        allLines[i] = allLines[i].replace("\n", "")
        segment = allLines[i].split(",")
        nodes[segment[0]] = int(segment[1])
        
    file.close()
    return nodes

def read_population():
    # return a dictionary of population
    nodes = {}
    file = open('kao_popu.csv', 'r')
    allLines = file.readlines()

    total_areas = len(allLines)

    for i in range(1, total_areas):
        allLines[i] = allLines[i].replace("\n", "")
        segment = allLines[i].split(",")
        nodes[segment[0]] = int(segment[2])
        
    file.close()
    return nodes

def read_area():
    # return a dictionary of area
    nodes = {}
    file = open('kao_area.csv', 'r')
    allLines = file.readlines()

    total_areas = len(allLines)

    for i in range(1, total_areas):
        allLines[i] = allLines[i].replace("\n", "")
        segment = allLines[i].split(",")
        nodes[segment[0]] = float(segment[1])
        
    file.close()
    return nodes