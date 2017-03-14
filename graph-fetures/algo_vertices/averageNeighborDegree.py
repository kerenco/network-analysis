import networkx as nx
from utils import timer

def average_neighbor_degree(gnx, f, ft):
    start = timer.start(ft,'average_neighbor_degree')
    average_neighbor_degree_dict = nx.average_neighbor_degree(gnx)
    timer.stop(ft,start)
    for k in average_neighbor_degree_dict:
        f.writelines(str(k) + ',' + str(average_neighbor_degree_dict[k]) + '\n')
    return average_neighbor_degree_dict