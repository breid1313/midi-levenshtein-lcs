# -*- coding: utf-8 -*-

# Helper class for doing interesting things with music21

from music21 import chord, pitch
import numpy as np
import random
import os

class Music21Helper():
    def __init__(self):
        pass
    
    @staticmethod
    def listInstruments(stream):
        """
        takes a music21.stream object and outputs a list of the instruments
        present in the score
        note: these instruments may not be named depending on the midi file, so some
        of the output might be None. that's ok.
        """
        partList = []
        partStream = stream.parts.stream()
        for p in partStream:
            aux = p
            partList.append(p.partName)
        return partList

    @staticmethod
    def extract_notes(midi_part):  
        """
        takes a midi part stream and extracts the note/chord objects. returns as a list.
        note that we have a mix, of note/chord objects (although in the case of a string
        quartet the "chords" are probably just double stops), so we need to think about
        a justifiable way to hand this.
        Reduce to the root of the chord? e.g Emaj => E
        """
        ret = []
        for nt in midi_part.flat.notes:  
            ret.append(nt)          
        return ret

    def streamToMatrix(self, stream):
        note_matrix = []
        for i in range(len(stream.parts)):
            part_arr = self.extract_notes(stream.parts[i].flat.notes)
            note_matrix.append(part_arr)
        return note_matrix

    @staticmethod
    def noteToLetterName(note_matrix):
        aux = []
        for i in range(len(note_matrix)):
            row = []
            for j in range(len(note_matrix[i])):
                if isinstance(note_matrix[i][j], chord.Chord):
                    nt = note_matrix[i][j]._findRoot().name
                else:
                    nt = note_matrix[i][j]._getName()
                row.append(nt)
            aux.append(row)
        return aux

    @staticmethod
    def levenshteinDistanceDP(token1, token2, printDistances=False):
        distances = np.zeros((len(token1) + 1, len(token2) + 1))

        for t1 in range(len(token1) + 1):
            distances[t1][0] = t1

        for t2 in range(len(token2) + 1):
            distances[0][t2] = t2
            
        a = 0
        b = 0
        c = 0
        
        for t1 in range(1, len(token1) + 1):
            for t2 in range(1, len(token2) + 1):
                if (token1[t1-1] == token2[t2-1]):
                    distances[t1][t2] = distances[t1 - 1][t2 - 1]
                else:
                    a = distances[t1][t2 - 1]
                    b = distances[t1 - 1][t2]
                    c = distances[t1 - 1][t2 - 1]
                    
                    distances[t1][t2] = min([a,b,c]) + 1
        if printDistances:
            printDistances(distances, len(token1), len(token2))
        return distances[len(token1)][len(token2)]

    @staticmethod
    def printDistances(distances, token1Length, token2Length):
        for t1 in range(token1Length + 1):
            for t2 in range(token2Length + 1):
                print(int(distances[t1][t2]), end=" ")
            print()

    @staticmethod
    def lcsDP(token1, token2): 
        # find the length of the strings 
        m = len(token1) 
        n = len(token2) 
    
        # declaring the array for storing the dp values 
        L = [[None]*(n+1) for i in range(m+1)] 
    
        # build L by computing values from the bottom uo
        for i in range(m+1): 
            for j in range(n+1): 
                if i == 0 or j == 0 : 
                    L[i][j] = 0
                elif token1[i-1] == token2[j-1]: 
                    L[i][j] = L[i-1][j-1]+1
                else: 
                    L[i][j] = max(L[i-1][j] , L[i][j-1]) 
        # return the value of the bottom right corner of the array
        # this contains the length of the LCS if we consider both complete strings
        return L[m][n] 

    @staticmethod
    def selectFile(directory):
        choice = random.choice(os.listdir(directory))
        return os.path.join(directory, choice)
