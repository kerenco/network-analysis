import numpy as np
import itertools

import numpy as np
def z_scoring(matrix):
    new_matrix = np.asmatrix(matrix)
    minimum = np.asarray(new_matrix.min(0))
    for i in range(minimum.shape[1]):
        if minimum[0,i] > 0:
            new_matrix[:,i] = np.log10(new_matrix[:,i])
        elif minimum[0,i] == 0:
            new_matrix[:, i] = np.log10(new_matrix[:, i]+0.1)
        if new_matrix[:,i].std() > 0:
            new_matrix[:,i] = (new_matrix[:,i]-new_matrix[:,i].min())/new_matrix[:,i].std()
    return new_matrix

def build_matrix_from_fetures(vertex_to_tag,map_fetures):
    node_to_fetures = {}
    for n in vertex_to_tag.keys():
        if n in map_fetures[1].keys():
            node_to_fetures[n] = []
    for fm in map_fetures:
        for k in node_to_fetures:
            if fm == 7:
                for i in range(len(map_fetures[fm][k])):
                    if sum(map_fetures[fm][k]) != 0:
                        map_fetures[fm][k][i] = map_fetures[fm][k][i]/sum(map_fetures[fm][k])
                node_to_fetures[k] = list(itertools.chain(node_to_fetures[k], map_fetures[fm][k]))
            elif(type(map_fetures[fm][k]) == list):
                node_to_fetures[k] = list(itertools.chain(node_to_fetures[k],map_fetures[fm][k]))
            else:
                node_to_fetures[k].append(map_fetures[fm][k])
    return node_to_fetures
    # matrix = [node_to_fetures[node] for node in node_to_fetures]



def build_matrix_with_tags(gnx,map_fetures,vertex_to_tag,zscoring = True):
    nodeWithTags_to_features = build_matrix_from_fetures(vertex_to_tag,map_fetures)
    [[nodeWithTags_to_features[node].insert(0,vertex_to_tag[node]) for node in nodeWithTags_to_features]]
    matrix_with_tags = np.asmatrix([nodeWithTags_to_features[node] for node in nodeWithTags_to_features])
    if(zscoring):
        feature_matrix = z_scoring(matrix_with_tags[:,1:])
    else:
        feature_matrix = matrix_with_tags[:,1:]

    tags_vector = matrix_with_tags[:,:1]
    return [feature_matrix, tags_vector]







# import numpy as np
# import itertools
#
# def build_matrix_from_fetures(gnx,map_fetures):
#     node_to_fetures = {}
#     for n in gnx.nodes():
#         node_to_fetures[n] = []
#     for fm in map_fetures:
#         for k in map_fetures[fm]:
#             if fm == 7:
#                 for i in range(len(map_fetures[fm][k])):
#                     if sum(map_fetures[fm][k]) != 0:
#                         map_fetures[fm][k][i] = map_fetures[fm][k][i]/sum(map_fetures[fm][k])
#                 node_to_fetures[k] = list(itertools.chain(node_to_fetures[k], map_fetures[fm][k]))
#             elif(type(map_fetures[fm][k]) == list):
#                 node_to_fetures[k] = list(itertools.chain(node_to_fetures[k],map_fetures[fm][k]))
#             else:
#                 node_to_fetures[k].append(map_fetures[fm][k])
#
#
#     return node_to_fetures
#     # matrix = [node_to_fetures[node] for node in node_to_fetures]
#
#
#
# def readTagsfromFile(node_to_fetures,fileName):
#     with open(fileName) as f:
#         for line in f:
#             line.rstrip()
#             (key, val) = line.split('\t')
#             node_to_fetures[key].insert(0,val.rstrip())
#
#
# def build_matrix_with_tags(gnx,map_fetures,fileName):
#     node_to_fetures = build_matrix_from_fetures(gnx,map_fetures)
#     readTagsfromFile(node_to_fetures, fileName)
#     matrix = np.asarray([node_to_fetures[node] for node in node_to_fetures])
#     return matrix
#




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
