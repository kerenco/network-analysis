import ReadFeatureFile
import networkx as nx
from utils import timer

def edge_based_degree(f,ft,gnx):
    if (gnx.is_directed()):
        return edge_based_degree_directed(gnx, f, ft)
    else:
        return edge_based_degree_undirected(gnx, f, ft)

def edge_based_degree_directed(gnx, f, ft):
    start = timer.start(ft, 'Edge based degree')
    nodes_dict = ReadFeatureFile.fileToMap_vertices('general.txt')
    edge_dict = {}
    for edge in gnx.edges():
        f.write(edge[0]+','+edge[1] + ' ')
        # f.write(str(edge) + ',')
        edge_dict[edge] = []
        sub_out = float(nodes_dict[edge[0]][0]) - nodes_dict[edge[1]][0]
        sub_in = float(nodes_dict[edge[0]][1]) - nodes_dict[edge[1]][1]
        mean_out = float(nodes_dict[edge[0]][0]) + nodes_dict[edge[1]][0] / 2
        mean_in = float(nodes_dict[edge[0]][1]) + nodes_dict[edge[1]][1] / 2
        f.write(str(sub_out) + ',' + str(mean_out) + ',')
        f.write(str(sub_in) + ',' + str(mean_in) + '\n')
        edge_dict[(edge[0], edge[1])].append(sub_out)
        edge_dict[(edge[0], edge[1])].append(mean_out)
        edge_dict[(edge[0], edge[1])].append(sub_in)
        edge_dict[(edge[0], edge[1])].append(mean_in)
    timer.stop(ft, start)
    return edge_dict

def edge_based_degree_undirected(gnx, f, ft):
    start = timer.start(ft, 'Edge based degree')
    nodes_dict = ReadFeatureFile.fileToMap_vertices('general.txt')
    edge_dict = {}
    for edge in gnx.edges():
        f.write(edge[0] + ',' + edge[1] + ' ')
        edge_dict[edge] = []
        sub = float(nodes_dict[edge[0]][0]) - nodes_dict[edge[1]][0]
        mean = float(nodes_dict[edge[0]][0]) + nodes_dict[edge[1]][0] / 2
        f.write(str(sub) + ',')
        f.write(str(mean) + '\n')
        edge_dict[edge].append(sub, mean)
    timer.stop(ft, start)
    return edge_dict

def edge_based_node_feature(f,gnx, map_algo):
    nodes_dict = map_algo
    edge_dict = {}
    for edge in gnx.edges():
        f.write(edge[0] + ',' + edge[1] + ' ')
        edge_dict[edge] = []
        if (type(nodes_dict[edge[0]]) is not list):
            sub = float(nodes_dict[edge[0]]) - nodes_dict[edge[1]]
            mean = float(nodes_dict[edge[0]]) + nodes_dict[edge[1]] / 2
            f.write(',' + str(sub) + ',' + str(mean))
            edge_dict[edge].append(sub)
            edge_dict[edge].append(mean)
        else:
            for index in range(len(nodes_dict[edge[0]])):
                sub = float(nodes_dict[edge[0]][index]) - nodes_dict[edge[1]][index]
                mean = float(nodes_dict[edge[0]][index]) + nodes_dict[edge[1]][index] / 2
                f.write(','+str(sub) + ',' + str(mean))
                edge_dict[edge].append(sub)
                edge_dict[edge].append(mean)
        f.write('\n')
    return edge_dict