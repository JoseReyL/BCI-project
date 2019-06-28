#!/usr/bin/env python3
# Set up imports and paths
import sys, os
# Get the helper functions for connecting to the buffer
try:     pydir=os.path.dirname(__file__)
except:  pydir=os.getcwd()
sigProcPath = os.path.join(os.path.abspath(pydir),'../../python/signalProc')
sys.path.append(sigProcPath)
import bufhelp
import pickle

# connect to the buffer, if no-header wait until valid connection
ftc,hdr=bufhelp.connect()

### Variables ###
trialLength = 2000  # time (ms) lenght of recording for each event
dname  ='training_data_ErrPs'   # name for the data dile created 


# grab data after every t:'stimulus.start_feedback' event until we get a {t:'stimulus.training' v:'end'} event
data, events, stopevents, pending = bufhelp.gatherdata("stimulus.start_feedback",trialLength,("stimulus.training","end"), milliseconds=True)
# save the calibration data
with open(os.path.join(os.getcwd(),dname+'.pk'), 'wb') as f:
    pickle.dump({"events":events,"data":data,'hdr':hdr}, f)
