import networkx as nx
from graph_features.utils import timer

def communicability_centrality(gnx, f, ft):
    start = timer.start(ft,'load_centrality')
    communicability_centrality_dict = nx.communicability_centrality(gnx)
    timer.stop(ft,start)
    for k in communicability_centrality_dict:
        f.writelines(str(k) + ',' + str(communicability_centrality_dict[k]) + '\n')
    return communicability_centrality_dict