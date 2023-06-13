#!/usr/bin/env python


from __future__ import print_function


import matplotlib.pyplot as plt
import numpy as np
import sys
import time
import _thread
import serial

#from libregpio import IN
#from libregpio import OUT
#from libregpio import cleanup


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

#Uncomment the following when not using setup.py or pip to install the packages
#Replace the path to the appropriate package location
#sys.path.append('/path/to/pyrgbdriverkit/')
#sys.path.append('/path/to/pyusb/')

import rgbdriverkit as rgbdriverkit
from rgbdriverkit.qseriesdriver import Qseries
from rgbdriverkit.spectrometer import SpectrometerStatus
from rgbdriverkit.calibratedspectrometer import SpectrumData
from rgbdriverkit.calibratedspectrometer import SpectrometerProcessing


def main(index_open_probe, serial_check, flake_delay, subcoords_pp0, subcoords_pp1, subcoords_pe0, subcoords_pe1):
    try:
        while(True):
            
            
            
            
            
            
            index_open_probe = ser_arduino.readline().decode('utf-8').rstrip()
            if ser_arduino.in_waiting > 0:
                ser_arduino.reset_input_buffer()
                #print('test')
            
                                             
            
            #lightsensor0 = lightsensor_pin0.input(bias='pull-down') #if sensor pin is HIGH, set variable to True
            #lightsensor1 = lightsensor_pin1.input(bias='pull-down')
            #lightsensor2 = lightsensor_pin2.input(bias='pull-down')
            #lightsensor3 = lightsensor_pin3.input(bias='pull-down')
            #lightsensor4 = lightsensor_pin4.input(bias='pull-down')
            #lightsensor5 = lightsensor_pin5.input(bias='pull-down')
            #lightsensor6 = lightsensor_pin6.input(bias='pull-down')
                    
            #arr_probe = np.array([lightsensor0, lightsensor1, lightsensor2, lightsensor3, lightsensor4, lightsensor5, lightsensor6], dtype=bool)
            
            #arr_probe = np.array([False, True, False, False, False, False, False], dtype=bool) #temporary, delete this
            
            #global open_probe
            
            #Check if a currently open probe is closed AND a new probe is opened, also ignore when no probes are open
            #POSSIBLE ISSUE: open_probe could be overwritten with 2 indexes being true / 2 probes being open (not certain if it accually could happen)
            #if len(open_probe) == len(arr_probe): # Assuming both arrays have the same length
            #    # Check if one of the arrays has all zeros
            #    if all(val_probe == 0 for val_probe in open_probe) or all(val_probe == 0 for val_probe in arr_probe):
            #        #print("False test 1")
            #        activate_spectrometer = False
            #    else:
            #        # Use a flag variable to keep track if any of the values match
            #        flag = True
            #        for i in range(len(open_probe)):
            #            if open_probe[i] != 0 and arr_probe[i] != 0 and open_probe[i] == arr_probe[i]:
            #                flag = False
            #                break
            #        # Output True only if none of the values match
            #        if flag:
            #            activate_spectrometer = True
            #            #count_flake = count_flake + 1   #set the number of flakes detected to one higher
            #        else:
            #            print("False test 2")
            #            activate_spectrometer = False
            #else:
            #    activate_spectrometer = False # Arrays are not of the same length
            
            #global serial_check
            
            #code for activation of measuring spectrum
            #if activate_spectrometer:
            if index_open_probe != serial_check and index_open_probe != '':

                print(index_open_probe)   

                serial_check = index_open_probe
                
                #open_probe = arr_probe #overwrite the indexes of open probes to only execute this code ones
                #index_open_probe = [i for i, val_spectrometer in enumerate(open_probe) if val_spectrometer] #output the number of the open probe
                
                    
                #print(index_open_probe)
                    
                #start exposure
                q.start_exposure(1)
                #print("Waiting for spectrum...")
                while not q.available_spectra:
                    #print("measuring..")
                    time.sleep(0.0001)

                #print("Spectrum available")
                spec = q.get_spectrum_data() # Get spectrum with meta data
                #print("TimeStamp:", spec.TimeStamp)
                #print("LoadLevel: %.2f" % spec.LoadLevel)
                #print("ExposureTime: " + str(spec.ExposureTime) + "s")
                #print("Averaging: " + str(spec.Averaging))


                #print figure of the spectrum
                if False:
                    print("Plot spectrum and save figure to file 'spectrum.png'.")
                    #import matplotlib.pyplot as plt
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
                    
                    
                y_coordinates = spec.Spectrum
                

                maximum_intensity = np.max(y_coordinates)

                if maximum_intensity > 300:
                    
                    #x > 900, x < 1300 || x > 1150, x < 1750
                    if any(np.logical_and(x > maximum_intensity*0.2, x < maximum_intensity*0.3) for x in y_coordinates[subcoords_pp0]) and any(np.logical_and(x > maximum_intensity*0.4, x < maximum_intensity*0.5) for x in y_coordinates[subcoords_pp1]): #if any value in the array exceeds the threshhold, a material is identified
                        start_flake_thread = True #True if the material needs to be sorted out, false if not
                        print("pp")

                    #x > 300, x < 600 || x > 700, x < 1000    
                    elif any(np.logical_and(x > maximum_intensity*0.15, x < maximum_intensity*0.2) for x in y_coordinates[subcoords_pe0]) and any(np.logical_and(x > maximum_intensity*0.5, x < maximum_intensity*0.5) for x in y_coordinates[subcoords_pe1]): #if any value in the array exceeds the threshhold, a material is identified
                        start_flake_thread = True
                        print("pe")
                    

                    #elif any(x > spectrum_threshold for x in y_coordinates[subcoords_pvc]): #if any value in the array exceeds the threshhold, a material is identified
                    #    start_flake_thread = True
                        #print("pvc")
                            
                    else: #alse no material is identified
                        start_flake_thread = False
                    
                        
                    if start_flake_thread: #start thread that activates the solenoid valves and seperates the flake
                        _thread.start_new_thread(flake_tracking, (index_open_probe, flake_delay))
                
        
            
    except KeyboardInterrupt: #when pressing ctrl + c, the code is stopped and correctly shut down
        print("Shutdown requested...exiting")
        #cleanup() #reset gpio pins
        q.close() # Close spectrometer connection
        


