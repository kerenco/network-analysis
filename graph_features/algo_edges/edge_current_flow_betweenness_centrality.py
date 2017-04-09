import networkx as nx
from graph_features.utils import timer

def edge_current_flow_betweenness_centrality(f, ft, gnx):
    start = timer.start(ft, 'Edge Current Flow Betweenness Centrality')
    result = nx.edge_current_flow_betweenness_centrality(gnx)
    timer.stop(ft, start)

    for k in result:
        f.writelines(str(k) + ',' + str(result[k]) + '\n')
    return result
