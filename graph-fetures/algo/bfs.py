import networkx as nx
from utils import timer

def bfs_distance_distribution(f, ft, gnx):
    start = timer.start(ft,'BFS distance distribution')
    bfs_dist = calc_bfs_dist(gnx)
    timer.stop(ft,start)
    write_distance_distribution_to_file(bfs_dist, f)

def write_distance_distribution_to_file(bfs_dist, f):
    for n in bfs_dist:
        line = str(n)
        distance_distribution = bfs_dist[n]
        for d in distance_distribution:
            line = line + ',' + str(d)
        f.writelines(line + '\n');

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