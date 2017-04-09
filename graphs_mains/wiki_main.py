import os
import featuresList
from features_calculator import featuresCalculator
from learning.TagsLoader import TagsLoader
import main_manager as mm

currentDirectory = str(os.getcwd())

if __name__ == "__main__":

    wdir = os.getcwd()
    file_in = str(wdir) + r'/../data/directed/wiki-rfa/input/wiki.txt'

    output_dir = str(wdir) + r'/../data/directed/wiki-rfa/features'

    calculator = featuresCalculator()
    features_list = featuresList.featuresList(True, 'nodes').getFeatures()
    features_list.remove('motif4')
    features_list.remove('flow')
    result = calculator.calculateFeatures(features_list, file_in, output_dir, True, 'nodes')


    classification_wiki_result = ['wiki-tags']  # , 'Nucleus', 'Membrane', 'Vesicles', 'Ribosomes', 'Extracellular']
    ml_algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM']
    directory_tags_path = str(wdir) + r'/../data/directed/wiki-rfa/tags/'
    result_path = str(wdir) + r'/../data/directed/wiki-rfa/results/'
    tagsLoader = TagsLoader(directory_tags_path, classification_wiki_result)
    tagsLoader.Load()


    gnx = result[0]
    map_fetures = result[1]
    number_of_learning_for_mean = 10.0

    deep = False
    if(deep):
        mm.deepLearning(gnx,map_fetures,number_of_learning_for_mean=3.0,classifications=classification_wiki_result,tags_loader=tagsLoader,result_path=result_path)
    else:
        mm.machineLearning(gnx,map_fetures,number_of_learning_for_mean=10.0,
                           classifications=classification_wiki_result,
                           ml_algos=ml_algos,
                           tags_loader=tagsLoader,
                           result_path=result_path)


