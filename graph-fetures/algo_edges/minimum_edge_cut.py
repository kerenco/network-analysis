import networkx as nx
from utils import timer

def minimum_edge_cut(f, ft, gnx):
    start = timer.start(ft, 'Minimum Edge Cut')
    result = nx.minimum_edge_cut(gnx)
    timer.stop(ft, start)

    # for k in result:
    #     f.writelines(str(k) + ',' + str(result[k]) + '\n')
    return result
