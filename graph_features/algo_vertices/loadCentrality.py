import networkx as nx
from graph_features.utils import timer

def load_centrality(gnx, f, ft):
    start = timer.start(ft,'load_centrality')
    load_centrality_dict = nx.load_centrality(gnx)
    timer.stop(ft,start)
    for k in load_centrality_dict:
        f.writelines(str(k) + ',' + str(load_centrality_dict[k]) + '\n')
    return load_centrality_dict