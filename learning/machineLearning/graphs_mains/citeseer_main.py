import os
import sys
# import LearningPhase
# import FeturesMatrix
import numpy as np
# from TagsLoader import TagsLoader
import multiprocessing
from operator import itemgetter



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
features = import_path(currentDirectory + r'/../../../graph-fetures/fetures.py')

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

directed_weighted = ['general','closeness','bfsmoments','flow','ab','kcore','page_rank','hierarchy_energ','motif3','load_centrality','average_neighbor_degree'] #no betweenness,motif4,eccentricity,communicability_centrality
undirected_weighted = ['general','betweenness','closeness','bfsmoments','kcore','louvain','page_rank','hierarchy_energ','motif3','eccentricity','load_centrality','communicability_centrality','average_neighbor_degree'] #no motif4, flow, ab, fiedler_vector
directed_unweighted = ['general','betweenness','closeness','bfsmoments','flow','ab','kcore','louvain','page_rank','fiedler_vector','hierarchy_energ','motif3','load_centrality','average_neighbor_degree'] #no motif4,eccentricity,communicability_centrality
undirected_unweighted = ['general','betweenness','closeness','bfsmoments','kcore','louvain','page_rank','hierarchy_energ','motif3','eccentricity','load_centrality','communicability_centrality','average_neighbor_degree'] #no motif4, flow, ab, fiedler_vector


directed_features = ['general','betweenness','closeness','bfsmoments','flow','ab','kcore','page_rank','motif3'
    ,'load_centrality','average_neighbor_degree','hierarchy_energy','eccentricity'] #no motif4,'hierarchy_energy','eccentricity'
undirected = ['general','betweenness','closeness','bfsmoments','kcore','louvain','page_rank','fiedler_vector',
    'motif3','eccentricity','load_centrality','communicability_centrality','average_neighbor_degree'] #no motif4, flow, ab, fiedler_vector,'hierarchy_energy'
edges = ['edge_flow', 'edge_betweenness']

directed_features.remove('eccentricity')
directed_features.remove('flow')
directed_features.remove('kcore')
directed_citeseer = directed_features

def machineLearning(gnx, map_fetures, number_of_learning_for_mean, confusion_matrix_file_name, classifications):
    confusion_matrix_file = open(confusion_matrix_file_name, 'a')
    features_importance_file_name = result_path + 'features_importance.csv'
    features_importance_file = open(features_importance_file_name, 'w')

    for classification in classifications:
        vertex_to_tags = tagsLoader.calssification_to_vertex_to_tag[classification]
        result = FeturesMatrix.build_matrix_with_tags(gnx, map_fetures, vertex_to_tags, zscoring=True)
        feature_matrix = result[0]
        tags_vector = np.squeeze(np.asarray(result[1]))
        l = LearningPhase.learningPhase(feature_matrix, tags_vector)
        for algo in ml_algos:
            print algo
            sum_confusion_matrix_test = 0
            sum_feature_importance = 0
            for i in range(int(number_of_learning_for_mean)):
                cls = l.implementLearningMethod(algo)
                if (algo == 'RF'):
                    sum_feature_importance += cls.feature_importances_
                    print len(cls.feature_importances_)
                    print cls.feature_importances_
                cm = l.evaluate_confusion_metric_test()
                sum_confusion_matrix_test += cm
            confusion_matrix_file.writelines(algo + ',' + str(sum_confusion_matrix_test))
            plot_file_name = result_path + '//' + algo + '_confusion_matrix.png'
            l.plot_confusion_matrix(sum_confusion_matrix_test, ['0', '1', '2', '3', '4', '5'], True,
                                    title='Confusion Matrix', plot_file_name=plot_file_name)

            if algo == 'RF':
                for fi in features_importance_dict:
                    feature_importance_value = sum_feature_importance[fi] / number_of_learning_for_mean
                    features_importance_file.writelines(
                        features_importance_dict[fi] + ',' + str(feature_importance_value) + '\n')
    features_importance_file.close()
    confusion_matrix_file.close()


def deepLearning(gnx, map_fetures, number_of_learning_for_mean, confusion_matrix_file_name, classifications):
    confusion_matrix_file = open(confusion_matrix_file_name, 'a')
    deep = import_path(currentDirectory + r'/../../deepLearning/learningPhase.py')
    for classification in classifications:
        vertex_to_tags = tagsLoader.calssification_to_vertex_to_tag[classification]
        result = FeturesMatrix.build_matrix_with_tags(gnx, map_fetures, vertex_to_tags, zscoring=True)
        feature_matrix = result[0]
        tags_vector = np.squeeze(np.asarray(result[1]))
        deepL = deep.learningPhase(feature_matrix, tags_vector)
        sum_confusion_matrix_test = 0
        for i in range(int(number_of_learning_for_mean)):
            cls = deepL.runNetwork(0.2,output_activation='softmax',output_size=6)
            cm = deepL.evaluate_confusion_metric_test()
            sum_confusion_matrix_test += cm
        confusion_matrix_file.writelines('deep,' + str(sum_confusion_matrix_test))
        plot_file_name = result_path + '//deep_confusion_matrix.png'
        deepL.plot_confusion_matrix(sum_confusion_matrix_test, ['0', '1', '2', '3', '4', '5'], True,
                                title='Confusion Matrix', plot_file_name=plot_file_name)
    confusion_matrix_file.close()



