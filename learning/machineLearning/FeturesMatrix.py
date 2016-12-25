import numpy as np
import itertools

def build_matrix_from_fetures(gnx,map_fetures):
    node_to_fetures = {}
    for n in gnx.nodes():
        node_to_fetures[n] = []
    for fm in map_fetures:
        for k in map_fetures[fm]:
            if(type(map_fetures[fm][k]) == list):
                node_to_fetures[k] = list(itertools.chain(node_to_fetures[k],map_fetures[fm][k]))
            else:
                node_to_fetures[k].append(map_fetures[fm][k])


    return node_to_fetures
    # matrix = [node_to_fetures[node] for node in node_to_fetures]



def readTagsfromFile(node_to_fetures,fileName):
    with open(fileName) as f:
        for line in f:
            (key, val) = line.split()
            node_to_fetures[int(key)].insert(0,int(val))


def build_matrix_with_tags(gnx,map_fetures,fileName):
    node_to_fetures = build_matrix_from_fetures(gnx,map_fetures)
    readTagsfromFile(node_to_fetures, fileName)
    return np.asarray([node_to_fetures[node] for node in node_to_fetures])





# def initializeMap(gnx):
#     '''
#     creates a map between each vertex and its index in the matrix
#     :return: a map between each node/edge and its corresponding index in the matrix
#     '''
#     map = {}
#     index = 0
#     for node in gnx.nodes():
#         map[index] = node
#         index += 1
#     return map
#
#
# def createMatrix(map_index_to_node,gnx,map_fetures):
#     '''
#     fills the matrix using the algorithms for undirected graph
#     :return: the nav matrix
#     '''
#     matirx = [[]for x in range(len(gnx.nodes()))]
#     louvainMaps = map_fetures['louvain']
#     for lm in louvainMaps:
#         appendToMatrix(matrix,lm,map_index_to_node)
#     self.appendToNavsMat(k_core.k_core(graph=self.graph, recalculateFeatures=recalculateFeatures))
#     self.appendToNavsMat(bfs.bfs_distance_distribution(self.graph, recalculateFeatures=recalculateFeatures))
#     self.appendToNavsMat(
#         closenessCentrality.closeness_centrality(gnx=self.graph, recalculateFeatures=recalculateFeatures))
#     self.appendToNavsMat(myMotifs.find_all_motifs(gnx=self.graph, motifs_number=3))
#     # self.appendToNavsMat(myMotifs.find_all_motifs(gnx = self.graph,motifs_number=4))
#     print self.navsMat
#     return self.navsMat
#
#
# def appendToMatrix(matrix, feture_map,map_index_to_node):
#     '''
#     appends a score of a feature to the matrix in the place that fits each node/edge using the map
#     :param map: maps between a node and it's place in the matrix
#     :return:
#     '''
#     for i in range(len(matrix)):
#         feture = feture_map[map_index_to_node[i]]
#         if type(feature) != list or (type(feature) == list and len(feature) == 1):
#             self.navsMat[i].append(map[self.nodesMap[i]])
#         else:
#             for j in feature:
#                 self.navsMat[i].append(j)
#
#
# class createNavs:
#
#     def __init__(self, graph):
#         '''
#         the constructor of the create navs class
#         gets a graph and creates a matrix in the size: num of features over the num of nodes/edges
#         :param graph: a networkx graph(directed or undirected)
#         '''
#         self.graph = graph
#         self.navsMat = [[]for x in range(len(self.graph.nodes()))]
#         self.tags = []
#         self.nodesMap = self.createMap()
#
#     def createMap(self):
#         '''
#         creates a map between each vertex and its index in the matrix
#         :return: a map between each node/edge and its corresponding index in the matrix
#         '''
#         map = {}
#         index = 0
#         for node in self.graph.nodes():
#             map[index] = node
#             index += 1
#         return map
#
#     def createNavsMat(self, recalculateFeatures, fileName):
#         '''
#         fills the matrix using the algorithms for undirected graph
#         :return: the nav matrix
#         '''
#         maps = louvain.louvainCommunityDetection(graph=self.graph, recalculateFeatures=recalculateFeatures)
#         for map in maps:
#             self.appendToNavsMat(map)
#         self.appendToNavsMat(k_core.k_core(graph=self.graph, recalculateFeatures=recalculateFeatures))
#         self.appendToNavsMat(bfs.bfs_distance_distribution(self.graph, recalculateFeatures=recalculateFeatures))
#         self.appendToNavsMat(closenessCentrality.closeness_centrality(gnx=self.graph, recalculateFeatures=recalculateFeatures))
#         self.appendToNavsMat(myMotifs.find_all_motifs(gnx = self.graph,motifs_number=3))
#         #self.appendToNavsMat(myMotifs.find_all_motifs(gnx = self.graph,motifs_number=4))
#         print self.navsMat
#         return self.navsMat
#
#     def appendToNavsMat(self, map):
#         '''
#         appends a score of a feature to the matrix in the place that fits each node/edge using the map
#         :param map: maps between a node and it's place in the matrix
#         :return:
#         '''
#         for i in range(len(self.graph.nodes())):
#             feature = map[self.nodesMap[i]]
#             if v != list or (type(feature) == list and len(feature) == 1):
#                 self.navsMat[i].append(map[self.nodesMap[i]])
#             else:
#                 for j in feature:
#                     self.navsMat[i].append(j)
#
#     def readTagsfromFile(self,fileName):
#         with open(fileName) as f:
#             tmpMap = {}
#             for line in f:
#                 (key, val) = line.split()
#                 tmpMap[int(key)] = int(val)
#             for i in range(len(self.graph.nodes())):
#                 self.tags.append(tmpMap[self.nodesMap[i]])
#         return self.tags
