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
from learning_base import LearningBase
from keras.callbacks import EarlyStopping
from keras.models import load_model
import os

class DeepLearning(LearningBase):

    def runNetwork(self,test_size = 0.3, output_activation='sigmoid', output_size=1,
                   load_clf_file_name = None, save_clf_file_name = None, random_state = None):
        self.DivideToTrainAndTest(test_size, random_state=random_state)
        # create model
        print self.x_train.shape[1]
        if load_clf_file_name == None or (not os.path.isfile(load_clf_file_name+'deep.h5')
                                          or os.stat(load_clf_file_name+'deep.h5').st_size == 0):
            early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=50,mode='min', verbose=1)
            self.classifier = Sequential()
            self.classifier.add(Dense(300, activation="relu", kernel_initializer="he_normal", input_dim=self.x_train.shape[1]))
            self.classifier.add(Dropout(0.2))
            self.classifier.add(Dense(100, init='he_normal', activation='relu', W_regularizer=l2(0.1)))
            self.classifier.add(Dropout(0.2))
            self.classifier.add(Dense(output_size, init='uniform', activation=output_activation, W_regularizer=l2(0.01)))

            # self.classifier.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

            # Fit the model
            if(output_activation == 'softmax'):
                self.classifier.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
                self.y_train = keras.utils.to_categorical(self.y_train, num_classes=max(self.y_train)+1)
                self.y_test = keras.utils.to_categorical(self.y_test, num_classes=max(self.y_test)+1)
            else:
                self.classifier.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

            self.classifier.fit(self.x_train, self.y_train,validation_split=0.1 ,callbacks=[early_stopping], epochs=1000, batch_size=10, verbose=2)
        else:
            self.classifier = self.load_clf(load_clf_file_name+'deep.h5')

        if save_clf_file_name != None:
            self.save_clf(save_clf_file_name+'deep.h5')

        return self.classifier

    def plotROCcurve(self, plot_file_name='ROC_curve.png'):
        scores = self.classifier.predict(self.x_test)
        test_fpr, test_tpr, thresholds = metrics.roc_curve(self.y_test, scores)
        aucTest = numpy.trapz(test_tpr, test_fpr)

        scores = self.classifier.predict(self.x_train)
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

    def save_clf(self, file_name):
        self.classifier.save(filepath=file_name)

    def load_clf(self, file_name):
        return load_model(file_name)

