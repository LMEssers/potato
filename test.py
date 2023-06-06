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




def main():
    try:
        while(True):
            lightsensor0 = lightsensor_pin0.input(bias='pull-down') #if sensor pin is HIGH, set variable to True
            lightsensor1 = lightsensor_pin1.input(bias='pull-down')
            lightsensor2 = lightsensor_pin2.input(bias='pull-down')
                    
            arr_probe = np.array([lightsensor0, lightsensor1, lightsensor2], dtype=bool)
            
            arr_probe = np.array([False, True, False], dtype=bool) #temporary, delete this
            
            global open_probe
            
            #Check if a currently open probe is closed AND a new probe is opened, also ignore when no probes are open
            #POSSIBLE ISSUE: open_probe could be overwritten with 2 indexes being true / 2 probes being open (not certain if it accually could happen)
            if len(open_probe) == len(arr_probe): # Assuming both arrays have the same length
                # Check if one of the arrays has all zeros
                if all(val_probe == 0 for val_probe in open_probe) or all(val_probe == 0 for val_probe in arr_probe):
                    print("False test")
                    activate_spectrometer = False
                else:
                    # Use a flag variable to keep track if any of the values match
                    flag = True
                    for i in range(len(open_probe)):
                        if open_probe[i] != 0 and arr_probe[i] != 0 and open_probe[i] == arr_probe[i]:
                            flag = False
                            break
                    # Output True only if none of the values match
                    if flag:
                        activate_spectrometer = True
                        #count_flake = count_flake + 1   #set the number of flakes detected to one higher
                    else:
                        activate_spectrometer = False
            else:
                activate_spectrometer = False # Arrays are not of the same length
            
            
            #code for activation of measuring spectrum
            if activate_spectrometer:

                open_probe = arr_probe #overwrite the indexes of open probes to only execute this code ones
                index_open_probe = [i for i, val_spectrometer in enumerate(open_probe) if val_spectrometer] #output the number of the open probe
                
                print("arr_probe", arr_probe)
                print("Software version: " + q.software_version)
                print("Hardware version: " + q.hardware_version)

                nm = q.get_wavelengths()

                # Set exposure time and start exposure
                q.exposure_time = 0.5 # in seconds
                q.averaging = 1 # number of measurements per spectrum
                print("Starting exposure with t=" + str(q.exposure_time) + "s" + ", and averaging " + str(q.averaging))
                q.processing_steps = SpectrometerProcessing.AdjustOffset # only adjust offset
                q.start_exposure(1)
                print("Waiting for spectrum...")
                while not q.available_spectra:
                    print("test")
                    time.sleep(1)

                print("Spectrum available")
                spec = q.get_spectrum_data() # Get spectrum with meta data

                print("TimeStamp:", spec.TimeStamp)
                print("LoadLevel: %.2f" % spec.LoadLevel)
                print("ExposureTime: " + str(spec.ExposureTime) + "s")
                print("Averaging: " + str(spec.Averaging))

                

                if False:
                    print("Plot spectrum and save figure to file 'spectrum.png'.")
                    import matplotlib.pyplot as plt
                    # Create plot
                    plt.clf()
                    plt.plot(nm, spec.Spectrum)
                    plt.grid(True)
                    plt.title('Spectrum')
                    plt.xlabel('Wavelength (nm)')
                    plt.ylabel('ADCvalues')
                    plt.draw()
                    plt.show()
                    # save figure to file
                    plt.savefig("spectrum.png")
                
                import matplotlib.pyplot as plt
                plt.clf() #clear plot
                lines = plt.plot(nm, spec.Spectrum)
                #line.get_xdata()
                #line.get_ydata()
                lines_spectrum = lines[0].get_xydata()
                
                print("Done")
                
                print(lines_spectrum)
                
                
                
                #bepaal materiaal van het spectrum -> set detect_material op true wanneer het uitgesorteerd moeten worden, false wanneer niet
                #subcoords = [(x, y) for x, y in lines_spectrum if x in range(1200, 1300)]
                
                x_coordinates = lines_spectrum[:,0]
                y_coordinates = lines_spectrum[:,1]
                print(x_coordinates)
                subcoords = [index for index,value in enumerate(x_coordinates) if np.logical_and(value > 1200, value < 1400)]
                #subcoords = subcoords1[np.where(subcoords1 <1400, subcoords1, 0)]
                                           
                print("range")
                print(y_coordinates[subcoords])
                
                if any(x > spectrum_threshold for x in y_coordinates[subcoords]):
                    print("goed")
                    
                else:
                    print("slecht")
                
                _thread.start_new_thread(flake_tracking, (index_open_probe,))

        
            
    except KeyboardInterrupt:
        print("Shutdown requested...exiting")
        cleanup() #reset gpio pins
        q.close() # Close device connection
        

   
    



#thread for tracking flakes
def flake_tracking(index_open_valve):
    
    global flake_delay
    
    
    if index_open_valve == [0]:
        gpio_open_valve = solenoid_pin0
        print("probe 0")
    
    elif index_open_valve == [1]:
        gpio_open_valve = solenoid_pin1
        print("probe 1")

    elif index_open_valve == [2]:
        gpio_open_valve = solenoid_pin2
        print("probe 2")


    time.sleep(flake_delay)
    gpio_open_valve.output(1)
    time.sleep(0.1) 
    gpio_open_valve.output(0)
    
    print("flake uitgeschoten")
    
    
    



lightsensor_pin0 = IN('GPIOX_12') # set pin GPIOX_12 to be used as an input
lightsensor_pin1 = IN('GPIOX_13') # set pin GPIOX_13 to be used as an input
lightsensor_pin2 = IN('GPIOX_14') # set pin GPIOX_14 to be used as an input

solenoid_pin0 = OUT('GPIOX_5') # set pin GPIOX_5 to be used as an output
solenoid_pin1 = OUT('GPIOX_6') # set pin GPIOX_6 to be used as an output
solenoid_pin2 = OUT('GPIOX_7') # set pin GPIOX_7 to be used as an output

open_probe = (True, False, False) #set the first probe as initially open (this gets overwritten)

flake_delay = 2 #delay of activating solenoid valve in seconds

spectrum_threshold = 400 #value at which a peak is registered




print("Demo program started.")
print("rgbdriverkit version: " + rgbdriverkit.__version__)

dev = Qseries.search_devices()
if (dev != None):
    print("Device found.")
else:
    cleanup() #reset gpio pins
    q.close() # Close device connection
    sys.exit("No device found.")

q = Qseries(dev[0]) # Create instance of first spectrometer found

# Print device properties
print("Model name:", q.model_name)
print("Manufacturer:", q.manufacturer)
print("Serial Number:", q.serial_number)

q.open() # Open device connection



main()
