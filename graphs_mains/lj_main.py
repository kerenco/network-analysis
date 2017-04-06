import os
import sys
from operator import itemgetter

import numpy as np

import featuresList
from features_calculator import featuresCalculator


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
features = import_path(currentDirectory + r'/../graph-fetures/fetures.py')

def machineLearning(gnx, map_fetures, number_of_learning_for_mean, result_path, classifications):
    for classification in classifications:
        auc_file_name = result_path + classification + '_auc.csv'
        auc_file = open(auc_file_name, 'a')
        features_importance_file_name = result_path + classification + '_features_importance.csv'
        features_importance_file = open(features_importance_file_name, 'w')

        vertex_to_tags = tagsLoader.calssification_to_vertex_to_tag[classification]
        result = FeturesMatrix.build_matrix_with_tags(gnx, map_fetures, vertex_to_tags, zscoring=True)
        feature_matrix = result[0]
        tags_vector = np.squeeze(np.asarray(result[1]))
        l = LearningPhase.SimpleMachineLearning(feature_matrix, tags_vector)
        for algo in ml_algos:
            print algo
            sum_auc_test = 0
            sum_auc_train = 0
            sum_feature_importance = 0
            for i in range(int(number_of_learning_for_mean)):
                cls = l.implementLearningMethod(algo)
                if (algo == 'RF'):
                    sum_feature_importance += cls.feature_importances_
                    print len(cls.feature_importances_)
                    print cls.feature_importances_
                auc_test = l.evaluate_AUC_test()
                print 'auc_test', auc_test
                sum_auc_test += auc_test
                auc_train = l.evaluate_AUC_train()
                print 'auc_train', auc_train
                sum_auc_train += auc_train
            auc_file.writelines(algo + ',' + str(sum_auc_test / number_of_learning_for_mean) + '\n')
            print 'mean_feature_importance', sum_feature_importance / number_of_learning_for_mean
            print 'mean_auc_test', sum_auc_test / number_of_learning_for_mean
            print 'mean_auc_train', sum_auc_train / number_of_learning_for_mean
            if algo == 'RF':
                for fi in features_importance_dict:
                    feature_importance_value = sum_feature_importance[fi] / number_of_learning_for_mean
                    features_importance_file.writelines(
                        features_importance_dict[fi] + ',' + str(feature_importance_value) + '\n')
        features_importance_file.close()
        auc_file.close()


def deepLearning(gnx, map_fetures, number_of_learning_for_mean, result_path, classifications):
    deep = import_path(currentDirectory + r'/../learning/deep_learning.py')
    for classification in classifications:
        print classification
        auc_file_name = result_path + classification + '_auc_d.csv'
        auc_file = open(auc_file_name, 'a')

        vertex_to_tags = tagsLoader.calssification_to_vertex_to_tag[classification]
        result = FeturesMatrix.build_matrix_with_tags(gnx, map_fetures, vertex_to_tags, zscoring=True)
        feature_matrix = result[0]
        tags_vector = np.squeeze(np.asarray(result[1]))
        deepL = deep.DeepLearning(feature_matrix, tags_vector)
        sum_auc_test = 0
        sum_auc_train = 0
        for i in range(int(number_of_learning_for_mean)):
            cls = deepL.runNetwork(0.2)
            auc_test = deepL.evaluate_AUC_test()
            print 'auc_test', auc_test
            sum_auc_test += auc_test
            auc_train = deepL.evaluate_AUC_train()
            print 'auc_train', auc_train
            sum_auc_train += auc_train
        auc_file.writelines('deep ,' + str(sum_auc_test / number_of_learning_for_mean) + '\n')
        print 'mean_auc_test', sum_auc_test / number_of_learning_for_mean
        print 'mean_auc_train', sum_auc_train / number_of_learning_for_mean
        auc_file.close()

