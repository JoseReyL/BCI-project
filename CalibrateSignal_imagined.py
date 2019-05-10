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

trialLength = 3000
dname  ='training_data_imagined_movement'
cname = 'classifier_imagined_movement'


# grab data after every t:'stimulus.target' event until we get a {t:'stimulus.training' v:'end'} event
data, events, stopevents, pending = bufhelp.gatherdata("stimulus.target",trialLength,("stimulus.training","end"), milliseconds=True)
# save the calibration data
pickle.dump({"events":events,"data":data,'hdr':hdr}, open(dname+'.pk','wb'))#N.B. to pickle open in binary mode