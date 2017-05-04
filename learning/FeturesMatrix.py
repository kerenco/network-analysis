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
    k = map_fetures.keys()[0]
    for n in vertex_to_tag.keys():
        if n in map_fetures[k].keys():
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

def build_matrix_from_edges_fetures(edge_to_tag, map_features):
    edge_to_fetures = {}
    k = map_features.keys()[0]
    for e in map_features[k].keys():
        if edge_to_tag.has_key(e):
            edge_to_fetures[e] = []
    for fm in map_features:
        for k in edge_to_fetures:
            if fm == 7:
                for i in range(len(map_features[fm][k])):
                    if sum(map_features[fm][k]) != 0:
                        map_features[fm][k][i] = map_features[fm][k][i] / sum(map_features[fm][k])
                edge_to_fetures[k] = list(itertools.chain(edge_to_fetures[k], map_features[fm][k]))
            elif(type(map_features[fm][k]) == list):
                edge_to_fetures[k] = list(itertools.chain(edge_to_fetures[k], map_features[fm][k]))
            else:
                edge_to_fetures[k].append(map_features[fm][k])
    return edge_to_fetures

def build_matrix_with_tags(gnx, map_features, vertex_to_tag, zscoring = True):
    nodeWithTags_to_features = build_matrix_from_fetures(vertex_to_tag, map_features)
    [[nodeWithTags_to_features[node].insert(0,vertex_to_tag[node]) for node in nodeWithTags_to_features]]
    matrix_with_tags = np.asmatrix([nodeWithTags_to_features[node] for node in nodeWithTags_to_features])
    if(zscoring):
        feature_matrix = z_scoring(matrix_with_tags[:,1:])
    else:
        feature_matrix = matrix_with_tags[:,1:]

    tags_vector = matrix_with_tags[:,:1]

    node_to_features = build_object_to_features(nodeWithTags_to_features, zscoring)
    return [feature_matrix, tags_vector,node_to_features]

def build_matrix_with_tags_edges(gnx, map_features, edge_to_tag, zscoring = True):
    edgeWithTags_to_features = build_matrix_from_edges_fetures(edge_to_tag, map_features)
    [[edgeWithTags_to_features[node].insert(0, edge_to_tag[node]) for node in edgeWithTags_to_features]]
    matrix_with_tags = np.asmatrix([edgeWithTags_to_features[node] for node in edgeWithTags_to_features])
    if (zscoring):
        feature_matrix = z_scoring(matrix_with_tags[:, 1:])
    else:
        feature_matrix = matrix_with_tags[:, 1:]

    tags_vector = matrix_with_tags[:, :1]
    edge_to_features = build_object_to_features(edgeWithTags_to_features, zscoring)
    return [feature_matrix, tags_vector, edge_to_features]


def build_object_to_features(objectWithTags_to_features, zscoring=True):
    object_to_row = {}
    object_to_matrix = []
    row_index = 0
    for n in objectWithTags_to_features:
        object_to_matrix.append(objectWithTags_to_features[n])
        object_to_row[n] = row_index
        row_index += 1
    matrix = np.asmatrix(object_to_matrix)
    if(zscoring):
        z_matrix = z_scoring(matrix[:, 1:])
    else:
        z_matrix = matrix[:, 1:]
    object_to_zscoringfeatures = {}
    for n in objectWithTags_to_features:
        row_index = object_to_row[n]
        object_to_zscoringfeatures[n] = np.asarray(z_matrix[row_index, :])
    return object_to_zscoringfeatures