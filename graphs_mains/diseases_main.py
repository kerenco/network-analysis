import os
from operator import itemgetter
import numpy as np
import featuresList
from features_calculator import featuresCalculator
from graph_features import fetures as features
from learning import simple_machine_learning as ml
from learning.TagsLoader import TagsLoader
from learning import FeturesMatrix


currentDirectory = str(os.getcwd())


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
        l = ml.SimpleMachineLearning(feature_matrix, tags_vector)
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
    from learning import deep_learning as deep
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
    file_in = str(wdir) + r'/../data/undirected/diseases/input/diseases_graph_with_weights.txt'
    output_dir = str(wdir) + r'/../data/undirected/diseases/features'

    calculator = featuresCalculator()
    features_list = featuresList.featuresList(directed=False, analysisType='nodes').getFeatures()
    features_list.remove('fiedler_vector')
    # features_list.remove('motif4')
    result = calculator.calculateFeatures(features_list, file_in, output_dir, directed=False, analysisType='nodes')

    diseases_tags = ['ConnectiveTissue',
                     'ImmunityDisorders',
                     'Symptoms',
                     'DiseasesOfTheBlood',
                     'MetabolicDiseases',
                     'Injury',
                     'Blood-FormingOrgans',
                     'Endocrine',
                     'Ill-DefinedConditions',
                     'ComplicationsOfPregnancy',
                     'DiseasesOfTheMusculoskeletalSystem',
                     'DiseasesOfTheDigestiveSystem',
                     'DiseasesOfTheRespiratorySystem',
                     'CertainConditionsOriginatingInThePerinatalPeriod',
                     'Childbirth',
                     'CongenitalAnomalies',
                     'ThePuerperium',
                     'Infectious',
                     'MentalDisorders',
                     'SubcutaneousTissue',
                     'Poisoning',
                     'DiseasesOfTheNervousSystem',
                     'SenseOrgans',
                     'Neoplasms',
                     'Nutritional',
                     'DiseasesOfTheSkin',
                     'DiseasesOfTheGenitourinarySystem',
                     'ParasiticDiseases',
                     'Signs',
                     'DiseasesOfTheCirculatorySystem']

    directed = False
    takeConnected = False
    motif_path = str(wdir) + r'/../graph-fetures/algo_vertices/motifVariations'
    # result = features.calc_fetures_vertices(file_in, motif_path, output_dir, directed, takeConnected,
    # result = features.calc_fetures_vertices(file_in, motif_path, output_dir, directed, takeConnected,
    #                                         ['motif4'], return_map=True)
    place = 0
    features_importance_dict = {}

    for k, v in sorted(features.vertices_algo_dict.items(), key=itemgetter(1)):
        if k not in features_list:
            continue
        if k not in features.vertices_algo_feature_undirected_length_dict:
            features_importance_dict[place] = k
            place += 1
        else:
            for i in range(features.vertices_algo_feature_undirected_length_dict[k]):
                features_importance_dict[place] = k + '[' + str(i) + ']'
                place += 1

    print features_importance_dict

    classification_diseases_result = diseases_tags  # , 'Nucleus', 'Membrane', 'Vesicles', 'Ribosomes', 'Extracellular']
    ml_algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM']
    directory_tags_path = str(wdir) + r'/../data/undirected/diseases/tags/'
    result_path = str(wdir) + r'/../data/undirected/diseases/results/'
    tagsLoader = TagsLoader(directory_tags_path, classification_diseases_result)
    tagsLoader.Load()

    gnx = result[0]
    map_fetures = result[1]

    deep = False
    if (deep):
        deepLearning(gnx, map_fetures, number_of_learning_for_mean=1.0, result_path=result_path,
                     classifications=classification_diseases_result)
    else:
        machineLearning(gnx, map_fetures, number_of_learning_for_mean=4.0, result_path=result_path,
                        classifications=classification_diseases_result)
