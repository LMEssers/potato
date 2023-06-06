#!/usr/bin/env python


from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import _thread

from libregpio import IN
from libregpio import OUT
from libregpio import cleanup


__author__ = "RGB Photonics GmbH"

"""
Simple Spectrometer

A demo program to take a spectrum with a new Qseries spectrometer
demonstrating how to use the rgbdriverkit in order to use the
spectrometer from your own software.

Note: For plotting/saving the graph matplotlib is required.

Copyright 2017 RGB Photonics GmbH
written by Martin Hofmann
Version 0.1.1 - April 28, 2017
"""

import sys
import time

#Uncomment the following when not using setup.py or pip to install the packages
#Replace the path to the appropriate package location
#sys.path.append('/path/to/pyrgbdriverkit/')
#sys.path.append('/path/to/pyusb/')

import rgbdriverkit as rgbdriverkit
from rgbdriverkit.qseriesdriver import Qseries
from rgbdriverkit.spectrometer import SpectrometerStatus
from rgbdriverkit.calibratedspectrometer import SpectrumData
from rgbdriverkit.calibratedspectrometer import SpectrometerProcessing



lightsensor_pin0 = IN('GPIOX_12') # set pin GPIOX_12 to be used as an input

cleanup()

#while True:
#    lightsensor0 = lightsensor_pin0.input(bias='pull-down') #if sensor pin is HIGH, set variable to True
           
#    print(lightsensor0)    
    

    
    
    
    
    



