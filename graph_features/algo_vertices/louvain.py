import community
from graph_features.utils import timer


def louvainCommunityDetection(f,ft,gnx):
    start = timer.start(ft, 'Louvain')
    bp = community.best_partition(gnx)
    comSizeBp = getCommunitySize(gnx, bp)
    timer.stop(ft,start)
    writeTofile(comSizeBp, f)
    return comSizeBp


def getCommunitySize(graph, partition):
    comSizeDict = {}
    nodesComSize = {}
    for com in set(partition.values()):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        comSizeDict[com] = len(list_nodes)
    for node in graph.nodes():
        nodesComSize[node] = comSizeDict[partition[node]]
    return nodesComSize

def writeTofile(partition, f):
    for k in partition:
        string = str(k)
        string += ',' + str(partition[k])
        f.writelines(string + '\n')
