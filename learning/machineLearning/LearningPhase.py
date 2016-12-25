import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import log_loss

class learningPhase:

    def __init__(self, featuresMat, tagsVec):
        self.featuresMat = np.asmatrix(featuresMat, dtype=float)
        self.tagsVec = tagsVec

    def DivideToTrainAndTest(self, trainSize, isValitation):
        row = int(self.featuresMat.shape[0] * trainSize / 100)
        self.x_train = self.featuresMat[:row, :]
        self.y_train = self.tagsVec[:row]
        self.x_test = self.featuresMat[row:, :]
        self.y_test = self.tagsVec[row:]
        return self.x_train, self.y_train, self.x_test, self.y_test

    def implementLearningMethod(self):
        params = self.DivideToTrainAndTest(70, False)
        clf = RandomForestClassifier(n_estimators=1000, criterion="entropy", min_samples_split=15)
        print (clf.fit(params[0], params[1])).score(params[0], params[1])
        clf_probs = clf.predict_proba(params[2])
        score = log_loss(params[3], clf_probs)
        s = clf.score(params[2], params[3])
        print 'The accuracy is: ' + str(s)
        print 'The log loss is: ' + str(score)