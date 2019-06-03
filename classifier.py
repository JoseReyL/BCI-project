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

##### Variables #####

verbose = True

trialLength = 1000

classifier_right_name =  'classifier_right.pk'
classifier_left_name  =  'classifier_left.pk'


##### Loadind classifier pickle file ######

if verbose: print('Loading classifier file....')

f = open(classifier_rigth_name + '.pk', 'rb')
classifier_rigth = pickle.load(f)

if verbose: print('--right')

f = open(classfifier_left_name + '.pk', 'rb')
classifier_left = pickle.load(f)

if verbose: print('--left')

if verbose: print('Classifiers loaded #')


##### Gathering data from the events ######

while True:

	if verbose: print('Collecting data...')

	bufhelp.gatherdata()

	data, events, stopevents, pending = bufhelp.gatherdata("second",trialLength,("end_second","end"), milliseconds=True)


	prediction_right = classifier_right.predict()
	prediction_left  = classfier_left.predict()

	prediction 		= [prediction_left, prediction_right]
	prediction_int  = 0


	if prediction == [0 0]:
		prediction_int = 4
	if prediction == [1 0]:
		prediction_int = 0
	if prediction == [0 1]:
		prediction_int = 1
	if prediction == [1 1]:
		prediction_int = 3

	bufhelp.sendevent('prediction', str([prediction_left, prediction_right]))




