import os
import featuresList
from features_calculator import featuresCalculator
from learning.TagsLoader import TagsLoader
import main_manager as mm

currentDirectory = str(os.getcwd())

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
        mm.deepLearning(gnx, map_fetures, number_of_learning_for_mean=3.0, classifications=classification_diseases_result,
                        tags_loader=tagsLoader, result_path=result_path)
    else:
        mm.machineLearning(gnx, map_fetures, number_of_learning_for_mean=10.0,
                           classifications=classification_diseases_result,
                           ml_algos=ml_algos,
                           tags_loader=tagsLoader,
                           result_path=result_path)
