import networkx as nx
from utils import timer


def eccentricity(gnx, f, ft):
    start = timer.start(ft,'eccentricity')
    eccentricity_nodes_map = {}
    for n in gnx.nodes():
        eccentricity_nodes_map[n] = nx.eccentricity(gnx,n)
    timer.stop(ft,start)
    for k in eccentricity_nodes_map:
        f.writelines(str(k) + ',' + str(eccentricity_nodes_map[k]) + '\n')
    return eccentricity_nodes_map