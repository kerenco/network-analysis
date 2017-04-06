import os
import sys
import numpy as np
from operator import itemgetter
from features_calculator import featuresCalculator
import featuresList



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

    # features calculate part 1
    wdir = os.getcwd()
    file_in = str(wdir) + r'/../../../data/directed/citeseer/input/citeseer.txt'
    output_dir = str(wdir) + r'/../../../data/directed/citeseer/features'
    calculator = featuresCalculator()
    features_list = featuresList.featuresList(directed=True, analysisType='nodes').getFeatures()
    features_list.remove('eccentricity')
    features_list.remove('kcore')
    features_list.remove('flow')
    result = calculator.calculateFeatures(features_list, file_in, output_dir, directed=True, analysisType='nodes')


    # Learning phase part 2
    place = 0
    features_importance_dict = {}

    for k,v in sorted(features.vertices_algo_dict.items(), key=itemgetter(1)):
        if k not in features_list:
            continue
        if k not in features.vertices_algo_feature_directed_length_dict:
            features_importance_dict[place] = k
            place +=1
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

    deep = True
    if (deep):
        deepLearning(gnx, map_fetures, number_of_learning_for_mean=3.0,
                     confusion_matrix_file_name=confusion_matrix_file_name,
                     classifications=classification_wiki_result)
    else:
        machineLearning(gnx, map_fetures, number_of_learning_for_mean=10.0,
                        confusion_matrix_file_name=confusion_matrix_file_name,
                        classifications=classification_wiki_result)
