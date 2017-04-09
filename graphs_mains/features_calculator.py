import os
import multiprocessing
from graph_features import features as features

class featuresCalculator:
    def __init__(self):
        self.wdir = os.getcwd()
        self.featuresFile = features
        self.motif_path = str(self.wdir) + r'/../graph-fetures/algo_vertices/motifVariations'

    def calculateFeatures(self, features_list, file_in, output_dir, directed, analysisType):
        processes = []
        for feature in features_list:
            file_input = file_in
            motif_path = str(self.wdir) + r'/../graph-fetures/algo_vertices/motifVariations'
            outputDirectory = output_dir
            takeConnected = True
            fetures_list = [feature]
            print fetures_list
            return_map = False

            if analysisType == 'nodes':
                processes.append(multiprocessing.Process(target=self.featuresFile.calc_fetures_vertices, args=(
                file_input, motif_path, outputDirectory, directed, takeConnected, fetures_list, return_map)))
            else:
                processes.append(multiprocessing.Process(target=self.featuresFile.calc_fetures_edges, args=(
                    file_input, motif_path, outputDirectory, directed, takeConnected, fetures_list, return_map)))

        for pr in processes:
            pr.start()

        for pr in processes:
            pr.join()

        if analysisType == 'nodes':
            result = self.featuresFile.calc_fetures_vertices(file_input, motif_path, outputDirectory, directed, takeConnected,
                                                            features_list, return_map=True)
        else:
            result = self.featuresFile.calc_fetures_edges(file_input, motif_path, outputDirectory, directed,
                                                             takeConnected,
                                                             features_list, return_map=True)

        return result


