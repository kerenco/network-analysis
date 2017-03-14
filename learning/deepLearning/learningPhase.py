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
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.featuresMat, self.tagsVec, test_size=testSize)

    def runNetwork(self,test_size = 0.3):
        self.DivideToTrainAndTest(test_size)
        # create model
        self.model = Sequential()
        self.model.add(Dense(35, input_dim=x_train.shape[1], init='he_normal', activation='relu'))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(35, init='he_normal', activation='relu', W_regularizer=l2(0.01)))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(1, init='uniform', activation='sigmoid', W_regularizer=l2(0.01)))

        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the model
        self.model.fit(self,x_train, self.y_train, nb_epoch=1000, batch_size=10, verbose=0)

        return self.model


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
        scores = model.predict(self.x_test)
        fprVal, tprVal, thresholds = metrics.roc_curve(self.y_test, scores)
        aucVal = numpy.trapz(tprVal, fprVal)
        return aucVal

    def evaluate_AUC_train(self):
        scores = model.predict(self.x_train)
        fprVal, tprVal, thresholds = metrics.roc_curve(self.y_train, scores)
        aucVal = numpy.trapz(tprVal, fprVal)
        return aucVal





from keras.models import Sequential
from keras.layers import Dense,Dropout
import numpy
from sklearn import metrics
from sklearn.model_selection import train_test_split
from keras.regularizers import l2

location_classifications = ['Cytosol', 'Nucleus', 'Membrane', 'Vesicles', 'Ribosomes', 'Extracellular']
function_classifications = ['Adapter', 'Kinase', 'Receptor', 'TF', 'Ligand']
f = open('AUC_function.txt','w')
f.write('deep\n')
for classification in function_classifications:
    f.write(classification+', ')
    # load pima indians dataset
    dataset = numpy.loadtxt("features/"+classification+"_matrix.txt")
    # split into input (X) and output (Y) variables
    X = dataset[:,1:]
    Y = numpy.loadtxt("tags/"+"signaling_pathways_tags_"+classification+".txt")
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.4)

    # create model
    model = Sequential()
    model.add(Dense(35, input_dim=x_train.shape[1], init='he_normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(35, init='he_normal', activation='relu', W_regularizer=l2(0.01)))
    model.add(Dropout(0.2))
    model.add(Dense(1, init='uniform', activation='sigmoid', W_regularizer=l2(0.01)))
    # model = Sequential()
    # model.add(Dense(80, input_dim=X.shape[1], init='he_normal', activation='relu'))
    # #model.add(Dense(80, init='uniform', activation='relu'))
    # model.add(Dense(1, init='he_normal', activation='sigmoid'))

    # Compile model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit the model
    model.fit(x_train, y_train, nb_epoch=1000, batch_size=10, verbose=0)

    # evaluate the model
    scores = model.evaluate(x_test, y_test)
    #print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    scores=model.predict(x_test)
    fprVal, tprVal, thresholds = metrics.roc_curve(y_test, scores)
    aucVal= numpy.trapz(tprVal, fprVal)
    print [round(x) for x in scores]
    print 'AUC TEST: ', aucVal
    f.write(str(aucVal)+'\n')
f.close()

    # train_scores = model.predict(x_train)
    # fprVal, tprVal, thresholds = metrics.roc_curve(y_train, train_scores)
    # aucVal = numpy.trapz(tprVal, fprVal)
    # print [round(x) for x in train_scores]
    # print 'AUC TRAIN: ', aucVal


