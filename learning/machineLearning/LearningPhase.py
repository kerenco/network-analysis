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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import SGDClassifier


class learningPhase:

    def __init__(self, featuresMat, tagsVec):
        self.featuresMat = np.asmatrix(featuresMat, dtype=float)
        self.tagsVec = tagsVec

    def DivideToTrainAndTest(self, testSize, isValitation):
        self.x_train, self.x_test, self.y_train, self.y_test = cross_validation.train_test_split(self.featuresMat, self.tagsVec, test_size=testSize, random_state=7)
        #row = int(self.featuresMat.shape[0] * trainSize / 100)
        # self.x_train = self.featuresMat[:row, :]
        # self.y_train = self.tagsVec[:row]
        # self.x_test = self.featuresMat[row:, :]
        # self.y_test = self.tagsVec[row:]
        #return self.x_train, self.x_test, self.y_train, self.y_test

    def implementLearningMethod(self):
        self.DivideToTrainAndTest(0.3, False)

        num_folds = 10
        num_instances = len(self.x_train)
        seed = 7
        scoring = 'accuracy'

        models = []
        #models.append(('LR', LogisticRegression()))
        #models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('SGD', SGDClassifier(n_iter=1000, alpha=0.01, class_weight='balanced')))
        models.append(('RF', RandomForestClassifier(n_estimators=1000, criterion="entropy", min_samples_split=5, oob_score=True, class_weight='balanced')))
        models.append(('NB', GaussianNB()))
        models.append(('SVM-RBF', SVC(class_weight="balanced")))
        models.append(('AdaBoost', AdaBoostClassifier()))

        # evaluate each model in turn
        results = []
        names = []

        for name, model in models:
            kfold = cross_validation.KFold(n=num_instances, n_folds=num_folds, random_state=seed)
            cv_results = cross_validation.cross_val_score(model, self.x_train, self.y_train, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)

        # Compare Algorithms
        fig = plt.figure()
        fig.suptitle('Algorithm Comparison')
        ax = fig.add_subplot(111)
        plt.boxplot(results)
        ax.set_xticklabels(names)
        plt.show()

        #sgd = RandomForestClassifier(n_estimators=1000, criterion="entropy", min_samples_split=5, oob_score=True, class_weight='balanced')
        sgd = AdaBoostClassifier()
        sgd.fit(self.x_train, self.y_train)
        predictions = sgd.predict(self.x_test)
        print(accuracy_score(self.y_test, predictions))
        print(confusion_matrix(self.y_test, predictions))
        print(classification_report(self.y_test, predictions))
        file = open('auc.txt', 'w')
        file.writelines(classification_report(self.y_test, predictions))
        file.close()


        # clf = RandomForestClassifier(n_estimators=1000, criterion="entropy", min_samples_split=15)
        # print (clf.fit(self.x_train, self.y_train)).score(self.x_train, self.y_train)
        # clf_probs = clf.predict_proba(self.x_test)
        # score = log_loss(self.y_test, clf_probs)
        # s = clf.score(self.x_test, self.y_test)
        # print 'The accuracy is: ' + str(s)
        # print 'The log loss is: ' + str(score)

    def evaluation(self):
        num_folds = 10
        num_instances = len(self.x_train)
        seed = 7
        scoring = 'accuracy'
