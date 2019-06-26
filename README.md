# BCI Imagined Movement

The following brain-computer interface project is part of the final assessment for the course Advanced Brain-Computer Interfaces (SOW-MKI46) taught at Radboud University, Nijmegen, The Netherlands.

## The project
The project is based on imagined movement and has an implementation of error potentials. The aim of the interface is enable a paralised patient to perform simple actions, such as navigate through his/her house, call someone, watch TV or call for emergency. The types of emergency are toilet, food, and pain. 

## Prerequisites and Installation
Here are detailed instructions about the installation procedure. 
The following project is part of the Buffer-BCI framework. First you need to install the framework by cloning the git repository: [Buffer-BCI](https://github.com/jadref/buffer_bci)

Next, clone or download our repository under Tutorials folder of the Buffer-BCI framework.

The project is implemented in pygame. To be able to run our experiment, you need to install psycjopy. We recommend to make a separate conda environment for the project first. There are the steps:

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
## Running the experiment
To run our experiment you need to do the following steps (simultaneously, seperate terminals):
* Connect to the buffer-bci framework by running `./debug_quickstart.sh`
* Run the imagined movement classifier: `python classifier.py`
* Run the error potential classifier: `python classifier_ErrPs.py`
* Run the interface: `python interface_imagined.py`

## Debugging
For debugging purposes, or in case you would like to see how the system is working on a conceptual level without connecting to EEG mobile equipment, you can manually send events in the terminal after running `./debug_quickstart.sh`

To navigate through the interface send the following event type: *classifier.prediction*
Values: 0 - left, 1 - right, 2 - to select the option

Ones you have selected an option, it will be coloured in green. Then, normally the error potential classifier is evoked. To send an event manuaally, the event type is *errp.prediction* and the values are 0 - mistake (reject the selection) and 1 - select the option. If you reject the selection, you will keep selecting from the options on the current screen. 

## Authors
**Jose**

**Lorenzo**

**Mihaela Gerova**
