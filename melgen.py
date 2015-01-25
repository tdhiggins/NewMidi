import math
import random
from midiutil.MidiFile import MIDIFile
import sys


# Create dictionary mapping midi number to note.

midi_to_note = {}

for i in range(0, 128):
    midi_to_note[i] = None

mod_map = {0:'c',1:'cs',2:'d',3:'ds',4:'e',5:'f',6:'fs',7:'g',8:'gs',9:'a',10:'as',11:'b'}

for i in midi_to_note:
    midi_to_note[i] = mod_map[i%12]

counter = 0
adder = 0
for i in midi_to_note:
    midi_to_note[i] += str(adder)
    counter += 1
    if counter == 12:
        counter = 0
        adder += 1

# Create dictionary mapping note to midi number.

note_to_midi = {}
for k, v in midi_to_note.items():
    note_to_midi[v] = k

# Create list of usable notes.

maji = [2, 2, 1, 2, 2, 2, 1]
mini = [2, 1, 2, 2, 1, 2, 2]
maji = maji + maji + maji + maji + maji + maji + maji + maji + maji + maji + maji
mini = mini + mini + mini + mini + mini + mini + mini + mini + mini + mini + mini

def get_midi_scale(key, m):
    scale = []
    if m == 'major':
        scale.append(note_to_midi[key+'0'])
        for i in maji:
            if scale[-1]+i in midi_to_note:
                scale.append(scale[-1]+i)
            else:
                break
    if m == 'minor':
        scale.append(note_to_midi[key+'0'])
        for i in mini:
            if scale[-1]+i in midi_to_note:
                scale.append(scale[-1]+i)
            else:
                break
    return scale

def get_note_scale(key, m):
    scale = []
    for i in get_midi_scale(key, m):
        scale.append(midi_to_note[i])
    return scale

def get_next_note(note, scale, maxD):
    number = random.randrange(-maxD, maxD)
    current = scale.index(note)
    newIndex = current+number
    if newIndex < 0:
        newIndex = current-number
    elif newIndex > len(scale):
        newIndex = current-number
    return scale[newIndex]

def mel_check(melody):
    for i in range(0, len(melody)):
        melody[i] = midi_to_note[melody[i]]
    return melody

note_lengths = [1.0, 1/2.0, 1/4.0, 1/8.0, 1/16.0, 1/32.0, 1/64.0]

def make_melody(key, m, maxD, root, smallestNote, biggestNote, length, startOct):
    midi_scale = get_midi_scale(key, m)
    note_scale = get_note_scale(key, m)
    melody = []
    possible_note_lengths = note_lengths[biggestNote:smallestNote+1]
    count = 0
    if root:
        melody.append([note_to_midi[key+str(startOct)], random.choice(possible_note_lengths)])
        count += melody[0][1]
    else:
        melody.append([note_to_midi[key+str(startOct)]+random.randrange(0, 7), random.choice(possible_note_lengths)])
        count += melody[0][1]
    while count < length:
        d = random.choice(possible_note_lengths)
        while count + d > length:
            d = random.choice(possible_note_lengths)
        melody.append([get_next_note(melody[-1][0], midi_scale, maxD), d])
        count += d

    return melody


def make_midi(name, tempo, key, m, maxD, root, smallestNote, biggestNote, length, startOct):
    melody = make_melody(key, m, maxD, root, smallestNote, biggestNote, length, startOct+2)
    MyMIDI = MIDIFile(1)
    track = 0
    time = 0
    MyMIDI.addTrackName(track, time, name)
    MyMIDI.addTempo(track, time, tempo)

    for i in melody:
        MyMIDI.addNote(track, 0, i[0], time, 4*i[1], 100)
        time += 4*i[1]


    return MyMIDI