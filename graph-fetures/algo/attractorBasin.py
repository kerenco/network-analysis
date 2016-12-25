import networkx as nx
from utils import timer


def attractor_basin(gnx, f, ft):
    if(not gnx.is_directed()):
        return
    start = timer.start(ft, 'Attractor Basin')
    attractor_dict = calc_attractor_basin(gnx)
    timer.stop(ft, start)

    for k in attractor_dict.keys():
        f.writelines(str(k) + ',' + str(attractor_dict[k]) + '\n')

    return attractor_dict


def calc_attractor_basin(gnx):
    attractor_basin_dist, avg_in, avg_out = initialize_attraction_basin_dist(gnx)

    attractor_basin = calc_final_attraction_basin(attractor_basin_dist, avg_in, avg_out, gnx)
    return attractor_basin


def initialize_attraction_basin_dist(gnx):
    attractor_basin_dist, avg_add, avg_in, avg_out, reversed_gnx = initialize_variables(gnx)

    for n in gnx.nodes():
        in_dist = {}
        out_dist = {}
        out_nodes = nx.single_source_shortest_path_length(gnx, n)
        in_nodes = nx.single_source_shortest_path_length(reversed_gnx, n)
        for d in out_nodes.keys():
            m = out_nodes[d]
            if (m == 0):
                continue
            add_to_dict(out_dist, m, 1)
            add_to_dict(avg_out, m, avg_add)
        for d in in_nodes.keys():
            m = in_nodes[d]
            if (m == 0):
                continue
            add_to_dict(in_dist,m,1)
            add_to_dict(avg_in,m,avg_add)
        attractor_basin_dist[n] = [out_dist, in_dist]

    return attractor_basin_dist, avg_in, avg_out


def initialize_variables(gnx):
    number_of_nodes = nx.number_of_nodes(gnx)
    reversed_gnx = nx.reverse(gnx, True)
    attractor_basin_dist = {}
    avg_in = {}
    avg_out = {}
    avg_add = 1.0 / number_of_nodes;
    return attractor_basin_dist, avg_add, avg_in, avg_out, reversed_gnx


def calc_final_attraction_basin(attractor_basin_dist, avg_in, avg_out, gnx):
    attractor_basin = {}
    for n in gnx.nodes():
        alpha = 2;
        out_dist = attractor_basin_dist[n][0]
        in_dist = attractor_basin_dist[n][1]
        numerator = 0
        denominator = 0
        for m in in_dist:
            numerator = numerator + in_dist[m] / avg_in[m] * alpha ** (-m)
        for m in out_dist:
            denominator = denominator + out_dist[m] / avg_out[m] * alpha ** (-m)
        if (denominator == 0):
            attractor_basin[n] = -1
        else:
            attractor_basin[n] = numerator / denominator
    return attractor_basin


def add_to_dict(dict,key,value):
    if dict.has_key(key):
        dict[key] += value
    else:
        dict[key] = value