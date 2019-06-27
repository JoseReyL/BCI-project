#!/usr/bin/env python3
# Set up imports and paths
import sys, os
from time import sleep, time
# Get the helper functions for connecting to the buffer
try:     pydir=os.path.dirname(__file__)
except:  pydir=os.getcwd()
sigProcPath = os.path.join(os.path.abspath(pydir),'../../python/signalProc')
sys.path.append(sigProcPath)
import preproc
import bufhelp
import pickle
import numpy as np
import random

# connect to the buffer, if no-header wait until valid connection
ftc,hdr=bufhelp.connect()

### Variables ###
im_length = 3000
classifier_right_name =  'classifier_right'
classifier_left_name  =  'classifier_left'
DEBUG = True    # True for debugging, False for real experiment
n_symbols = 4   # 0 - left, 1 - right, 2 - both, 3 - none (no movement) 
debug_predictions = [0,0,0,0,0,0,0,3,0,1,2,3,0,1,2,3]

##### Loadind classifier pickle file ######

f = open(os.path.join(pydir, classifier_right_name + '.pk' ), 'rb')
classifier_right = pickle.load(f)

if verbose: print('--right')

f = open(os.path.join(pydir, classifier_left_name + '.pk' ), 'rb')
classifier_left = pickle.load(f)

if verbose: print('--left')

if verbose: print('Classifiers loaded #')

# invert the value dict to get a key->value map
ivaluedict = { k:v for k,v in valuedict.items() }

# clear event history
pending = []
while True:
    if not DEBUG:
        # wait for data after a trigger event
        #  exitevent=None means return as soon as data is ready
        #  N.B. be sure to propogate state between calls
        data_im, events_im, stopevents, pending = bufhelp.gatherdata(["stimulus.target", "stimulus.last_target"],im_length,[], milliseconds=True)

        # get all event type labels
        event_types = [e.type for e in events_im]
        print(event_types)
        # get all event values
        event_values = [e.value[0] for e in events_im]
        print(event_values)

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

                
        data = np.reshape(data, (1,-1))
                
        prediction_right = classifier_right.predict(data)
        prediction_left  = classifier_left.predict(data)
                
        pred = [prediction_left, prediction_right]
        prediction0 = [np.round(prediction_left).astype(int), np.round(prediction_right).astype(int)]
        prediction = [np.round(prediction_left-0.6).astype(int), np.round(prediction_right-0.3).astype(int)]
        prediction_int  = -1

        # combine predictions from classifiers

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

        # stop processing if needed
        if "stimulus.last_target" in event_types :
            break

    else:
        # wait for data after a trigger event
        #  exitevent=None means return as soon as data is ready
        #  N.B. be sure to propogate state between calls
        data_im, events_im, stopevents, pending = bufhelp.gatherdata(["stimulus.target", "stimulus.last_target"],im_length,[], milliseconds=True)
        print('asd')
        # get all event type labels
        event_types = [e.type for e in events_im]
        print(event_types)
        # get all event values
        event_values = [e.value[0] for e in events_im]
        print(event_values)

        # send premade prediction
        bufhelp.sendEvent("classifier.prediction",debug_predictions[0])
        print(debug_predictions[0])
        debug_predictions = debug_predictions[1:]

        # stop processing if needed
        if "stimulus.last_target" in event_types :
            break

