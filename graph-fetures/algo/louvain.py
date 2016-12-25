import community
from utils import timer


def louvainCommunityDetection(f,ft,gnx):
    start = timer.start(ft, 'Louvain')
    dendrogram = community.generate_dendrogram(gnx)
    partitions = []
    for level in range(len(dendrogram)):
        partition = community.partition_at_level(dendrogram, level)
        partitions.append(getCommunitySize(gnx, partition))
    timer.stop(ft,start)
    writeTofile(partitions, f)
    return partitions


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

def writeTofile(partitions, f):
    for k in partitions[0]:
        string = str(k)
        for part in partitions:
            string += ',' + str(part[k])
        f.writelines(string + '\n')