if __name__ == "__main__":

    wdir = os.getcwd()
    for i in range(1,2):
        if(i<10):
            snap = '000'+str(i)
        else:
            snap = '00' + str(i)
        print snap

        # snap = '0001'
        file_in = str(wdir) + r'/../data/directed/live_journal/'+snap+r'/input/graph.txt'

        output_dir = str(wdir) + r'/../data/directed/live_journal/'+snap+r'/features'
        calculator = featuresCalculator()
        features_list = featuresList.featuresList(True, 'nodes').getFeatures()
        features_list.remove('flow')
        features_list.remove('ab')
        features_list.remove('eccentricity')
        features_list.remove('load_centrality')
        features_list.remove('hierarchy_energy')
        result = calculator.calculateFeatures(features_list, file_in, output_dir, True, 'nodes')

        motif_path = str(wdir) + r'/../graph-fetures/algo/motifVariations'
        result = features.calc_fetures_vertices(file_in, motif_path, output_dir, directed=True, takeConnected=True, fetures_list=directed_lj, return_map=True)

        print result[1].keys()

        place = 0
        features_importance_dict = {}

        for k, v in sorted(features.vertices_algo_dict.items(), key=itemgetter(1)):
            if k not in features_list:
                continue
            if k not in features.vertices_algo_feature_directed_length_dict:
                features_importance_dict[place] = k
                place += 1
            else:
                for i in range(features.vertices_algo_feature_directed_length_dict[k]):
                    features_importance_dict[place] = k + '[' + str(i) + ']'
                    place += 1

        print features_importance_dict

        for k in features_list:
            print k
            if not features.vertices_algo_feature_directed_length_dict.has_key(k):
                place += 1
            else:
                print k
                place += features.vertices_algo_feature_directed_length_dict[k]
        print place

        LearningPhase = import_path(currentDirectory + r'/../learning/simple_machine_learning.py')
        TagsLoader = import_path(currentDirectory + r'/../learning/TagsLoader.py')
        FeturesMatrix = import_path(currentDirectory + r'/../learning/FeturesMatrix.py')

        doi = ['summer'
            , 'the beatles'
            , 'cars'
            , 'traveling'
            , 'animals'
            , 'anime'
            , 'art'
            , 'books'
            , 'boys'
            , 'cars'
            , 'cats'
            , 'chocolate'
            , 'coffee'
            , 'computers'
            , 'concerts'
            , 'cooking'
            , 'dancing'
            , 'dogs'
            , 'drawing'
            , 'family'
            , 'fashion'
            , 'food'
            , 'friends'
            , 'girls'
            , 'guitar'
            , 'harry potter'
            , 'internet'
            , 'laughing'
            , 'love'
            , 'manga'
            , 'movies'
            , 'music'
            , 'painting'
            , 'photography'
            , 'pictures'
            , 'piercings'
            , 'poetry'
            , 'rain'
            , 'reading'
            , 'rock'
            , 'sex'
            , 'shopping'
            , 'singing'
            , 'sleeping'
            , 'snowboarding'
            , 'stars'
            , 'swimming'
            , 'taking back sunday'
            , 'tattoos'
            , 'video games'
            , 'writing']
        classification_lj_result = doi
        ml_algos = ['adaBoost', 'RF', 'L-SVM']#, 'RBF-SVM']
        directory_tags_path = str(wdir) + r'/../data/directed/live_journal/0001/tags/doi/'
        result_path = str(wdir) + r'/../data/directed/live_journal/'+snap+r'/results/'
        tagsLoader = TagsLoader.TagsLoader(directory_tags_path, classification_lj_result)
        tagsLoader.Load()

        gnx = result[0]
        map_fetures = result[1]

        deep = True
        if (deep):
            deepLearning(gnx, map_fetures, number_of_learning_for_mean=1.0, result_path=result_path,
                         classifications=classification_lj_result)
        else:
            machineLearning(gnx, map_fetures, number_of_learning_for_mean=4.0, result_path=result_path,
                            classifications=classification_lj_result)





