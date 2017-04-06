import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import SGDClassifier
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


class LearningBase:
    def __init__(self, featuresMat, tagsVec):
        self.featuresMat = np.asmatrix(featuresMat, dtype=float)
        self.tagsVec = tagsVec

    def DivideToTrainAndTest(self, testSize):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.featuresMat, self.tagsVec, test_size=testSize)


    def evaluate_AUC_test(self):
        predictions = self.classifier.predict(self.x_test)
        y = [int(i) for i in self.y_test]
        score = [int(i) for i in predictions]
        test_fpr, test_tpr, thresholds = metrics.roc_curve(y, score)
        aucTest = np.trapz(test_tpr, test_fpr)
        return aucTest

    def evaluate_AUC_train(self):
        train_pred = self.classifier.predict(self.x_train)
        y = [int(i) for i in self.y_train]
        score = [int(i) for i in train_pred]
        train_fpr, train_tpr, thresholds = metrics.roc_curve(y, score)
        aucTrain = np.trapz(train_tpr, train_fpr)
        return aucTrain

    def evaluate_confusion_metric_test(self):
        y_pred = self.classifier.predict_proba(self.x_test)
        y_pred = [np.argmax(lst) for lst in y_pred]
        y_true = [np.argmax(lst) for lst in self.y_test]
        confusion_matrix_result = metrics.confusion_matrix(y_true,y_pred)
        confusion_matrix_result = confusion_matrix_result.astype('float') / confusion_matrix_result.sum(axis=1)[:, np.newaxis]
        return confusion_matrix_result

    def evaluate_confusion_metric_train(self):
        y_pred = self.classifier.predict_proba(self.x_train)
        y_pred = [np.argmax(lst) for lst in y_pred]
        y_true = [int(i) for i in self.y_train]
        confusion_matrix_result = metrics.confusion_matrix(y_true, y_pred)
        print confusion_matrix_result
        return confusion_matrix_result

    def write_coloring_file(self, node_to_zscoringfeatures, vertex_to_tags, file_name = None):
        if(file_name != None):
            f = open(file_name,'w')

        coloring_node = []
        for n in node_to_zscoringfeatures:
            node_features = node_to_zscoringfeatures[n]
            prob = self.classifier.predict_proba(node_features)
            coloring_node.append((n ,prob))
            if(file_name != None):
                line = n +' ' + str(vertex_to_tags[n])
                for p in prob:
                    line += ',' + str(p)
                f.writelines(line + '\n')

        if (file_name != None):
            f.close()
        return coloring_node




