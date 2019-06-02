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

im_length = 3000
Errp_length = 1000
dname  ='training_data_Errps'
cname = 'clsfr'
DEBUG = True    # True for debugging, False for real experiment
n_symbols = 4   # 0 - left, 1 - right, 2 - both, 3 - none (no movement) 
debug_predictions = [0,0,0,0,0,0,0,3,0,1,2,3,0,1,2,3]

Data=[]
Events=[]
#for x in range(40):
#    debug_predictions.append(random.randint(0, n_symbols-1))

#load the trained classifier
if os.path.exists(cname+'.pk'):
    f     =pickle.load(open(cname+'.pk','rb'))
    goodch     = f['goodch']
    freqbands  = f['freqbands']
    valuedict  = f['valuedict']
    classifier = f['classifier']
    fs         = f['fSample']

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
        print('asd')
        # get all event type labels
        event_types = [e.type for e in events_im]
        print(event_types)
        # get all event values
        event_values = [e.value[0] for e in events_im]
        print(event_values)
        ########################
        ## apply preprocessing and classifier 
        ###################


        bufhelp.sendEvent("classifier.prediction",prediction)
        print(prediction)

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

        bufhelp.sendEvent("classifier.prediction",debug_predictions[0])
        print(debug_predictions[0])
        debug_predictions = debug_predictions[1:]

        # stop processing if needed
        if "stimulus.last_target" in event_types :
            break

