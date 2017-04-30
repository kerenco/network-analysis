import os
import sys
sys.path.append( os.getcwd() +"//..")
import featuresList
from features_calculator import featuresCalculator
from learning.TagsLoader import TagsLoader
import main_manager as mm

currentDirectory = str(os.getcwd())

if __name__ == "__main__":

    #step 1: features calculate
    wdir = os.getcwd()
    file_in = str(wdir) + r'/../data/directed/social_sign/wiki/input/wiki.txt'

    output_dir = str(wdir) + r'/../data/directed/social_sign/wiki/features'

    calculator = featuresCalculator()
    features_list = featuresList.featuresList(True, 'edges').getFeatures()
    features_list.remove('motif4')
    features_list.remove('flow')
    features_list.remove('ab')
    features_list.remove('hierarchy_energy')
    print features_list
    result = calculator.calculateFeatures(['motif4'], file_in, output_dir, True, 'nodes',parallel=False)
    print result[1].keys()
    print len(result[1])

    # step 2: learning phase
    # classification_wiki_result = ['wiki-election-tags']
    # ml_algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM']
    # directory_tags_path = str(wdir) + r'/../data/directed/social_sign/wiki/tags/'
    # result_path = str(wdir) + r'/../data/directed/social_sign/wiki/results/'
    # tagsLoader = TagsLoader(directory_tags_path, classification_wiki_result)
    # tagsLoader.load_edges()
    # #
    # #
    # gnx = result[0]
    # map_fetures = result[1]
    # number_of_learning_for_mean = 1.0
    #
    # deep = False
    # if(deep):
    #     mm.deepLearning(gnx, map_fetures, number_of_learning_for_mean=3.0, classifications=classification_wiki_result, tags_loader=tagsLoader, result_path=result_path)
    # else:
    #     mm.machineLearning(gnx, map_fetures, number_of_learning_for_mean=number_of_learning_for_mean,
    #                        classifications=classification_wiki_result,
    #                        ml_algos=ml_algos,
    #                        tags_loader=tagsLoader,
    #                        result_path=result_path,
    #                        edges=True)


    #step 3: vizualization




