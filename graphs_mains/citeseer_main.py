import os
import featuresList
from features_calculator import featuresCalculator
from learning.TagsLoader import TagsLoader
import main_manager as mm

currentDirectory = str(os.getcwd())

if __name__ == "__main__":

    # features calculate part 1
    wdir = os.getcwd()
    file_in = str(wdir) + r'/../data/directed/citeseer/input/citeseer.txt'
    output_dir = str(wdir) + r'/../data/directed/citeseer/features'
    calculator = featuresCalculator()
    features_list = featuresList.featuresList(directed=True, analysisType='nodes').getFeatures()
    features_list.remove('eccentricity')
    features_list.remove('kcore')
    features_list.remove('flow')
    result = calculator.calculateFeatures(features_list, file_in, output_dir, directed=True, analysisType='nodes')

    # Learning phase part 2
    classification_citeseer_result = ['citeseer_tags']  # , 'Nucleus', 'Membrane', 'Vesicles', 'Ribosomes', 'Extracellular']
    ml_algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM']
    directory_tags_path = str(wdir) + r'/../data/directed/citeseer/tags/'
    result_path = str(wdir) + r'/../data/directed/citeseer/results/'
    tagsLoader = TagsLoader(directory_tags_path, classification_citeseer_result)
    tagsLoader.Load()

    gnx = result[0]
    map_fetures = result[1]
    number_of_learning_for_mean = 10.0

    confusion_matrix_file_name = result_path + 'confusion_matrix.txt'

    deep = False
    if (deep):
        mm.deepLearning(gnx, map_fetures, number_of_learning_for_mean=3.0,
                        classifications=classification_citeseer_result,
                        tags_loader=tagsLoader, result_path=result_path)
    else:
        mm.machineLearning(gnx, map_fetures, number_of_learning_for_mean=10.0,
                           classifications=classification_citeseer_result,
                           ml_algos=ml_algos,
                           tags_loader=tagsLoader,
                           result_path=result_path)
