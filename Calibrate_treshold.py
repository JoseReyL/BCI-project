from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold
import pickle
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys
import os



Path_Preproc = "/../python/signalproc"
print(os.getcwd() + Path_Preproc)
sys.path.append(os.getcwd() + Path_Preproc)
import preproc
import bufhelp


Path_FieldTrip = "../dataAcq/buffer/python"
sys.path.append(os.getcwd() + Path_FieldTrip)
import FieldTrip

ftc,hdr=bufhelp.connect()

##### Variables #####

verbose = True
left_t_0 = 0.5
right_t_0 = 0.5
lr = 0.3
tresholds = [left_t_0, right_t_0]
counter = 0     # consecutive good prediction
exit_counter = 4        # condition to stop the calibration
im_length = 3000

classifier_right_name =  'classifier_right'
classifier_left_name  =  'classifier_left'

#### Function ########
def treshold_pred(tresholds, raw_predictions):

    assert len(tresholds) == len(raw_predictions)

    residuals = np.empty(raw_predictions.shape)
    predictions = np.empty(raw_predictions.shape) 

    for i in range(len(raw_predictions)):
        residuals[i] = raw_predictions[i] - tresholds[i]

        if raw_predictions[i] > tresholds[i]:
            predictions[i] = 1
        else:
            predictions[i] = 0
    
    return predictions, residuals

def update_rule(predictions, targets, tresholds, residuals,  lr):

    new_tresholds = np.empty(tresholds.shape)

    # check and eventually update
    for hand in range(len(tresholds)):

        if predictions[hand] == targets[hand]:
            new_tresholds[hand] = tresholds[hand]
        else:
            new_tresholds[hand] = tresholds[hand] + lr * residuals[hand]
    
    return new_tresholds




##### Loadind classifier pickle file ######

if verbose: print('Loading classifier file....')

f = open(classifier_right_name + '.pk', 'rb')
classifier_right = pickle.load(f)

if verbose: print('--right')

f = open(classifier_left_name + '.pk', 'rb')
classifier_left = pickle.load(f)

if verbose: print('--left')

if verbose: print('Classifiers loaded #')


##### Gathering data from the events ######

threshold = []

f = open('threshold.pk','wb')

while counter < exit_counter:

        if verbose: print('Collecting data...')

	#bufhelp.gatherdata()

        data, events_im, stopevents, pending = bufhelp.gatherdata(["stimulus.target", "stimulus.last_target"],im_length,[], milliseconds=True)

        data = np.array(data)
        data_rec = np.copy(data)
        print(events_im[0].value)
        print(data.shape)
        data = data[:,:,[15,16,17]]
        print(data.shape)
        data           =   np.array(data)   #data support variable
        data           =   np.transpose(data)
        data           =   preproc.detrend(data);
        data           =   preproc.spatialfilter(data, type = 'car')
        data, freqs    =   preproc.powerspectrum(data,dim = 1,fSample= 250);
        data,freqIdx   =   preproc.selectbands(data,dim=1,band=[6,13,20,27],bins=freqs);

        print(data.shape)

        data = np.reshape(data, (1,-1))
        
        prediction_right = classifier_right.predict(data)
        prediction_left  = classifier_left.predict(data)

        # Set negative prediction to 0
        if prediction_left < 0:
            prediction_left = 0
        if prediction_right < 0:
            prediction_right = 0


        pred = [prediction_left, prediction_right]  # raw prediction of the two classifiers (ridge regression)

        predictions, residuals = treshold_pred(tresholds, pred)

        prediction_int  = -1

        if predictions == [0, 0]:
                prediction_int = 3
        if predictions == [1, 0]:
                prediction_int = 0
        if predictions == [0, 1]:
                prediction_int = 1
        if predictions == [1, 1]:
                prediction_int = 2

        print(pred ,'->', predictions, '->', prediction_int)
        print('true value: ', events_im[0].value)

        if events_im[0].value == 3:
                target = [0, 0]
        if events_im[0].value == 0:
                target =  [1, 0]
        if events_im[0].value == 1 :
                target = [1, 0]
        if events_im[0].value == 2:
                target =  [1, 1]

        print('old treshlds',tresholds)
        tresholds = update_rule(predictions, target, tresholds, residuals, lr)
        print('new treshlds',tresholds)

        if prediction_int == events_im[0].value:
            counter += 1
        else:
            counter = 0

        print('counter',counter)



