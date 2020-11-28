# -*- coding: utf-8 -*-

import os
# uncomment for cs server?
# os.system("pip install pandas numpy music21")
import sys
# add ../lib to the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from music21 import midi
import pandas as pd
import numpy as np

from helpers import Music21Helper

helper = Music21Helper()

"""
# ability to display music in colab environment
def show(music):
  display(Image(str(music.write('lily.png'))))
"""

"""
# ability to play music in a colab environment
def play(music):
  filename = music.write('mid')
  !fluidsynth -ni font.sf2 $filename -F $filename\.wav -r 44100 > /dev/null
  display(Audio(filename + '.wav'))
"""

# these work for some types of files, but not others. not sure which exactly
# credit where it's due: https://groups.google.com/g/music21list/c/wcUsuqvbpUQ/m/PiVpuxkZBAAJ

# set constant path for MIDI files
#midi_path = "MIDIs"
#mozart_dir = "mozart"

# create the midi dir
#!mkdir $midi_path

"""
# Some helper methods.    
def concat_path(path, child):
    return path + "/" + child
"""

"""
def download_midi(midi_url, path):
    !wget $midi_url --directory-prefix $path > download_midi.log
"""

# maybe we find some good midis here: https://www.midiworld.com/

# set the path for mozart midi files
#mozart_path = concat_path(midi_path, mozart_dir)

# download String Quartet #1
#download_midi("https://www.midiworld.com/midis/other/mozart/mozsq1.mid", mozart_path)

# print(os.listdir(mozart_path))

# lets see if we can get some basic info out the mozart midi file
# first we need to get the midi data into a music21 stream

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

music = helper.selectFile(data_dir)
#music =  "data/mozsq1.mid"
mf = midi.MidiFile()
mf.open(music)
print("Reading MIDI data...")
mf.read()
mf.close()
print("Converting MIDI to stream...")
stream = midi.translate.midiFileToStream(mf)

print("Converting stream to matrix...")
note_matrix = helper.streamToMatrix(stream)

# convert pitch classes to simple letter names
print("Gatheirng letter names from the music...")
letter_matrix = helper.noteToLetterName(note_matrix)
# transpose the matrix - easier to work with columns than rows
df = pd.DataFrame(letter_matrix).transpose()
df.head()

# name the columns for ease of access
print("Getting parts from the data...")
partList = helper.listInstruments(stream)
print("Found {} parts:".format(len(partList)))
for part in partList:
  print(part)
# manual step needed here
# change first two parts to Violin 1 and Violin 2 to avoid confusion
#partList[0]="Violin 1"
#partList[1]="Violin 2"
df.columns = partList
#df.head()

# TODO remove?
# lets test the levenstein by comparing a part to itself
# since the strings are identical, we should receive a score of 0
#distance = helper.levenshteinDistanceDP(df["Violin 1"], df["Violin 1"])

# Now compare the violin 1 and violin 2 parts
# We expect these to be pretty different, as the two
# are generally in harmony with one another and the 
# violin 1 will have more ornamentation
print("computing levenstein distance...")
distance = helper.levenshteinDistanceDP(df['Violino I'], df['Violino II'])
print("Raw distance between inputs: " + str(distance))

# want a "percent similar" score to normalize our levenstein distances
# if the levenshtein outputs the number of changes needed to make the strings equal,
# the max that number can be is the length of the longer string
# take 1-score since the score is 'percent differnt' and we want 'percent similar

percent = 1-(distance/max(len(df['Violino I']), len(df['Violino II'])))
print("Percent difference between inputs: " + str(percent))

# TODO:
# - pull in different data so we can compare different pieces
# maybe some more string quartets in G major?
# run as __main__ so we can specify inputs of different sizes etc
# Take select 2 random midi's from ./data and take a random part from each?
# record len of the input so we can 