if __name__ == "__main__":

        file_in = str(wdir) + r'/../../../data/directed/citeseer/input/citeseer.txt'

        output_dir = str(wdir) + r'/../../../data/directed/citeseer/features'
        # os.mkdir(output_dir+'//output')
        # os.mkdir(output_dir+'//times')


        # processes = []
        # q = multiprocessing.Queue()
        # lock = multiprocessing.Lock()
        # for feature in directed_features:
        #     file_input = file_in
        #     motif_path = str(wdir) + r'/../../../graph-fetures/algo_vertices/motifVariations'
        #     outputDirectory = output_dir
        #     directed = True
        #     takeConnected = True
        #     fetures_list = [feature]
        #     print fetures_list
        #     return_map = False
        #
        #     processes.append(multiprocessing.Process(target=features.calc_fetures_vertices, args=(file_input, motif_path, outputDirectory, directed, takeConnected, fetures_list, return_map)))
        #
        # for pr in processes:
        #     pr.start()
        #
        # for pr in processes:
        #     pr.join()

        directed = True
        takeConnected = False
        motif_path = str(wdir) + r'/../../../graph-fetures/algo_vertices/motifVariations'
        result = features.calc_fetures_vertices(file_in, motif_path, output_dir, directed, takeConnected, directed_citeseer, return_map=True)
        place = 0
        features_importance_dict = {}

        for k,v in sorted(features.vertices_algo_dict.items(), key=itemgetter(1)):
            if k not in directed_citeseer:
                continue
            if k not in features.vertices_algo_feature_directed_length_dict:
                features_importance_dict[place] = k
                place +=1
            else:
                for i in range(features.vertices_algo_feature_directed_length_dict[k]):
                    features_importance_dict[place] = k + '[' + str(i) + ']'
                    place += 1

        print features_importance_dict

        for k in directed_citeseer:
            print k
            if not features.vertices_algo_feature_directed_length_dict.has_key(k):
                place += 1
            else:
                print k
                place += features.vertices_algo_feature_directed_length_dict[k]
        print place

        LearningPhase = import_path(currentDirectory + r'/../LearningPhase.py')
        TagsLoader = import_path(currentDirectory + r'/../TagsLoader.py')
        FeturesMatrix = import_path(currentDirectory + r'/../FeturesMatrix.py')

        classification_wiki_result = ['citeseer_tags']  # , 'Nucleus', 'Membrane', 'Vesicles', 'Ribosomes', 'Extracellular']
        ml_algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM']
        directory_tags_path = str(wdir) + r'/../../../data/directed/citeseer/tags/'
        result_path = str(wdir) + r'/../../../data/directed/citeseer/results/'
        tagsLoader = TagsLoader.TagsLoader(directory_tags_path, classification_wiki_result)
        tagsLoader.Load()

        gnx = result[0]
        map_fetures = result[1]
        number_of_learning_for_mean = 10.0

        confusion_matrix_file_name = result_path + 'confusion_matrix.txt'
        # confusion_matrix_file = open(confusion_matrix_file_name, 'w')
        # features_importance_file_name = result_path + 'features_importance.csv'
        # features_importance_file = open(features_importance_file_name,'w')

        # for classification in classification_wiki_result:
        #     vertex_to_tags = tagsLoader.calssification_to_vertex_to_tag[classification]
        #     result = FeturesMatrix.build_matrix_with_tags(gnx, map_fetures, vertex_to_tags, zscoring=True)
        #     feature_matrix = result[0]
        #     tags_vector = np.squeeze(np.asarray(result[1]))
        #     l = LearningPhase.learningPhase(feature_matrix, tags_vector)
        #     for algo in ml_algos:
        #         print algo
        #         sum_confusion_matrix_test = 0
        #         sum_feature_importance = 0
        #         for i in range(int(number_of_learning_for_mean)):
        #             cls = l.implementLearningMethod(algo)
        #             if(algo == 'RF'):
        #                 sum_feature_importance += cls.feature_importances_
        #                 print len(cls.feature_importances_)
        #                 print cls.feature_importances_
        #             cm = l.evaluate_confusion_metric_test()
        #             sum_confusion_matrix_test += cm
        #         confusion_matrix_file.writelines(algo + ','+str(sum_confusion_matrix_test)+'\n')
        #         plot_file_name = result_path + '//'+algo+'_confusion_matrix.png'
        #         l.plot_confusion_matrix(sum_confusion_matrix_test ,['0' , '1','2','3','4','5'],True,title='Confusion Matrix',plot_file_name= plot_file_name)
        #
        #         if algo == 'RF':
        #             for fi in features_importance_dict:
        #                 feature_importance_value = sum_feature_importance[fi] / number_of_learning_for_mean
        #                 features_importance_file.writelines(features_importance_dict[fi] + ','+str(feature_importance_value)+'\n')
        # features_importance_file.close()
        # confusion_matrix_file.close()

        deep = True
        if (deep):
            deepLearning(gnx, map_fetures, number_of_learning_for_mean=3.0,
                         confusion_matrix_file_name=confusion_matrix_file_name,
                         classifications=classification_wiki_result)
        else:
            machineLearning(gnx, map_fetures, number_of_learning_for_mean=10.0,
                            confusion_matrix_file_name=confusion_matrix_file_name,
                            classifications=classification_wiki_result)
