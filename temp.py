from libregpio import IN
from libregpio import OUT
from libregpio import cleanup
import numpy as np
cleanup()

lightsensor_pin0 = IN('GPIOX_12') # set pin GPIOX_12 to be used as an input
lightsensor_pin1 = IN('GPIOX_13')
lightsensor_pin2 = IN('GPIOX_14')
lightsensor_pin3 = IN('GPIOX_15')
lightsensor_pin4 = IN('GPIOX_0')
lightsensor_pin5 = IN('GPIOX_10') 
lightsensor_pin6 = IN('GPIOX_1')

while True:
    
    
    
    
    lightsensor0 = lightsensor_pin0.input(bias='pull-down') #if sensor pin is HIGH, set variable to True
    lightsensor1 = lightsensor_pin1.input(bias='pull-down')
    lightsensor2 = lightsensor_pin2.input(bias='pull-down')
    lightsensor3 = lightsensor_pin3.input(bias='pull-down')
    lightsensor4 = lightsensor_pin4.input(bias='pull-down')
    lightsensor5 = lightsensor_pin5.input(bias='pull-down')
    lightsensor6 = lightsensor_pin6.input(bias='pull-down')
    
    arr_probe = np.array([lightsensor0, lightsensor1, lightsensor2, lightsensor3, lightsensor4, lightsensor5, lightsensor6], dtype=bool)
   
    print(arr_probe)
