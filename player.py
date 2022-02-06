#!/usr/bin/env python3

import time
import serial

DELAY = 0.3

s = serial.Serial("/dev/ttyUSB0", 115200);

solenoids = { '1': 14, '2': 9, '3': 10, '5': 8, '6': 11 } # Keys are the notes/identifiers for the strings on the guitar. Values are solenoid pin numbers.

def release_all():
    for solenoid in solenoids.values():
        s.write(bytes("D{}\n".format(solenoid), "utf-8"))
        time.sleep(0.1)

release_all()

solenoid_states = {} # Keys are solenoid pin numbers. Values are True if a solenoid is activated and False if not.

for solenoid in solenoids.values():
    solenoid_states[solenoid] = False

# song = "1532 3  1532 1  1532 3  1532 1  1532 3  1532 1  111232323232    1532 3  1532 1  1532 3  1532 1  1532 3  1532 1  11123232323211212123 2 3 23 25   3 3 2 3 23 26   3 3 2 3 23 25   3 323 33232    1123 2 3 23 25   3 3 2 3 23 26   3 3 2 3 23 25   3 323 3232    2321       " # Baby by Justin Bieber
# song = "3212333 222 355 3212333322321   " # mary had a little lamb
# song = "5 6 53          5 6 5 3          5 6 53  32  23  32  21          5 6 53          5 6 53          5 6 53  32  23  32  21        " # post malone circles
# song = "5 365 3  553235 5 365 3  553231 5 365 3  553235 5 365 3  553231" #in the name of love rexha
# song = "3 3  35 56  321 3 3  32 23  21  3 3  35 56  321 3 3 3 2 21  123 3 3  35 56  321 3 3  32 23  21  3 3  35 56  321 3 3  32 23  21    " # starships minaj
song = "123     312     321     356     5353    2123    321     121       " #country roads
# song = "1 1 5 5 6 6 5   5 5 3 3 2 2 1   5 5 3 5 3 3 2   5 5 3 5 3 3 2   1 1 5 5 6 6 5   5 5 3 3 2 2 1   " #twinkle twinkle

try:
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
except:
    pass

release_all()