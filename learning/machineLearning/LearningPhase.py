import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss
import pandas
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import cross_validation
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import SGDClassifier


class learningPhase:

    def __init__(self, featuresMat, tagsVec):
        self.featuresMat = np.asmatrix(featuresMat, dtype=float)
        self.tagsVec = tagsVec

    def DivideToTrainAndTest(self, testSize):
        self.x_train, self.x_test, self.y_train, self.y_test = cross_validation.train_test_split(self.featuresMat, self.tagsVec, test_size=testSize)

    def implementLearningMethod(self, algo):
        self.DivideToTrainAndTest(0.3)
        if algo == 'adaBoost':
            clf = AdaBoostClassifier(n_estimators=100)
        if algo == 'RF':
            clf = RandomForestClassifier(n_estimators=1000, criterion="gini", min_samples_split=15, oob_score=True, class_weight='balanced', max_depth=3)
        if algo == 'L-SVM':
            clf = SVC(kernel='linear', class_weight="balanced", C=0.01)
        if algo == 'RBF-SVM':
            clf = SVC(class_weight="balanced", C=0.01)
        self.classifier = clf.fit(self.x_train, self.y_train)

        return self.classifier



        # print('----------Train----CONFUSION----MATRIX----------')
        # print(confusion_matrix(self.y_train, train_pred))

        # print('----------Test----CONFUSION----MATRIX----------')
        # print(accuracy_score(self.y_test, predictions))
        # print(confusion_matrix(self.y_test, predictions))
        # print(classification_report(self.y_test, predictions))
        # file = open('auc.txt', 'w')
        # file.writelines(classification_report(self.y_test, predictions))
        # file.close()
        #
        #
        # print 'TrainAUC ' + str(aucTrain)
        #
        # print 'TestAUC ' + str(aucTest)
        # #self.plotROCcurve(test_fpr,test_tpr,train_fpr,train_tpr,aucTest,aucTrain)
        # return importantFeatures, aucTest, aucTrain

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

    def evaluate_importance(self):
        importantFeatures = None
        importantFeatures = None
        # if algo == 'adaBoost' or algo == 'RF':
        #     print clf.feature_importances_
        #     # importantFeatures = np.zeros(len(clf.feature_importances_))
        #     # for i in range(len(clf.feature_importances_)):
        #     #     if clf.feature_importances_[i] > 0:
        #     #         importantFeatures[i] = 1
        #     # print importantFeatures
        #     importantFeatures = clf.feature_importances_
        # elif algo == 'L-SVM':
        #     importantFeatures = np.asarray(clf.coef_)[0]

        return None

