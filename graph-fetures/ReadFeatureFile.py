def fileToMap_vertices(fPath):
    dict = {}
    with open(fPath) as f:
        for line in f:
            line = line.rstrip()
            lst = []
            splitted = line.split(',')
            for i in range(len(splitted)):
                if i > 0:
                    lst.append(float(splitted[i]))
            dict[splitted[0]] = lst
    return dict

def fileToMap_edges(fPath):
    dict = {}
    with open(fPath) as f:
        for line in f:
            line = line.rstrip()
            lst = []
            splitted = line.split(',')
            for i in range(len(splitted)):
                if i > 1:
                    lst.append(float(splitted[i]))
            dict[splitted[0]+','+splitted[1]] = lst
    return dict