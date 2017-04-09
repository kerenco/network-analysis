import networkx as nx
from graph_features.utils import timer

def closeness_centrality(f, ft, gnx):
    start = timer.start(ft,'Closeness Centrality')
    result = nx.closeness_centrality(gnx)
    timer.stop(ft,start)

    for k in result:
        f.writelines(str(k) + ',' + str(result[k]) + '\n');
    return result