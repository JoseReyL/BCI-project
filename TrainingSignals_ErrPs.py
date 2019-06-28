from scipy.signal import spectrogram, welch
import numpy as np
import pickle, glob
import sys,os
from scipy.fftpack import fft
import sklearn
import sklearn.linear_model
from sklearn import preprocessing


try:     pydir=os.path.dirname(__file__)
except:  pydir=os.getcwd()

Path_FieldTrip = os.path.join(os.path.abspath(pydir),'../../dataAcq/buffer/python')
sys.path.append(Path_FieldTrip)
import FieldTrip

sigProcPath = os.path.join(os.path.abspath(pydir),'../../python/signalProc')
sys.path.append(sigProcPath)
import preproc

### Variables ###
data_folder = 'error_potentials'    # folder containing training data
spatialfilter='car' #type of spatial filter
freqbands    = [8, 10, 28, 30]  # frequency bands for the spectral filter
cname_time = 'ErrP_clf_time'    # name of the time classifier
treshold_time = 0.4431697721955611 # optimal threshold for the time classifier (precomputed)
cname_freq = 'ErrP_clf_freq'    # name for the frequency classifier
treshold_freq = 0.45619815088221327 # optimal threshold for the frequency classifier (precomputed)


# grouping all the ErrPs data files
dataPath = os.path.join(os.path.abspath(pydir),data_folder)
exp = []
exp_name = []
for file in os.listdir(dataPath):
    if file == '.ipynb_checkpoints': continue # exception for non data file
    print(file)
    f = open(os.path.join(dataPath,file), 'rb')
    exp_name.append(file)
    exp.append(pickle.load(f))
    
# for discriminate correct Errp from incorrect 
bad = []
good = []

# counters
bad_count = 0
good_count = 0

# Data preprocessing 
for n_exp in range(len(exp)):
    print(' ***********   Experiment  '+exp_name[n_exp]+'   *********** ')
    data           =   np.array(exp[n_exp]['data'])   #data support variable
    data           =   np.transpose(data)
    # Take only the first 1s of EEG recording (We originally took 2s but 1s is enough)
    data = data[:,0:250,:]
    # 1: detrend
    data        = preproc.detrend(data)
    # 2: bad-channel removal
    goodch = np.arange(31) # all plugged-in electrodes of the cap
    data         = data[goodch,:,:]
    # 3: apply spatial filter
    data         = preproc.spatialfilter(data,type=spatialfilter)
    # 4 & 5: spectral filter
    data         = preproc.fftfilter(data, 1, freqbands, exp[n_exp]['hdr'].fSample)    
    # 6 : bad-trial removal
    goodtr, badtr = preproc.outlierdetection(data,dim=2)
    data = data[:,:,goodtr]
    
    n_events = goodtr
    for i, event in enumerate(n_events):
        
        if exp[n_exp]['events'][event].value[0] == '0':
            bad_count = bad_count + 1
            bad.append(data[:,:,i])
        
        
        if exp[n_exp]['events'][event].value[0] == '1':
            good_count = good_count + 1
            good.append(data[:,:,i]) 
        
        
bad_errp    =   np.array(bad)
good_errp   =   np.array(good)

# Concatenate all the trials
all_Data = np.concatenate((good_errp, bad_errp), axis=0)

# constructing labels (0 -> wrong Errp, 1 -> correct Errp)
y_g = np.ones((len(good_errp),),dtype=int)
y_b = np.zeros((len(bad_errp),),dtype=int)
y = np.concatenate((y_g, y_b), axis=0)


## Time features - classifiers

#reshape data to be in trials x features
X_train_2d = np.reshape(all_Data,(all_Data.shape[0],all_Data.shape[1]*all_Data.shape[2]))

# normalizer
scaler_time = preprocessing.StandardScaler()

scaler_time.fit(X_train_2d)

clsfr_time = sklearn.linear_model.RidgeCV(store_cv_values=True)

clsfr_time.fit(scaler_time.transform(X_train_2d),y)

# save the trained classifer and normalizer
print('Saving clsfr to : %s'%(cname+'.pk'))
pickle.dump({'classifier':clsfr_time,'spatialfilter':spatialfilter,'freqbands':freqbands,'goodch':goodch,'treshold':treshold_time},open(cname_time+'.pk','wb'))
pickle.dump({'normalizer':scaler_time},open(cname_time + '_Norm.pk','wb'))



## Power spectral density features - classifiers

fs = 250    # sampling frequency

# Welch psd

f, psd = welch(all_Data,
            fs= fs  ,           # sample rate
            window='hanning',     # apply a Hanning window before taking the DFT
            nperseg= 125)   

# select frequency bands of interests (from 8 to 30 Hz)
f_8 = f > 7
f_30 =f < 31
f_8_30 = f_8 & f_30

psd = psd[:,:,f_8_30]

#reshape data to be in trials x features
X_train_2d = np.reshape(psd,(psd.shape[0],psd.shape[1]*psd.shape[2]))

# Standardize features to mean 0 and unit variance
scaler_f = preprocessing.StandardScaler()

scaler_f.fit(X_train_2d)

clsfr_f = sklearn.linear_model.RidgeCV(store_cv_values=True)

clsfr_f.fit(scaler_f.transform(X_train_2d),y)

# save the trained classifer
print('Saving clsfr to : %s'%(cname+'.pk'))
pickle.dump({'classifier':clsfr_f,'spatialfilter':spatialfilter,'freqbands':freqbands,'goodch':goodch, 'treshold':treshold_freq},open(cname_freq+'.pk','wb'))
pickle.dump({'normalizer':scaler_f},open(cname_freq + '_Norm.pk','wb'))
