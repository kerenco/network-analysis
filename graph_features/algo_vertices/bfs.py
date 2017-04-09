import networkx as nx
from graph_features.utils import timer
import numpy as np

def bfs_distance_distribution(f,ft,gnx):
    start = timer.start(ft, 'BFS distance distribution')
    bfs_dist = calc_bfs_dist(gnx)
    dist_moments = {}
    for key in bfs_dist.keys():
        lst = []
        lst.append(float(np.average(bfs_dist[key], weights=range(1,len(bfs_dist[key])+1))))
        lst.append(float(np.std(bfs_dist[key])))
        dist_moments[key] = lst
    timer.stop(ft, start)
    write_bfs_moments_to_file(dist_moments, f)
    return dist_moments



def write_bfs_moments_to_file(dist_moments, f):
    for key in dist_moments:
        f.writelines(str(key) + ',' + str(dist_moments[key][0]) + ','+ str(dist_moments[key][1]) + '\n')


def calc_bfs_dist(gnx):
    bfs_dist = {}
    for n in gnx.nodes():
        node_dist = {}
        distances = nx.single_source_shortest_path_length(gnx, n)
        for k in distances.keys():
            if distances[k] in node_dist:
                node_dist[distances[k]] += 1
            else:
                node_dist[distances[k]] = 1
        bfs_dist[n] = node_dist.values()
    return bfs_dist

#
# def write_distance_distribution_to_file(bfs_dist):
#     f = open('output/output_bfs_distribution.txt', 'w')
#     for n in bfs_dist:
#         line = str(n)
#         distance_distribution = bfs_dist[n]
#         for d in distance_distribution:
#             line = line + ',' + str(d)
#         f.writelines(line + '\n')
#     f.close()



#
# def bfs_distance_distribution(f, ft, gnx):
#     start = timer.start(ft,'BFS distance distribution')
#     bfs_dist = calc_bfs_dist(gnx)
#     timer.stop(ft,start)
#     write_distance_distribution_to_file(bfs_dist, f)
#
# def write_distance_distribution_to_file(bfs_dist, f):
#     for n in bfs_dist:
#         line = str(n)
#         distance_distribution = bfs_dist[n]
#         for d in distance_distribution:
#             line = line + ',' + str(d)
#         f.writelines(line + '\n');
#
# def calc_bfs_dist(gnx):
#     bfs_dist = {}
#     for n in gnx.nodes():
#         node_dist = {}
#         distances = nx.single_source_shortest_path_length(gnx, n)
#         for k in distances.keys():
#             if distances[k] in node_dist:
#                 node_dist[distances[k]] += 1
#             else:
#                 node_dist[distances[k]] = 1
#         bfs_dist[n] = node_dist.values()
#     return bfs_dist
#
#
#
# import networkx as nx

# import os.path



