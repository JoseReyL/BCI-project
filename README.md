# BCI Imagined Movement

The following brain-computer interface project is part of the final assessment for the course Advanced Brain-Computer Interfaces (SOW-MKI46) taught at Radboud University, Nijmegen, The Netherlands.

## The project
The project is based on imagined movement and has an implementation of error potentials. The aim of the interface is enable a paralised patient to perform simple actions, such as navigate through his/her house, call someone, watch TV or call for emergency. The types of emergency are toilet, food, and pain.  
Mobile EEG equipment is required to be able to run the brain computer interface. Our project was developed with a water-based mobile EEG equipment from Mobita.

## Prerequisites and Installation
Here are detailed instructions about the installation procedure. 
The following project is part of the Buffer-BCI framework. First you need to install the framework by cloning the git repository: [Buffer-BCI](https://github.com/jadref/buffer_bci)

Next, clone or download our repository under Tutorials folder of the Buffer-BCI framework.

The project is implemented in pygame. To be able to run our experiment, you need to install psychopy. We recommend to make a separate conda environment for the project first. There are the steps:

* Make a new environmenent named *bcienv* using conda:
```
conda create --n bcienv python=3.6 
```
* Activate the new environment:
```
source activate bcienv
```
* Install pygame for python 3 (Ubuntu Instruction):
```
sudo apt-get install python3-pip
sudo pip3 install pygame
```

## Starting the mobita device

To collect the signals in the computer is necessary to turn on and connect the tmsi mobita.

1. Connect the USB stick to the computer

2. Check that the blue led in the device is blinking, that means it's ready to connect

3. Run on terminal `buffer_bci-master/dataAcq/startJavaBuffer.bat`

4. Run on terminal `buffer_bci-master/dataAcq/startMobitaAutoConnect.bat`

5. Run on terminal `buffer_bci-master/dataAcq/startSigViewer.bat`

Now you should see how matlab starts and you are asked to select the cap configuration 

6. Select `cap_tmsi_mobita_32ch.txt`

If everything is correct you should see the following screen on the matlab program

![](https://raw.githubusercontent.com/JoseReyL/BCI-project/master/channels.png)

Now you can run the project

## Running the experiment
To run our experiment you need to do the following steps (simultaneously, seperate terminals):

1. Connect to the buffer-bci framework by running `./debug_quickstart.sh`

2. Run the imagined movement classifier: `python classifier.py`

3. Run the error potential classifier: `python classifier_ErrPs.py`

4. Run the interface: `python interface_imagined.py`

Detailed information about the purpose of each file, as well as its overall structure can be found under Code Documentation.

## Debugging
For debugging purposes, or in case you would like to see how the system is working on a conceptual level without connecting to EEG mobile equipment, you can manually send events in the terminal after running `./debug_quickstart.sh`

Then you need to only run the interface: `python interdace_imagined.py`  
**Note**: in the code of interface_imagined.py change **DEBUG** on line 20 to **True**

To navigate through the interface send the following event type: *classifier.prediction*  
Values: 0 - left, 1 - right, 2 - to select the option  

Once you have selected an option, it will be coloured in green. Then, normally the error potential classifier is evoked. To send an event manuaally, the event type is *errp.prediction* and the values are 0 - mistake (reject the selection) and 1 - select the option. If you reject the selection, you will keep selecting from the options on the current screen. 



## Authors
**Jose Rey Lopez**  
**Lorenzo Valacchi**  
**Mihaela Gerova**  