#thread for tracking flakes
def flake_tracking(index_open_valve, flake_delay):
    
    
    #print(index_open_valve)
    if index_open_valve == '0':
        #gpio_open_valve = solenoid_pin0
        #ser_potato.Write("probe 0")
        print('probe 0')
    
    elif index_open_valve == '1':
        #gpio_open_valve = solenoid_pin1                                                  
        #ser_potato.Write("probe 1")
        print('probe 1')

    elif index_open_valve == '2':
        #gpio_open_valve = solenoid_pin2
        #ser_potato.Write("probe 2")
        print('probe 2')
    
    elif index_open_valve == '3':
        #gpio_open_valve = solenoid_pin3
        #ser_potato.Write("probe 3")
        print('probe 3')
    
    elif index_open_valve == '4':
        #gpio_open_valve = solenoid_pin4
        #ser_potato.Write("probe 4")
        print('probe 4')

    elif index_open_valve == '5':
        #gpio_open_valve = solenoid_pin5
        #ser_potato.Write("probe 5")
        print('probe 5')
    
    elif index_open_valve == '6':
        #gpio_open_valve = solenoid_pin6
        #ser_potato.Write("probe 6")
        print('probe 6')
    

    time.sleep(flake_delay)
    #gpio_open_valve.output(1) #activate solenoid valve
    #solenoid_pin0.output(1)
    #solenoid_pin1.output(1)
    #solenoid_pin2.output(1)
    #solenoid_pin3.output(1)
    #solenoid_pin4.output(1)
    #solenoid_pin5.output(1)
    #solenoid_pin6.output(1)
    time.sleep(2) 
    #gpio_open_valve.output(0) #deactivate solenoid valve
    #solenoid_pin0.output(0)
    #solenoid_pin1.output(0)
    #solenoid_pin2.output(0)
    #solenoid_pin3.output(0)
    #solenoid_pin4.output(0)
    #solenoid_pin5.output(0)
    #solenoid_pin6.output(0)
    
    print("flake uitgeschoten")
    
    
    

