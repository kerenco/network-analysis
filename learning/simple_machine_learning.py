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
from learning_base import LearningBase
from sklearn.externals import joblib
import os


class SimpleMachineLearning (LearningBase):


    def implementLearningMethod(self, algo,test_size=0.3, load_clf_file_name = None, save_clf_file_name = None,
                                random_state=None):
        self.DivideToTrainAndTest(test_size, random_state=random_state)
        if load_clf_file_name == None or (not os.path.isfile(load_clf_file_name+algo+'.pkl')
                                          or os.stat(load_clf_file_name+algo+'.pkl').st_size == 0):
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
            self.classifier = clf.fit(self.x_train, np.array(self.y_train).reshape(-1, ))

        else:
            self.classifier = self.load_clf(load_clf_file_name+algo+'.pkl')

        if save_clf_file_name != None:
            self.save_clf(save_clf_file_name+algo+'.pkl')

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

    def save_clf(self, file_name):
        joblib.dump(self.classifier, file_name)

    def load_clf(self, file_name):
        return joblib.load(file_name)







