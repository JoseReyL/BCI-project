from scipy.signal import spectrogram, welch
import numpy as np
import pickle, glob
import sys,os
from scipy.fftpack import fft
#import linear
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


dataPath = os.path.join(os.path.abspath(pydir),'error_potentials/training_data_ErrPs-')
exp = []
exp_name = []
for i in range(1,15):
    file = '/error_potentials/training_data_ErrPs-'
    if i == 4: continue
    print(i, dataPath+str(i)+'.pk')
    f = open(dataPath+str(i)+'.pk', 'rb')
    exp_name.append(file+str(i))
    exp.append(pickle.load(f))

bad = []
good = []



#Counters

bad_count = 0
good_count = 0
both = 0
none = 0

for n_exp in range(len(exp)):
    print(' ***********   Experiment  '+exp_name[n_exp]+'   *********** ')
    data           =   np.array(exp[n_exp]['data'])   #data support variable
    data           =   np.transpose(data)
    # Take only 1s of EEG recording (We originally took 2s but 1s is enough)
    data = data[:,0:250,:]
    # 1: detrend
    data        = preproc.detrend(data)
    # 2: bad-channel removal
    goodch = np.arange(31) # all plugged-in electrodes of the cap
    data         = data[goodch,:,:]
    # 3: apply spatial filter
    spatialfilter='car'
    data         = preproc.spatialfilter(data,type=spatialfilter)
    # 4 & 5: spectral filter
    freqbands    = [8, 10, 28, 30]
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

cname = 'cazzo'
norm_name = cname + '_Norm'
treshold = 0.4431697721955611 # optimal threshold

# save the trained classifer
print('Saving clsfr to : %s'%(cname+'.pk'))
pickle.dump({'classifier':clsfr_time,'spatialfilter':spatialfilter,'freqbands':freqbands,'goodch':goodch,'treshold':treshold},open(cname+'.pk','wb'))
pickle.dump({'normalizer':scaler_time},open(norm_name+'.pk','wb'))



## Power spectral density features - classifiers

fs = 250    # sampling frequency

# Welch psd

f, psd = welch(all_Data,
            fs= fs  ,           # sample rate
            window='hanning',     # apply a Hanning window before taking the DFT
            nperseg= 125)   

# select frequency bands of interests
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


cname = 'pippo'
norm_name = cname + '_Norm'
treshold = 0.45619815088221327 # optimal threshold

# save the trained classifer
print('Saving clsfr to : %s'%(cname+'.pk'))
pickle.dump({'classifier':clsfr_f,'spatialfilter':spatialfilter,'freqbands':freqbands,'goodch':goodch, 'treshold':treshold},open(cname+'.pk','wb'))
pickle.dump({'normalizer':scaler_f},open(norm_name+'.pk','wb'))