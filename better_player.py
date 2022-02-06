#!/usr/bin/env python3

import time
import serial
import websocket
import _thread

DELAY = 0.3
#DELAY = 0.05

s = serial.Serial("/dev/ttyUSB0", 115200);

#solenoids = { '1': 14, '2': 9, '3': 10, '5': 8, '6': 11 } # Keys are the notes/identifiers for the strings on the guitar. Values are solenoid pin numbers.
solenoids = { '0': 14, '1': 9, '2': 10, '3': 8, '4': 11 } # Keys are the notes/identifiers for the strings on the guitar. Values are solenoid pin numbers.

def on_message(ws, message):
    if 'players' not in message and 'x' in message:
        print(message)
        values = message.split(',')
        print(values)
        string = str(values.index('0'))
        solenoid = solenoids[string]
        print("string")
        print(string)
        print(solenoid)
        if solenoid_states[solenoid]:
            s.write(bytes("D{}\n".format(solenoid), "utf-8"))
            solenoid_states[solenoid] = False
        else:
            s.write(bytes("A{}\n".format(solenoid), "utf-8"))
            solenoid_states[solenoid] = True

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def release_all():
    for solenoid in solenoids.values():
        s.write(bytes("D{}\n".format(solenoid), "utf-8"))
        time.sleep(0.1)

release_all()

solenoid_states = {} # Keys are solenoid pin numbers. Values are True if a solenoid is activated and False if not.

for solenoid in solenoids.values():
    solenoid_states[solenoid] = False

try:
    ws = websocket.WebSocketApp("wss://play-guitar.herokuapp.com",
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
    """
    for note in song:
        if note == ' ':
            time.sleep(DELAY)
            continue
        if note not in solenoids:
            print("Invalid note: {}".format(note))
            break
        solenoid = solenoids[note]
        if solenoid_states[solenoid]:
            s.write(bytes("D{}\n".format(solenoid), "utf-8"))
            solenoid_states[solenoid] = False
            time.sleep(DELAY)
        else:
            s.write(bytes("A{}\n".format(solenoid), "utf-8"))
            solenoid_states[solenoid] = True
            time.sleep(DELAY)
    """
except:
    pass

release_all()
