import networkx as nx
import numpy as np
from sklearn.manifold import Isomap
import os

def save_to_file_mds_matrix(m,nodes,f):
    for i in range(len(m[:, 1])):
        line = nodes[i] + ','
        l = ','.join(str(x) for x in m[i, :])
        line += l
        f.writelines(line + '\n')
    f.close()

def compute_distance_matrix(gnx,output_file_name):
    if (not os.path.isfile(output_file_name) or os.stat(output_file_name).st_size == 0):
        m = nx.floyd_warshall_numpy(gnx)
        disimilarities = np.asarray(m)
        f = open(output_file_name, 'w')
        np.save(f,disimilarities)
    else:
        f = open(output_file_name,'r')
        disimilarities = np.load(f)
    return disimilarities


def compute_isomap(gnx, n_neighbors, dim, distance_matrix_file_name, embedding_output_file):

    disimilarities = compute_distance_matrix(gnx, distance_matrix_file_name)

    X_iso_distanceMatrix = Isomap(n_neighbors=n_neighbors, n_components=dim).fit_transform(disimilarities)

    f = open(embedding_output_file,'w')
    save_to_file_mds_matrix(X_iso_distanceMatrix,gnx.nodes(),f)




