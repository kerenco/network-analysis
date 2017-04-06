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


class learningPhase:
    def __init__(self, featuresMat, tagsVec):
        self.featuresMat = np.asmatrix(featuresMat, dtype=float)
        self.tagsVec = tagsVec

    def DivideToTrainAndTest(self, testSize):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.featuresMat, self.tagsVec, test_size=testSize)

    def implementLearningMethod(self, algo,test_size=0.3):
        self.DivideToTrainAndTest(test_size)
        if algo == 'adaBoost':
            clf = AdaBoostClassifier(n_estimators=100)
        if algo == 'RF':
            clf = RandomForestClassifier(n_estimators=1000, criterion="gini", min_samples_split=15, oob_score=True, class_weight='balanced', max_depth=3)
        if algo == 'L-SVM':
            clf = SVC(kernel='linear', class_weight="balanced", C=0.01)
        if algo == 'RBF-SVM':
            clf = SVC(class_weight="balanced", C=0.01)
        if algo == 'SGD':
            clf = SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,eta0=0.0,
                                fit_intercept=True, l1_ratio=0.15,learning_rate='optimal', loss='hinge',
                                n_iter=5, n_jobs=1,penalty='l2', power_t=0.5, random_state=None, shuffle=True,
                                verbose=0, warm_start=False)
        self.classifier = clf.fit(self.x_train, np.array(self.y_train).reshape(-1,))
        return self.classifier


    def plotROCcurve(self,test_fpr,test_tpr,train_fpr,train_tpr,aucTest,aucTrain):
        lw = 2
        plt.plot(test_fpr, test_tpr, color='darkorange',
                 lw=lw, label='test (area = %0.2f)' % aucTest)
        plt.plot(train_fpr, train_tpr, color='navy', lw=lw,
                 linestyle='--', label='train (area = %0.2f)' % aucTrain)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC curve')
        plt.legend(loc="lower right")
        plt.show()

    def plot_confusion_matrix(self, cm, classes,
                              normalize=False,
                              title='Confusion matrix',
                              plot_file_name='confusion matrix.png'):

        print normalize
        if (normalize):
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        df_cm = pd.DataFrame(cm, index=[i for i in classes],
                             columns=[i for i in classes])


        plt.figure()
        sn.heatmap(df_cm, annot=True)
        plt.title(title)
        plt.savefig(plot_file_name)

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
        y_pred = self.classifier.predict(self.x_test)
        y_true = [int(i) for i in self.y_test]
        confusion_matrix_result = metrics.confusion_matrix(y_true,y_pred)
        confusion_matrix_result = confusion_matrix_result.astype('float') / confusion_matrix_result.sum(axis=1)[:, np.newaxis]
        return confusion_matrix_result

    def evaluate_confusion_metric_train(self):
        y_pred = self.classifier.predict(self.x_train)
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




