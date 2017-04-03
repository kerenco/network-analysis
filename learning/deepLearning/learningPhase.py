import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense,Dropout
import numpy
from sklearn import metrics
from sklearn.model_selection import train_test_split
from keras.regularizers import l2
import pandas as pd
import seaborn as sn
import keras

class learningPhase:

    def __init__(self, featuresMat, tagsVec):
        self.featuresMat = np.asmatrix(featuresMat, dtype=float)
        self.tagsVec = tagsVec

    def DivideToTrainAndTest(self, testSize):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.featuresMat, self.tagsVec, test_size=testSize)

    def runNetwork(self,test_size = 0.3, output_activation='sigmoid', output_size=1):
        self.DivideToTrainAndTest(test_size)
        # create model
        self.model = Sequential()
        self.model.add(Dense(90, activation="relu", kernel_initializer="he_normal", input_dim=self.x_train.shape[1]))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(30, init='he_normal', activation='relu', W_regularizer=l2(0.2)))
        self.model.add(Dropout(0.5))
        # self.model.add(Dense(20, init='he_normal', activation='relu', W_regularizer=l2(0.01)))
        # self.model.add(Dropout(0.2))
        self.model.add(Dense(output_size, init='uniform', activation=output_activation, W_regularizer=l2(0.01)))

        # self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the model
        if(output_activation == 'softmax'):
            self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            self.y_train = keras.utils.to_categorical(self.y_train, num_classes=max(self.y_train)+1)
            self.y_test = keras.utils.to_categorical(self.y_test, num_classes=max(self.y_test)+1)
        else:
            self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.model.fit(self.x_train, self.y_train, epochs=1000, batch_size=100, verbose=1)

        return self.model


    def plotROCcurve(self, plot_file_name='ROC_curve.png'):
        scores = self.model.predict(self.x_test)
        test_fpr, test_tpr, thresholds = metrics.roc_curve(self.y_test, scores)
        aucTest = numpy.trapz(test_tpr, test_fpr)

        scores = self.model.predict(self.x_train)
        train_fpr, train_tpr, thresholds = metrics.roc_curve(self.y_train, scores)
        aucTrain = numpy.trapz(train_tpr, train_fpr)


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
        plt.savefig(plot_file_name)

    def evaluate_AUC_test(self):
        scores = self.model.predict(self.x_test)
        fprVal, tprVal, thresholds = metrics.roc_curve(self.y_test, scores)
        aucVal = numpy.trapz(tprVal, fprVal)
        return aucVal

    def evaluate_AUC_train(self):
        scores = self.model.predict(self.x_train)
        fprVal, tprVal, thresholds = metrics.roc_curve(self.y_train, scores)
        aucVal = numpy.trapz(tprVal, fprVal)
        return aucVal

    def evaluate_confusion_metric_test(self):
        y_pred = self.model.predict(self.x_test)
        y_pred = [np.argmax(lst) for lst in y_pred]
        y_true = [np.argmax(lst) for lst in self.y_test]
        confusion_matrix_result = metrics.confusion_matrix(y_true,y_pred)
        confusion_matrix_result = confusion_matrix_result.astype('float') / confusion_matrix_result.sum(axis=1)[:, np.newaxis]
        return confusion_matrix_result

    def evaluate_confusion_metric_train(self):
        y_pred = self.classifier.predict(self.x_train)
        y_true = [int(i) for i in self.y_train]
        confusion_matrix_result = metrics.confusion_matrix(y_true, y_pred)
        print confusion_matrix_result
        return confusion_matrix_result

    def plot_confusion_matrix(self, cm, classes,
                              normalize=True,
                              title='Confusion matrix',
                              plot_file_name='confusion matrix.png'):

        if (normalize):
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

        df_cm = pd.DataFrame(cm, index=[i for i in classes],
                             columns=[i for i in classes])

        print normalize


        plt.figure()
        sn.heatmap(df_cm, annot=True)
        plt.title(title)
        plt.savefig(plot_file_name)




# from keras.models import Sequential
# from keras.layers import Dense,Dropout
# import numpy
# from sklearn import metrics
# from sklearn.model_selection import train_test_split
# from keras.regularizers import l2
#
# location_classifications = ['Cytosol', 'Nucleus', 'Membrane', 'Vesicles', 'Ribosomes', 'Extracellular']
# function_classifications = ['Adapter', 'Kinase', 'Receptor', 'TF', 'Ligand']
# f = open('AUC_function.txt','w')
# f.write('deep\n')
# for classification in function_classifications:
#     f.write(classification+', ')
#     # load pima indians dataset
#     dataset = numpy.loadtxt("features/"+classification+"_matrix.txt")
#     # split into input (X) and output (Y) variables
#     X = dataset[:,1:]
#     Y = numpy.loadtxt("tags/"+"signaling_pathways_tags_"+classification+".txt")
#     x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.4)
#
#     # create model
#     model = Sequential()
#     model.add(Dense(35, input_dim=x_train.shape[1], init='he_normal', activation='relu'))
#     model.add(Dropout(0.2))
#     model.add(Dense(35, init='he_normal', activation='relu', W_regularizer=l2(0.01)))
#     model.add(Dropout(0.2))
#     model.add(Dense(1, init='uniform', activation='sigmoid', W_regularizer=l2(0.01)))
#     # model = Sequential()
#     # model.add(Dense(80, input_dim=X.shape[1], init='he_normal', activation='relu'))
#     # #model.add(Dense(80, init='uniform', activation='relu'))
#     # model.add(Dense(1, init='he_normal', activation='sigmoid'))
#
#     # Compile model
#     model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
#
#     # Fit the model
#     model.fit(x_train, y_train, nb_epoch=1000, batch_size=10, verbose=0)
#
#     # evaluate the model
#     scores = model.evaluate(x_test, y_test)
#     #print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
#
#     scores=model.predict(x_test)
#     fprVal, tprVal, thresholds = metrics.roc_curve(y_test, scores)
#     aucVal= numpy.trapz(tprVal, fprVal)
#     print [round(x) for x in scores]
#     print 'AUC TEST: ', aucVal
#     f.write(str(aucVal)+'\n')
# f.close()

    # train_scores = model.predict(x_train)
    # fprVal, tprVal, thresholds = metrics.roc_curve(y_train, train_scores)
    # aucVal = numpy.trapz(tprVal, fprVal)
    # print [round(x) for x in train_scores]
    # print 'AUC TRAIN: ', aucVal


