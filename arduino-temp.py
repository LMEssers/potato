import serial
from time import sleep

dev = serial.Serial("COM4", baudrate=9600)
sleep(1)
dev.write(b'1')
print(dev.readline())
dev.write(b'0')
print(dev.readline())
dev.write(b'1')
print(dev.readline())

data = []
for _ in range(10):
    dev.write(b'2')
    line = dev.readline()
    data.append(line)

print(data)