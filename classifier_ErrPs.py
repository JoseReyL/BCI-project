from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold
from scipy.signal import spectrogram, welch
import pickle
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys
import os

try:     pydir=os.path.dirname(__file__)
except:  pydir=os.getcwd()    


sigProcPath = os.path.join(os.path.abspath(pydir),'../python/signalProc')
sys.path.append(sigProcPath)


import preproc
import bufhelp


Path_FieldTrip = "../dataAcq/buffer/python"
sys.path.append(Path_FieldTrip)
import FieldTrip

ftc,hdr=bufhelp.connect()

##### Variables #####

verbose = True

recording_lenght = 1000 

TIME = False # choose between time classifier or frequency classifier

classifier_name =  'ErrP_clf_'

DEBUG = False    # True for debugging, False for real experiment
debug_predictions = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]

if TIME :
    classifier_name =  classifier_name + 'time'
else:
    classifier_name =  classifier_name + 'freq'

print(classifier_name)

Normalizer_name  =  classifier_name + '_Norm'


##### Loadind classifier pickle file ######

if verbose: print('Loading classifier file....')

if os.path.exists(classifier_name+'.pk'):
    f     =pickle.load(open(classifier_name+'.pk','rb'))
    goodch     = f['goodch']
    spatialfilter = f['spatialfilter']
    freqbands  = f['freqbands']
    valuedict  = f['valuedict']
    classifier = f['classifier']
    treshold   = f['treshold']
fs = 250    # sample rate of the device
freqs = np.arange(7,31)
goodch = np.arange(31)

if verbose: print('Classifiers loaded #')

if verbose: print('Loading normalizer file....')

if os.path.exists(Normalizer_name+'.pk'):
    f     =pickle.load(open(Normalizer_name+'.pk','rb'))
    scaler     = f['normalizer']

if verbose: print('Classifiers loaded #')

#print(valuedict)

##### Gathering data from the events ######

while True:

    if not DEBUG:



        if verbose: print('Collecting data...')

        #bufhelp.gatherdata()

        data, events_im, stopevents, pending = bufhelp.gatherdata("errp.trigger",recording_lenght,[], milliseconds=True)

        data = np.array(data)

        # get data in correct format
        #data = np.transpose(data) # make it [d x tau]

        data = np.moveaxis(data,1,2)  
        
        print(data.shape)
        
        # 1: detrend
        data = preproc.detrend(data)
        print(data.shape)
        # 2: bad-channel removal (as identifed in classifier training)
        data = data[:,goodch,:]
        print(data.shape)
        # 3: apply spatial filter (as in classifier training)
        data = preproc.spatialfilter(data,type=spatialfilter)
        print(data.shape)
        # 4 & 5: spectral filter (TODO: check fs matches!!)
        data = preproc.fftfilter(data, 1, freqbands, fs)
        print(data.shape)
        
        # Check the type of classifier
        if not TIME :
            # WELCH power spectrum
            f, psd = welch(data,
            fs= fs  ,           # sample rate
            window='hanning',     # apply a Hanning window before taking the DFT
            nperseg= 125)   

            data = psd[:,:,freqs]

        print(freqs)
        print(data.shape)


        # 7: apply the classifier, get raw predictions
        X2d  = np.reshape(data,(data.shape[0],data.shape[1]*data.shape[2])) # sklearn needs data to be [nTrials x nFeatures]
        #fraw = classifier.predict(scaler.transform(X2d))
        fraw = classifier.predict(scaler.transform(X2d))# normalize the features
        # 8: map from fraw to event values  
        # send the prediction events
        for i,f in enumerate(fraw):
            if f < treshold:
                new_p = 0
            else:
                new_p = 1
            print("%d) %f(raw)\n"%(i,new_p))
            bufhelp.sendEvent("errp.prediction",new_p)

    else:

        if verbose: print('Collecting data...')

        data, events_im, stopevents, pending = bufhelp.gatherdata("errp.trigger",recording_lenght,[], milliseconds=True)

        # get all event type labels
        event_types = [e.type for e in events_im]
        print(event_types)
        # get all event values
        event_values = [e.value[0] for e in events_im]
        print(event_values)

        bufhelp.sendEvent("errp.prediction",debug_predictions[0])
        print(debug_predictions[0])
        debug_predictions = debug_predictions[1:]

        # stop processing if needed
        if "stimulus.last_target" in event_types :
            break


