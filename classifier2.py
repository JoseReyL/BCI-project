from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold
import pickle
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys
import os

try:
    pydir = os.path.dirname(__file__)
    print(pydir)
except:
    pydir = os.getcwd()
sigProcPath = os.path.join(os.path.abspath(pydir), '../python/signalProc')
sys.path.append(sigProcPath)
import preproc
import bufhelp


Path_FieldTrip = "../dataAcq/buffer/python"
sys.path.append(Path_FieldTrip)
import FieldTrip

ftc,hdr=bufhelp.connect()

##### Variables #####

verbose = True

im_length = 3000

classifier_right_name =  'classifier_right'
classifier_left_name  =  'classifier_left'

# for debugging
DEBUG = False    # True for debugging, False for real experiment
debug_predictions = [2,0,0,0,0,2,0,0,2,0,0,2,1,3,2,3]



##### Loadind classifier pickle file ######

if verbose: print('Loading classifier file....')

f = open(os.path.join(pydir, classifier_right_name + '.pk' ), 'rb')
classifier_right = pickle.load(f)

if verbose: print('--right')

f = open(os.path.join(pydir, classifier_left_name + '.pk' ), 'rb')
classifier_left = pickle.load(f)

if verbose: print('--left')

if verbose: print('Classifiers loaded #')


##### Gathering data from the events ######

threshold = []

f = open('threshold.pk','wb')

while True:
        if not DEBUG:

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
                
                pred = [prediction_left, prediction_right]
                prediction0 = [np.round(prediction_left).astype(int), np.round(prediction_right).astype(int)]
                prediction = [np.round(prediction_left-0.6).astype(int), np.round(prediction_right-0.3).astype(int)]
                prediction_int  = -1

                

                if prediction == [0, 0]:
                        prediction_int = 3
                if prediction == [1, 0]:
                        prediction_int = 0
                if prediction == [0, 1]:
                        prediction_int = 1
                if prediction == [1, 1]:
                        prediction_int = 2

                print(prediction , prediction_int, pred)

                threshold.append([events_im[0].value, prediction0 , prediction_int, pred, data_rec])

                bufhelp.sendEvent('classifier.prediction', str(prediction_int))


                event_types = [e.type for e in events_im]
                # stop processing if needed
                if "stimulus.last_target" in event_types :
                        #pickle.dump(threshold, f)
                        break
                
        else:

                if verbose: print('Collecting data...')

                data, events_im, stopevents, pending = bufhelp.gatherdata(["stimulus.target", "stimulus.last_target"],im_length,[], milliseconds=True)

                # get all event type labels
                event_types = [e.type for e in events_im]
                print(event_types)
                # get all event values
                event_values = [e.value[0] for e in events_im]
                print(event_values)

                bufhelp.sendEvent("classifier.prediction",debug_predictions[0])
                print(debug_predictions[0])
                debug_predictions = debug_predictions[1:]

                # stop processing if needed
                if "stimulus.last_target" in event_types :
                        break





