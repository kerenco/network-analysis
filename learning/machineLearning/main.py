import os
import sys
import LearningPhase
import FeturesMatrix
import zScoring
import numpy as np
import plotGraphs
import extractData
import matplotlib.pyplot as plt
from TagsLoader import TagsLoader


def import_path(fullpath):
    """
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do.
    """
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    reload(module) # Might be out of date
    del sys.path[-1]
    return module


currentDirectory = str(os.getcwd())
f = import_path(currentDirectory + r'/../../graph-fetures/fetures.py')

# 1 - Degrees
# 2 - betweenes
# 3 - closeness
# 4 - bfs moments
# 5 - flow
# 6 - A.B
# 7 - motif3
# 8 - motif4
# 9 - k-core
# 10 - louvain
# 11 - page_rank
# 12 - fiedler_vector

wdir = os.getcwd()
result = f.calc_fetures(file_input = str(wdir) + r'/../../data/signaling_pathways.txt'
                        ,motif_path = str(wdir) + r'/../../graph-fetures/algo/motifVariations'
                       ,outputDirectory=str(wdir) + r'/../../graph-fetures'
                       ,directed=True
                       ,weighted=False
                       ,fetures_list=['page_rank', 'general', 'closeness', 'bfsmoments', 'motif3',

                                      'kcore', 'betweenness', 'flow', 'ab'])



location_classifications = ['Cytosol']#, 'Nucleus', 'Membrane', 'Vesicles', 'Ribosomes', 'Extracellular']
function_classifications = ['Adapter', 'Kinase', 'Receptor', 'TF', 'Ligand']
ml_algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM']
directory_tags_path = r'C:/Users/Keren/Documents/GitHub/network-analysis/data/tags/signaling_pathways_tags_'
tagsLoader = TagsLoader(directory_tags_path, location_classifications)
tagsLoader.Load()

gnx = result[0]
map_fetures = result[1]

for classification in location_classifications:
    vertex_to_tags =tagsLoader.calssification_to_vertex_to_tag[classification]
    result = FeturesMatrix.build_matrix_with_tags(gnx, map_fetures, vertex_to_tags,zscoring = True)
    feature_matrix = result[0]
    tags_vector = np.squeeze(np.asarray(result[1]))
    l = LearningPhase.learningPhase(feature_matrix, tags_vector)
    for algo in ml_algos:
        sum_auc_test = 0
        sum_auc_train = 0
        for i in range(10):
            l.implementLearningMethod(algo)
            auc_test = l.evaluate_AUC_test()
            print 'auc_test',auc_test
            sum_auc_test += auc_test
            auc_train = l.evaluate_AUC_train()
            print 'auc_train',auc_train
            sum_auc_train += auc_train
        print 'mean_auc_test',sum_auc_test/10.0
        print 'mean_auc_train',sum_auc_train/10.0