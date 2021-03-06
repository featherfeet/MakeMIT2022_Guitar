#!/usr/bin/env python3

import time
import serial

DELAY = 0.3
#DELAY = 0.05

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

baby = "1532 3  1532 1  1532 3  1532 1  1532 3  1532 1  111232323232    1532 3  1532 1  1532 3  1532 1  1532 3  1532 1  11123232323211212123 2 3 23 25   3 3 2 3 23 26   3 3 2 3 23 25   3 323 33232    1123 2 3 23 25   3 3 2 3 23 26   3 3 2 3 23 25   3 323 3232    2321       " # Baby by Justin Bieber
mary = "3212333 222 355 3212333322321   " # mary had a little lamb
circles = "5 6 53          5 6 5 3          5 6 53  32  23  32  21          5 6 53          5 6 53          5 6 53  32  23  32  21        " # post malone circles
love = "5 365 3  553235 5 365 3  553231 5 365 3  553235 5 365 3  553231" #in the name of love rexha
starships = "3 3  35 56  321 3 3  32 23  21  3 3  35 56  321 3 3 3 2 21  123 3 3  35 56  321 3 3  32 23  21  3 3  35 56  321 3 3  32 23  21    " # starships minaj
country = "123     312     321     356     5353    2123    321     121       " #country roads
twinkle = "1 1 5 5 6 6 5   5 5 3 3 2 2 1   5 5 3 5 3 3 2   5 5 3 5 3 3 2   1 1 5 5 6 6 5   5 5 3 3 2 2 1   " #twinkle twinkle
death = "3   5 53  36  3 3   5 52    1532121  1 23   1532121  5 53    2   3   5 53  36  3 3   5 52   1532121  1 23   1532121  5 53  32  21" #death bed
runaway = "1 32 11 16 31 32 35 3  3  33 52    23 25 6321  11 32 11 16 31 32 35 3  3  33 52    23 25 6321" # runaway aurora
heatwaves = "1 1 1133222     1 1 11332 2     1 1 1 332 2     1 1 1 332 2     1 1 1133222     1 1 11332 2     1 1 1 332 2     1 1 1 332 2     2221 2  2221 2  2221 2  2221 2  2221 2  2221 2  2221 2  2322 1  33333335 32      2222223 21  31  3333335 32      2222223 21  31  1 1 11332 2     1 1 11332 2     1 1 1 332 2     1 1 11332 2     1 1 1 332 2     1 1 1 332 2     1 1 1 332 2     1 1 11332 2 " # HEATWAVES
scale = "12353532123535321353135313631363153525351"
test = "1 2 3 5 6"

songs = {"Baby by Justin Bieber": baby, "Mary Had a Little Lamb": mary, "Circles by Post Malone": circles, "In the Name of Love by Rexha": love, "Starships by Nicki Minaj": starships, "Country Roads, Take Me Home by John Denver": country, "Twinkle Twinkle Little Star": twinkle, "Death Bed": death, "Runaway Aurora": runaway, "Heatwaves": heatwaves, "Scale": scale, "Test": test}

print("Available songs:")
for song_name in songs:
    print("    - {}".format(song_name))

song = songs[input("Song? ")]

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
