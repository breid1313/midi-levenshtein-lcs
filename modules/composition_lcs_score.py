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

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

music = helper.selectFile(data_dir)
#music =  "data/mozart_sq_F_k590_1.squ"
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

print("Computing the longest common subsequence...")
lcs_length = helper.lcsDP(df[partList[0]], df[partList[1]])

print("Length of the longest common subsequence: " + str(lcs_length))
percentage = lcs_length/max(len(df[partList[0]]), len(df[partList[1]]))
print("LCS length as a percentage of input size: " + str(percentage))