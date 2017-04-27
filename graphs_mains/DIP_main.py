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
    file_in = str(wdir) + r'/../data/directed/DIP/input/DIP.txt'

    output_dir = str(wdir) + r'/../data/directed/DIP/features'

    calculator = featuresCalculator()
    features_list = featuresList.featuresList(directed=True, analysisType='nodes').getFeatures()
    result = calculator.calculateFeatures(features_list, file_in, output_dir, directed=True, analysisType='nodes')

