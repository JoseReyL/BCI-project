
# Classifier.py
#
# The goal of the program is to load a pretrained classifier, when the program detects the signal to start collecting
# signal, this gets processed and passed to the loaded classifier which returns a numerical value for the detected activity


#Loading libraries

import pickle
import numpy as np
import sys
import os


# Loading the preproc and bufhelp libraries, preproc provides the processing functions for the signal data
# bufhelp will provide the connection to the buffer, where al programs can pass events

Path_Preproc = "/../python/signalproc"         # This variable contains the path to the folder where the libraries files are
sys.path.append(os.getcwd() + Path_Preproc)    # This allows to load the libraries this way
import preproc                                 # Loading
import bufhelp


Path_FieldTrip = "../dataAcq/buffer/python"    # Variable which contains the path to the Fieldtrip library 
sys.path.append(os.getcwd() + Path_FieldTrip)  
import FieldTrip

ftc,hdr=bufhelp.connect()                     #This functions connects the program to the buffer, and the passing of messages

##### Variables #####

verbose = True                                # For True values, the terminal will detail what it's happening inside the program

im_length = 3000                              # Length of time that the signal will be collected
# This time should be the same as the time used to collect the data to train the classifier, 
#otherwise, the sizes of the classifier training and the processed signal wont match


classifier_right_name =  'classifier_right'   # Name of the file with the classifier for the right hand, must be of pk type
classifier_left_name  =  'classifier_left'    # Name of the file with the classifier for the left hand, must be of pk type




##### Loadind classifier pickle files ######

if verbose: print('Loading classifier file....')   # Information in terminal, verbose option

f = open(classifier_right_name + '.pk', 'rb')      # This variable contains a file sata type, which corresponds to the right classifier
classifier_right = pickle.load(f)                  # Now the 

if verbose: print('--right')                       # Information in terminal, verbose option

f = open(classifier_left_name + '.pk', 'rb')
classifier_left = pickle.load(f)

if verbose: print('--left')                        # Information in terminal, verbose option

if verbose: print('Classifiers loaded #')          # Information in terminal, verbose option





##### Gathering data from the events ######


# In this part the programs enters in a loop, it will wait for events telling it to collect data, it'll process it and wait for 
# events again untill the program is closed


while True:

        if verbose: print('Collecting data...')   # Information in terminal, verbose option

        data, events_im, stopevents, pending = bufhelp.gatherdata(["stimulus.target", "stimulus.last_target"],im_length,[], milliseconds=True)



        data = np.array(data)                       # data contains the signal sampled, 750 samples for 32 channels
        data_rec = np.copy(data)

        if verbose: print(events_im[0].value)       # Information in terminal, verbose option, for debugging purposes
        if verbose: print(data.shape)               # Information in terminal, verbose option, for debugging purposes
        
        data = data[:,:,:]                   
        
        if verbose: print(data.shape)               # Information in terminal, verbose option, for debugging purposes

        data           =   np.array(data)   #data support variable
        data           =   np.transpose(data)
        data           =   preproc.detrend(data);                                          # Preprocessing operations, more detailed in the report
        data           =   preproc.spatialfilter(data, type = 'car')                       #      "                  
        data, freqs    =   preproc.powerspectrum(data,dim = 1,fSample= 250);               #      "       sample information included in the hdr, must be changed if it changes for it to work
        data,freqIdx   =   preproc.selectbands(data,dim=1,band=[6,13,15,32],bins=freqs);   #      "       the bands selected here also should be the same as the chosen one in the classifier file             


        if verbose: print(data.shape)               # Information in terminal, verbose option, for debugging purposes

        data = np.reshape(data, (1,-1))             # Data now, is an bunch of array containing the power spectrum of every channel in the selected frequencies (#ch, #freq), in this line all those arrays become one of size (1, #ch * #freq)
        
        prediction_right = classifier_right.predict(data)    # The freq informations is now passed to the classifier, each one yielding a float value
        prediction_left  = classifier_left.predict(data)
        
        pred = [prediction_left, prediction_right]                        # The predictions are put into an array, for debugging reasons, this isn't what will be passed
        prediction = [np.round(prediction_left).astype(int), np.round(prediction_right).astype(int)]    # In this array the predictions are rounded, as the expected values are 0,1 for each classifier but the outputs are float, they need to be rounded
        

        # In the following lunes, the conversion is made from a the array to a single int value, easier to pass as an event value
        # 0 - left [1, 0]   1- right [0, 1]   2 - both [1, 1]    3 - none [0, 0]

        if prediction == [0, 0]:       # None
                prediction_int = 3
        if prediction == [1, 0]:       # Left Hand
                prediction_int = 0
        if prediction == [0, 1]:       # Right Hand
                prediction_int = 1
        if prediction == [1, 1]:       # Both Hands
                prediction_int = 2

        if verbose: print(pred, prediction)        # Information in terminal, verbose option, for debugging purposes


        bufhelp.sendEvent('classifier.prediction', str(prediction_int))   # After the classifier has done its job, send an event with ethe expected result as value


        # This iteration has ended, now the classifier goes back to the biggining of the loop and waits for more events

