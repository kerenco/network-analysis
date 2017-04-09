import os
import sys
sys.path.append( os.getcwd() +"//..")
import featuresList
from features_calculator import featuresCalculator
from learning.TagsLoader import TagsLoader
import main_manager as mm

currentDirectory = str(os.getcwd())

if __name__ == "__main__":
    wdir = os.getcwd()
    file_in = str(wdir) + r'/../data/directed/cora/input/cora.txt'
    output_dir = str(wdir) + r'/../data/directed/cora/features'

    calculator = featuresCalculator()
    features_list = featuresList.featuresList(directed=True, analysisType='nodes').getFeatures()
    result = calculator.calculateFeatures(features_list, file_in, output_dir, directed=True, analysisType='nodes')

    classification_cora_result = ['cora_tags']  # , 'Nucleus', 'Membrane', 'Vesicles', 'Ribosomes', 'Extracellular']
    ml_algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM']
    directory_tags_path = str(wdir) + r'/../data/directed/cora/tags/'
    result_path = str(wdir) + r'/../data/directed/cora/results/'
    tagsLoader = TagsLoader(directory_tags_path, classification_cora_result)
    tagsLoader.Load()

    gnx = result[0]
    map_fetures = result[1]
    number_of_learning_for_mean = 10.0

    deep = False
    if (deep):
        mm.deepLearning(gnx, map_fetures, number_of_learning_for_mean=3.0,
                        classifications=classification_cora_result,
                        tags_loader=tagsLoader, result_path=result_path)
    else:
        mm.machineLearning(gnx, map_fetures, number_of_learning_for_mean=10.0,
                           classifications=classification_cora_result,
                           ml_algos=ml_algos,
                           tags_loader=tagsLoader,
                           result_path=result_path)


