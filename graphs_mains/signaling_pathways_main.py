import os
import sys
sys.path.append( os.getcwd() +"//..")
import featuresList
from features_calculator import featuresCalculator
from learning.TagsLoader import TagsLoader
import main_manager as mm

currentDirectory = str(os.getcwd())

def resultAnalysis(year, classifications, tags_type):
    wdir = os.getcwd()
    file_in = str(
        wdir) + r'/../data/directed/signaling_pathway/' + year + '/input/signaling_pathways_' + year + '.txt'
    output_dir = str(wdir) + r'/../data/directed/signaling_pathway/' + year + '/features'

    calculator = featuresCalculator()
    features_list = featuresList.featuresList(True, 'nodes').getFeatures()
    # features_list.remove('eccentricity')
    result = calculator.calculateFeatures(features_list, file_in, output_dir, True, 'nodes')

    directory_tags_path = str(wdir) + r'/../data/directed/signaling_pathway/' + year + '/tags/'+tags_type+'/signaling_pathways_tags_'
    result_path = str(wdir) + r'/../data/directed/signaling_pathway/' + year + '/results/'

    tagsLoader = TagsLoader(directory_tags_path, classifications)
    tagsLoader.Load()

    ml_algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM']


    gnx = result[0]
    map_fetures = result[1]

    deep = False
    if (deep):
        mm.deepLearning(gnx, map_fetures, number_of_learning_for_mean=3.0, classifications=classifications,
                        tags_loader=tagsLoader, result_path=result_path, save_clf_file_name=None,
                        load_clf_file_name=result_path + r'clf/')
    else:
        mm.machineLearning(gnx, map_fetures, number_of_learning_for_mean=10.0,
                           classifications=classifications,
                           ml_algos=ml_algos,
                           tags_loader=tagsLoader,
                           result_path=result_path,
                           save_clf_file_name=result_path + r'clf/',
                           load_clf_file_name=None)



if __name__ == "__main__":
    location_classifications = ['Cytosol', 'Nucleus', 'Membrane', 'Vesicles','Ribosomes','Extracellular']
    function_classifications = ['Adapter', 'Kinase', 'Receptor', 'TF', 'Ligand']
    resultAnalysis(year='2004', classifications=location_classifications, tags_type='location')
    resultAnalysis(year='2004', classifications=function_classifications, tags_type='function')
    resultAnalysis(year='2006', classifications=location_classifications, tags_type='location')
    resultAnalysis(year='2006', classifications=function_classifications, tags_type='function')
