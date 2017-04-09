import os
import featuresList
from features_calculator import featuresCalculator
from graph_features import features as features
from learning.TagsLoader import TagsLoader
import main_manager as mm

currentDirectory = str(os.getcwd())

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
        tagsLoader = TagsLoader(directory_tags_path, classification_lj_result)
        tagsLoader.Load()

        gnx = result[0]
        map_fetures = result[1]

        deep = False
        if (deep):
            mm.deepLearning(gnx, map_fetures, number_of_learning_for_mean=3.0, classifications=classification_lj_result,
                            tags_loader=tagsLoader, result_path=result_path)
        else:
            mm.machineLearning(gnx, map_fetures, number_of_learning_for_mean=10.0,
                               classifications=classification_lj_result,
                               ml_algos=ml_algos,
                               tags_loader=tagsLoader,
                               result_path=result_path)





