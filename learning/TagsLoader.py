class TagsLoader:

    def __init__(self, directory_full_path, calssifcation_files_name):
        self.directory_full_path = directory_full_path
        self.calssifcation_files_name = calssifcation_files_name
        self.calssification_to_vertex_to_tag = {}
        self.calssification_to_edge_to_tag = {}


    def readTagsfromFile(self,fileName):
        vertex_to_tag = {}
        with open(fileName) as f:
            for line in f:
                line.rstrip()
                (key, val) = line.split()
                vertex_to_tag[key] = float(val)
        return vertex_to_tag

    def readEdgesTagsfromFile(self,fileName):
        edge_to_tag = {}
        with open(fileName) as f:
            for line in f:
                line.rstrip()
                (src_trg, tag) = line.split(' ')
                (src, trg) = src_trg.split(',')
                tag = tag[0:-1]
                edge_to_tag[(src,trg)] = float(tag)
        return edge_to_tag

    def Load(self):
        for classification in self.calssifcation_files_name:
            fileNameTags = self.directory_full_path + classification + '.txt'
            vertex_to_tag = self.readTagsfromFile(fileNameTags)
            self.calssification_to_vertex_to_tag[classification] = vertex_to_tag

    def load_edges(self):
        for classification in self.calssifcation_files_name:
            fileNameTags = self.directory_full_path + classification + '.txt'
            edge_to_tag = self.readEdgesTagsfromFile(fileNameTags)
            self.calssification_to_edge_to_tag[classification] = edge_to_tag


