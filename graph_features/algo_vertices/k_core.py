import networkx as nx
from graph_features.utils import timer


def k_core(f,ft,gnx):
    start = timer.start(ft, 'K-Core')
    result = nx.core_number(gnx)
    timer.stop(ft, start)
    for k in result:
        f.writelines(str(k) + ',' + str(result[k]) + '\n');
    return result