#cleanup()



#lightsensor_pin0 = IN('GPIOX_0') # set pin GPIOX_12 to be used as an input
#lightsensor_pin1 = IN('GPIOX_10')
#lightsensor_pin2 = IN('GPIOX_1')
#lightsensor_pin3 = IN('GPIOX_16')
#lightsensor_pin4 = IN('GPIOX_2')
#lightsensor_pin5 = IN('GPIOX_3') 
#lightsensor_pin6 = IN('GPIOX_4') 

#solenoid_pin0 = OUT('GPIOX_8') # set pin GPIOX_8 to be used as an output
#solenoid_pin1 = OUT('GPIOX_9') 
#solenoid_pin2 = OUT('GPIOX_11')
#solenoid_pin3 = OUT('GPIOX_17')
#solenoid_pin4 = OUT('GPIOX_18')
#solenoid_pin5 = OUT('GPIOX_6')
#solenoid_pin6 = OUT('GPIOX_7')


#open_probe = (True, False, False, False, False, False, False) #set the first probe as initially open (this gets overwritten)

flake_delay = 13
#delay of activating solenoid valve in seconds

serial_check = 10 #arduino read, set arbitrary value that isn't between 0 and 6

index_open_probe = 20 #set arbitrary value that isn't between 0 and 6 and not equal to serial_check


print("Demo program started.")
print("rgbdriverkit version: " + rgbdriverkit.__version__)

dev = Qseries.search_devices()
if (dev != None):
    print("Device found.")
else:
    #cleanup() #reset gpio pins
    sys.exit("No device found.")

q = Qseries(dev[0]) # Create instance of first spectrometer found

# Print device properties
print("Model name:", q.model_name)
print("Manufacturer:", q.manufacturer)
print("Serial Number:", q.serial_number)

q.open() # Open device connection

print("Software version: " + q.software_version)
print("Hardware version: " + q.hardware_version)

# Set exposure time and averaging
q.exposure_time = 0.025 # in seconds
q.averaging = 1 # number of measurements per spectrum

print("Starting exposure with t=" + str(q.exposure_time) + "s" + ", and averaging " + str(q.averaging))

q.processing_steps = (SpectrometerProcessing.AdjustOffset)

x_coordinates = q.get_wavelengths()

#to add more peaks/ranges to check -> np.logical_or(np.logical_or(np.logical_and(x), y), z) -- where y and z can each contain an np.logical_or and np.logical_and statement
subcoords_pp0 = [index for index,value in enumerate(x_coordinates) if np.logical_and(value > 1180, value < 1240)] #get index of wavelengths in the spectrum
subcoords_pp1 = [index for index,value in enumerate(x_coordinates) if np.logical_and(value > 1530, value < 1550)]
subcoords_pe0 = [index for index,value in enumerate(x_coordinates) if np.logical_and(value > 1180, value < 1240)] #get index of wavelengths in the spectrum
subcoords_pe1 = [index for index,value in enumerate(x_coordinates) if np.logical_and(value > 1530, value < 1550)]
#subcoords_pvc = [index for index,value in enumerate(x_coordinates) if np.logical_and(value > 1400, value < 1600)] #get index of wavelengths in the spectrum 
                            
#print("range")
#print(y_coordinates[subcoords])


if __name__ == '__main__':
    ser_arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=0)
    ser_arduino.reset_input_buffer()

    #ser_potato = serial.Serial('/dev/ttyS0', 115200, serial.PARITY_NONE, serial. STOPBITS_ONE, serial. EIGHTBITS, timeout=0)

#start the program
main(index_open_probe, serial_check, flake_delay, subcoords_pp0, subcoords_pp1, subcoords_pe0, subcoords_pe1)
