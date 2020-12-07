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
import random

from helpers import Music21Helper

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

class LCS():

  def __init__(self):
    self.helper = Music21Helper()

  def preProcessStream(self, music):
    """
    Convert MIDI file to a stream and return
    """
    mf = midi.MidiFile()
    mf.open(music)
    print("Reading MIDI data for {}...".format(music))
    mf.read()
    mf.close()
    print("Converting MIDI to stream for {}...".format(music))
    stream = midi.translate.midiFileToStream(mf)

    return stream

  def streamToDF(self, stream):
    """
    Convert a music21 stream to a pd DataFrame
    """
    print("Converting stream to matrix...")
    note_matrix = self.helper.streamToMatrix(stream)

    # convert pitch classes to simple letter names
    print("Gatheirng letter names from the music...")
    letter_matrix = self.helper.noteToLetterName(note_matrix)
    # transpose the matrix - easier to work with columns than rows
    df = pd.DataFrame(letter_matrix).transpose()

    return df

  def selectPart(self, stream, dataframe):
    partList = self.helper.listInstruments(stream)
    dataframe.columns = partList

    partNum = random.choice(range(len(partList)))

    return dataframe[partList[partNum]]

  def compute(self, file1, file2):
    stream1 = self.preProcessStream(file1)
    stream2 = self.preProcessStream(file2)

    df1 = self.streamToDF(stream1)
    df2 = self.streamToDF(stream2)

    part1 = self.selectPart(stream1, df1)
    part2 = self.selectPart(stream2, df2)

    print("Computing the longest common subsequence...")
    print("We are comparing the {} part from {} to the {} part from {}".format(part1.name, file1, part2.name, file2))
    lcs_length = self.helper.lcsDP(part1, part2)

    print("Length of the longest common subsequence: " + str(lcs_length))
    #percentage = lcs_length/max(len(part1), len(part2))
    percentage = lcs_length
    print("LCS length as a percentage of input size: " + str(percentage))

if __name__ == '__main__':
  lcs = LCS()
  file1 = lcs.helper.selectFile(data_dir)
  file2 = lcs.helper.selectFile(data_dir)

  lcs.compute(file1, file2)
  