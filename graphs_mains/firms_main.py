import os
import featuresList
from features_calculator import featuresCalculator
from learning.TagsLoader import TagsLoader
import main_manager as mm

currentDirectory = str(os.getcwd())

if __name__ == "__main__":
    wdir = os.getcwd()

    for year in range(1999,2000):

        print str(year)
        file_in = str(wdir) + r'/../data/undirected/firms/'+str(year)+r'/input/firms_'+str(year)+'.txt'
        output_dir = str(wdir) + r'/../data/undirected/firms/'+str(year)+r'/features'
        calculator = featuresCalculator()
        features_list = featuresList.featuresList(directed=False, analysisType='nodes').getFeatures()
        features_list.remove('fiedler_vector')
        result = calculator.calculateFeatures(features_list, file_in, output_dir, directed=False, analysisType='nodes')


        classification_firms_result = ['dis_tags', 'top_tags']
        ml_algos = ['adaBoost', 'RF', 'L-SVM']  # , 'RBF-SVM']
        directory_tags_path = str(wdir) + r'/../data/undirected/firms/'+str(year)+'/tags/firms_'+str(year)+'_'
        result_path = str(wdir) + r'/../data/undirected/firms/' + str(year) + r'/results/'
        tagsLoader = TagsLoader(directory_tags_path, classification_firms_result)
        tagsLoader.Load()

        gnx = result[0]
        map_fetures = result[1]

        deep = False
        if (deep):
            mm.deepLearning(gnx, map_fetures, number_of_learning_for_mean=3.0, classifications=classification_firms_result,
                            tags_loader=tagsLoader, result_path=result_path)
        else:
            mm.machineLearning(gnx, map_fetures, number_of_learning_for_mean=10.0,
                               classifications=classification_firms_result,
                               ml_algos=ml_algos,
                               tags_loader=tagsLoader,
                               result_path=result_path)