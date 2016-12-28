from utils import timer

def general_information(gnx, f, ft):
    if(gnx.is_directed()):
        return general_information_directed(gnx, f, ft)
    else:
        return general_information_undirected(gnx, f, ft)

def general_information_directed(gnx, f, ft):
    out_deg = []
    in_deg = []
    start = timer.start(ft,'Genral information')
    nodes = gnx.nodes()
    [out_deg.append([n, gnx.out_degree(n)]) for n in nodes]
    [in_deg.append([n, gnx.in_degree(n)]) for n in nodes]
    timer.stop(ft,start)
    [f.writelines(str(i) + ',' + str(in_deg[i][1]) +',' + str(out_deg[i][1]) + '\n') for i in nodes]
    map_degree ={}
    for n in nodes:
        map_degree[n] = [in_deg[n][1], out_deg[n][1]]
    return map_degree


def general_information_undirected(gnx, f, ft):
    degrees = []
    start = timer.start(ft, 'Genral information')
    nodes = gnx.nodes()
    [degrees.append([n, gnx.degree(n)]) for n in nodes]
    timer.stop(ft, start)
    [f.writelines(str(degree[0]) + ',' + str(degree[1]) + '\n') for degree in degrees]
    map_degree = {}
    for degree in degrees:
        map_degree[degree[0]] = [degree[1]]
    return map_degree


