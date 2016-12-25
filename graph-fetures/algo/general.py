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
    f.writelines('Number of Vertex:\n')
    f.writelines(str(len(gnx.nodes()))+'\n')
    f.writelines('Number of Edges:\n')
    f.writelines(str(len(gnx.edges()))+'\n')
    f.writelines('Out Degrees:\n')
    [f.writelines(str(out[0]) + ',' + str(out[1]) + '\n') for out in out_deg]
    f.writelines('In Degrees:\n')
    [f.writelines(str(i[0]) + ',' + str(i[1]) + '\n') for i in in_deg]
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
    f.writelines('Number of Vertex:\n')
    f.writelines(str(len(gnx.nodes())) + '\n')
    f.writelines('Number of Edges:\n')
    f.writelines(str(len(gnx.edges())) + '\n')
    f.writelines('Degrees:\n')
    [f.writelines(str(degree[0]) + ',' + str(degree[1]) + '\n') for degree in degrees]
    map_degree = {}
    for n in nodes:
        map_degree[n] = [degrees[n][1]]
    return map_degree


