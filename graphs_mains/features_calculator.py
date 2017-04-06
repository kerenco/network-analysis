import os
import sys
import multiprocessing
import featuresList

class featuresCalculator:
    def __init__(self):
        self.wdir = os.getcwd()
        self.featuresFile = self.import_path(str(self.wdir) + r'/../graph-fetures/fetures.py')
        self.motif_path = str(self.wdir) + r'/../graph-fetures/algo_vertices/motifVariations'

    def import_path(self, fullpath):
        """
        Import a file with full path specification. Allows one to
        import from anywhere, something __import__ does not do.
        """
        path, filename = os.path.split(fullpath)
        filename, ext = os.path.splitext(filename)
        sys.path.append(path)
        module = __import__(filename)
        reload(module)  # Might be out of date
        del sys.path[-1]
        return module

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


