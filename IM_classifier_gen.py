#IM_classifier_gen.py

# This program reads the data from the generated data files in the sessions, preprocess them and trains a classifier to be applied
# in new data, for the program classifier.py


# Imported libraries
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold
import numpy as np
import sys
import os
import pickle


# Importing FieldTrip, necessary to read the events from the generated files
sys.path.append(os.path.join(os.path.abspath(''),'buffer_bci-master/dataAcq/buffer/python'))
import FieldTrip

# Importing libraries to preprocess it 
sys.path.append(os.path.join(os.path.abspath(''),'buffer_bci-master/python/signalProc'))
import preproc


verbose = True         # If true, the terminal will display much more information, useful to debug it


init  = 16             # Files are numerated, this lines select which files are chosem, both numbers included
final = 21



exp = [0]*init   # This variable will contain the values of the data files for each experiment

for i in range(init, final +1):
    file = 'data/training_data_imagined_movement-'   # Name and path of the files generated in the training sessions
    if verbose: print(i, file+str(i)+'.pk')
    f = open(file+str(i)+'.pk', 'rb')                # File variable
    exp.append(pickle.load(f))						 # The data is appendend to the experiment array



# Each one of this variable will contain processed data, which will be also classified depending on the activity

left_hand_mov   =  []
right_hand_mov  =  []
both_hands_mov  =  []
no_hand_mov     =  []



for n_exp in range(init,final+1):                                                          # We iterate over all data gathered
    if verbose: print(' ***********   Experiment  '+str(n_exp)+'   *********** ')
    
    if verbose: print(np.array(exp[n_exp]['data']).shape)
    
    data = np.array(exp[n_exp]['data'])                                                     # Support variable that contains the data
    data           =   np.transpose(data)                                             
    data           =   preproc.detrend(data);                                               # Preprocessing functions, for more info check the report
    data           =   preproc.spatialfilter(data, type = 'car')
    data, freqs    =   preproc.powerspectrum(data,dim = 1,fSample=exp[i]['hdr'].fSample);   
    data,freqIdx   =   preproc.selectbands(data,dim=1,band=[6,13,15,32],bins=freqs);
     
    
    if verbose: print(data.shape)
        
    
    n_events = data.shape[2]

    for event in range(n_events):
        
        if verbose: print(exp[n_exp]['events'][event].value[0])         # Verbose option, for debugging
        
        if exp[n_exp]['events'][event].value[0] == 0:                   # If the event has been recorded for left activity is saved in the left array activity
            if verbose: print('left')
            left_hand_mov.append(data[:,:,event])
        
        
        if exp[n_exp]['events'][event].value[0] == 1:                   # Same for the right data
            if verbose: print('right')
            right_hand_mov.append(data[:,:,event])
        
            
        if exp[n_exp]['events'][event].value[0] == 2:                  # Both
            if verbose: print('both')
            both_hands_mov.append(data[:,:,event])
            
        if exp[n_exp]['events'][event].value[0] == 3:                  # None
            if verbose: print('None')
            no_hand_mov.append(data[:,:,event])
           

# We turn the arrays into numpy arrays, more comfortable to use
left_hand_mov    =   np.array(left_hand_mov)
right_hand_mov   =   np.array(right_hand_mov)
both_hands_mov   =   np.array(both_hands_mov)
no_hand_mov      =   np.array(no_hand_mov)




#Dictionary that contains all the preprocessed data
power_spectrum = {'left':left_hand_mov, 'right':right_hand_mov, 'both':both_hands_mov, 'no':no_hand_mov}


# We will use the KFold technique to calculate a better average performance for the classifiers when dealing with new data
kfold = KFold(12, shuffle = True)
kfold.split(X);


######## Classifier training ########

# To train the classifiers, we split the data into activity and no activity for each side, both is considered activity

# X contains the spectrums for right activity and no activity
Xleft = np.vstack((power_spectrum['left'], power_spectrum['both'], power_spectrum['no']))
Xleft.resize(Xleft.shape[0], Xleft.shape[1]*Xleft.shape[2])


# Y is the values for each spectrum, 1 for activity, 0 for no activity
Yleft = [1]*power_spectrum['left'].shape[0] + [1]*power_spectrum['both'].shape[0] + [0]*power_spectrum['no'].shape[0]
Yleft = np.array(Yleft)



#as before but applied to the right data
Xright = np.vstack((power_spectrum['right'], power_spectrum['both'], power_spectrum['no']))
Xright.resize(Xright.shape[0], Xright.shape[1]*Xright.shape[2])

Yright = [1]*power_spectrum['right'].shape[0] + [1]*power_spectrum['both'].shape[0] + [0]*power_spectrum['no'].shape[0]
Yright = np.array(Yright)



######## Classifier training ########


classifier = RidgeCV()     

for train, test in kfold.split(Xleft):
    
    if verbose: print('\n\nTrain:',train, '\nTest:', test)       # Verbose option, useful for debugging
    if verbose: print(Xleft[train].shape)						 # Verbose option, useful for debugging
        
    classifier.fit(Xleft[train], Yleft[train])                   # The classifier is trained
    
    if verbose: print('------')
    
    if verbose: print(classifier.predict(np.round(Xleft[test]))-Yleft[test])     # Verbose option, useful for debugging
    
    X_test = classifier.predict(np.round(Xleft[test]))          # We get the real values for the test data, both for X and Y
    Y_test = Yleft[test]                                        
    

    #Variables to calculate the metrics of the classifiers
    true = 0
    false = 0
    avg_performance = []
    
    for i in range(len(Xleft[test])):
        
        if verbose: print(int(np.round(X_test[i])), Y_test[i], int(np.round(X_test[i])) == Y_test[i])   # Verbose option
        

        #We check if the classifier is right or has missclassified it
        if np.round(X_test[i]) == Y_test[i]:
            true  = true  + 1
        if np.round(X_test[i]) != Y_test[i]:    
            false = false + 1
    
    if verbose: print('True: ', true, '  False: ', false, '   '+ str(true/(true+false)*100)[:4] +'%')
    
    avg_performance.append(true/(true+false)*100)                # The classifier accuracy for each split of the data is saved for calculating the average
    
pickle.dump(classifier, open( "classifier_left.pk", "wb" ) )     # The classifier variable is saved into a file

if verbose: print('\n\nAvg Performance: ' + str(np.mean(per)))   # Verbose option, the average performance




# Same as the last part but for data of right vs no movement


classifier = RidgeCV()

for train, test in kfold.split(Xright):
    
    if verbose: print('\n\nTrain:',train, '\nTest:', test)
    if verbose: print(Xright[train].shape)
        
    classifier.fit(Xright[train], Yright[train])
    
    if verbose: print('------')
    
    if verbose: print(classifier.predict(np.round(Xright[test]))-Yright[test])
    
    X_test = classifier.predict(np.round(Xright[test]))
    Y_test = Yright[test]
    
    
    true = 0
    false = 0
    avg_performance = []
    
    for i in range(len(Xright[test])):
        
        if verbose: print(int(np.round(X_test[i])), Y_test[i], int(np.round(X_test[i])) == Y_test[i])
        
        if np.round(X_test[i]) == Y_test[i]:
            true  = true  + 1
        if np.round(X_test[i]) != Y_test[i]:    
            false = false + 1
    
    print('True: ', true, '  False: ', false, '   '+ str(true/(true+false)*100)[:4] +'%')
    avg_performance.append(true/(true+false)*100)
    
pickle.dump(classifier, open( "classifier_right.pk", "wb" ) )

if verbose: print('\n\nAvg Performance: ' + str(np.mean(per)))