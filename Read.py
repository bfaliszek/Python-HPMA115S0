#!/usr/bin/python
import serial
from time import localtime, strftime

port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.5)
data = port.read(32);

f = open("/home/pi/" + strftime("%Y-%m-%d", localtime()) + ".txt", "a")
if ord(data[0]) == 66 and ord(data[1])==77:
        suma = 0
        for a in range(30):
                suma += ord(data[a])

        if suma == ord(data[30])*256+ord(data[31]):

                PM25 = str(ord(data[6])*256+ord(data[7]))
                PM10 = str(ord(data[8])*256+ord(data[9]))
                str = strftime("%Y-%m-%d %H:%M:%S", localtime()) + "\t" + PM25 + "\t" + PM10;
                f.write(str + "\n")
                print(str)


port.close()
f.close()
