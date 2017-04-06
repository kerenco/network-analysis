from graph_coloring import GraphColoring


class Vizualizator:

    def __init__(self,gnx):
        self.graph = gnx
        self.graphColoring = GraphColoring(gnx)

    def draw_confusion_matrix(self):
        raise NotImplementedError('draw confusion not implement')

    def draw_feature_importance(self):
        raise NotImplementedError('draw feature importance not implement')

    def draw_auc(self):
        raise NotImplementedError('draw auc not implement')

    def draw_roc_curve(self):
        raise NotImplementedError('draw roc curve not implement')

    def draw_degree_hist(self):
        raise NotImplementedError('draw degree hist not implement')

    def draw_tags_hist(self):
        raise NotImplementedError('draw tags hist not implement')