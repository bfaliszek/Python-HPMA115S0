#!/usr/bin/env python3

import serial, time
from time import localtime, strftime
import sqlite3

port = serial.Serial("/dev/serial0", baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1.5)

sqlite_file = 'dust_db.sqlite'

def main():
    db = sqlite3.connect(sqlite_file)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dust_table (id INTEGER PRIMARY KEY AUTOINCREMENT, data TIMESTAMP, pm25 REAL, pm10 REAL)''')
    if port.isOpen():
        port.close()
    port.open()
    time.sleep(0.2)
    try:
        data = port.read(32);
        if ord(data[0]) == 66 and ord(data[1]) == 77:
            suma = 0
            for a in range(30):
                suma += ord(data[a])
            if suma == ord(data[30])*256+ord(data[31]):
                PM25 = int(ord(data[6])*256+ord(data[7]))
                PM10 = int((ord(data[8])*256+ord(data[9]))/0.75)
                print('PM2.5: {} ug/m3'.format(PM25))
                print('PM10: {} ug/m3'.format(PM10))
                datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())
                cursor.execute('''INSERT INTO dust_table(data, pm25, pm10) VALUES(?,?,?)''', (datetime, PM25, PM10))
            else:
                print("no data")
        else:
            print("no data")
    except Exception as ex:
        print(ex)
    finally:
        db.commit()
        db.close()
        port.close()

if __name__=="__main__":
    for a in range(35):
        main()
        time.sleep(0.2)
