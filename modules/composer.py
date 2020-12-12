#!/usr/bin/python3

from itertools import combinations
import os
import sys

from music21 import environment, key, metadata, note, stream
import numpy as np

# add ../lib to the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
# add ../resources to the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "resources"))

from helpers import Music21Helper


# ## Musescore setup
# This is to configure Musescore as the musical notation generator/midi player for music21.
# Only needed for viewing scores and listening to generated music, so commented out by default.
# For more info: http://web.mit.edu/music21/doc/installing/installAdditional.html#musescore

# # Lookup music21 environment settings
# us = environment.UserSettings()

# # tell the music21 environment where musescore binary lives
# environment.set('musicxmlPath', '/usr/bin/musescore')

# # to let music21 talk to musescore, create a placeholder file and set
# # musescore's directPNGPath to point to it
# us['musescoreDirectPNGPath'] = '../resources/musescore_placeholder.png'



class Compose:
    """ Generates a musical score given a string representation of a key,
        following music21's convention which uses lowercase letters for minor mode
        and uppercase for major mode. 
        (https://web.mit.edu/music21/doc/moduleReference/moduleKey.html#music21.key.Key)
        
        Example usage:

        score_in_G_minor = Compose("g")
        score_in_F_sharp_major = Compose("F#")

    """
    
    def __init__(self, given_key):
        self.key = key.Key(given_key)
        self.pitch_names = [i.name for i in self.key.pitches]
        
    def melody(self, length):
        """given an int length,
           returns a list of pitch names randomly selected from
           list of notes ϵ self.key
        """
        return [np.random.choice(self.pitch_names) for i in range(length)]
    
    def convert_names_to_notes(self, pitch_names):
        """given a list of pitch names, eg ['A4'] 
           returns a list of note.Notes, eg [<music21.note.Note A>]
        """
        return [note.Note(j) for j in pitch_names]
    
    def list_to_random_subset(self, s):
        """ given s (list of notes), 
            returns a random subset of s as stream.Stream object
        """
        st = stream.Stream()

        #get list of unique notes
        un = list(set(i.pitch.name for i in s))

        for i in range(np.random.randint(0,len(un))):
            un.remove(np.random.choice(un))

        st.append( self.convert_names_to_notes(un) )
        return st
    
    def get_notes_in_key(self):
        """returns list of note.Notes in specified key"""
        return self.convert_names_to_notes(self.pitch_names)
    
    def create_chord_from_random_notes_in_key(self, minNum=2, maxNum=6):
        """ given list of note.Note objects
            return chord.Chord of n notes, minNum <= n <= maxNum
        """
        nl = [np.random.choice(self.get_notes_in_key()) for i in range(np.random.randint(minNum,maxNum))]
        ch = chord.Chord(nl)
        return ch
    
    def create_part_chords(self, chords):
        """return a stream of chords"""
        pass
    
    def create_part_from_notes(self, partID, size=10):
        """ given an id and optional size,
            return a stream.Part of size notes
        """
        p = stream.Part(id=partID)
        m = self.melody(size)
        n = self.convert_names_to_notes(m)
        for i in range(len(n)):
            p.insert(i+1,n[i])
        #s = self.list_to_random_subset(n)
        return p

    def create_measure_from_gen_notes(self):
        """ create a measure by randomly generating
            note durations; ordering them; adding a melody;
            inserting rests

        """
        #generate 100 random note durations
        a = []
        for i in range(100):
            a.append((f"n{i}", self.get_note_with_duration()))
            
        a_sorted = sorted(a,key=lambda x: x[1][2])
        notes = self.greedy_note_duration_selector(a_sorted)
        measure = self.note_seq_to_measure(notes)
        return measure

    def note_seq_to_measure(self,notes):
        """ takes a list of tuples like
                [('n13', (0, 1.0, 1.0)),
                 ('n59', (2, 1.0, 3.0)),
                 ('n0', (5, 1.0, 6.0)),
                 ('n68', (6, 1.0, 7.0)),...]
                 
            get_gaps_in_seq returns a list of tuples like
            [(1.0, 1.0, 2), (3.0, 2.0, 5), (9.0, 1.0, 10), (18.0, 1.0, 19)]
        
        """
        s = stream.Measure()
        
        melody = self.melody(len(notes))
        # find gaps and label as rests
        gap_rests = self.get_gaps_in_seq(notes)
        # build new list of notes+rests
        n_and_r = notes + gap_rests
        # sort
        n_and_r_sorted = sorted(n_and_r,key=lambda x: x[1][2])
        
        # for each protonote in seq assign pitch 
        # sampled from pitches in key
        # pitch <- random choice (from notes_in_key)
        for i in n_and_r_sorted:
            # add quarter note rests where gaps exist
            if i[0] == 'rest':
                rest = note.Rest()
                rest.quarterLength = i[1][1] #length/duration
                rest.offset = i[1][0] #startTime
                s.append(rest)
            # else add notes
            else:
                n = note.Note()
                n.pitch.name = melody.pop()
                n.lyric = i[0] #note id
                n.offset = i[1][0] #startTime
                n.duration.quarterLength = i[1][1] #length/duration
                s.append(n)

        return s


    def get_gaps_in_seq(self,seq):
        """  given seq of duration_tuples, locate gaps between where 
            endTime of tuple n-1 < startTime of tuple n
            eg below, n41's endTime is 18 while n1's startTime is 19,
            thus a gap of 1
             [...,
             ('n71', (14, 2.0, 16.0)),
             ('n41', (16, 2.0, 18.0)),
             ('n1', (19, 1.0, 20.0))]
            return the endTime,startTime as a new (start, dur, end) tuple
            for any gaps found - gaps to be converted to rests of same length
        """
        gaps=[]
        for i in range(1,len(seq)):
            if seq[i-1][1][2] < seq[i][1][0]:
                s, e = seq[i-1][1][2], seq[i][1][0]
                # flag this as a rest
                gaps.append( ('rest',(s,e-s,e)) )
        return gaps


    def create_part_from_measures(self,measures_per_part=4):
        """ generates measures_per_part measures,
            inserts in a stream.Part obj and returns the obj

        """
        part = stream.Part()
        for i in range(1,measures_per_part+1):
            m = self.create_measure_from_gen_notes()
            m.number = i
            part.append(m)
        return part
        

    def create_score_from_parts(self, parts=2,score_title="Piano concerto", composer="Anonymous COMP5030 student"):
        """ given list of stream.Parts
            return a stream.Score w/ each Part stacked together
        """
        # create a score container
        s = stream.Score()

        # insert stacked parts
        for i in range(1,parts+1):
            p = self.create_part_from_measures()
            p.id = f"Part{i}"
            s.insert(0,p)

        # set metadata
        s.insert(0, metadata.Metadata())
        s.metadata.title = f"{score_title} in {str(self.key)}"
        s.metadata.composer = composer
        return s
    
    def part_from_notes_to_str(self, part):
        """ given a stream.Part composed of note.Notes
            returns a string of concatenated pitch names

            use for comparisons
        """
        return "".join([i.name for i in part.pitches])
    
    def generate_candidate_parts(self, num_parts):
        """ given num_parts (int)
            returns a list of candidate stream.Parts w/ id="part{i}"
        """
        return [self.create_part_from_notes(f"part{i}") for i in range(num_parts)]
    
    def get_similar_parts(self, list_of_parts, dist_func=Music21Helper().levenshteinDistanceDP):
        """ given list of candidate parts
            returns subset (list) of most similar parts
        """
        # convert each part to a note_str
        note_str_list = [self.part_from_notes_to_str(i) for i in list_of_parts]

        # create dict of (str1,str2): distance(str1,str2) elements for all combinations
        # of all pairs of parts represented in note_str_list
        d = {}
        for i,j in list(combinations(note_str_list,r=2)):
            d[(i,j)] = dist_func(i,j)

        # convert dict to sorted list
        # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        sorted_str_d = sorted(d.items(), key=lambda item: item[1])

        # get avg dist in dict
        avg = np.round(np.mean([j for i,j in d.items()]))
        
        # return list of (str1,str2) pairs whose dist < avg
        return [i for i,j in sorted_str_d if j < avg]

    def get_note_with_duration(self,measureEndTime=20,qlen = [1.0,2.0,4.0],qlen_prob = [0.15, 0.35, 0.5]):
        """ returns a prenote w/ randomly selected
                duration <- random choice (from quarter,half,whole)
                startTime <- random choice (from 0:measureEnd-duration)
            implicit: endTime = startTime + duration (endTime <= measureEnd)
        """
        start = np.random.choice(range(measureEndTime))
        length = np.random.choice(qlen,p=qlen_prob)
        while start + length > measureEndTime:
            length = np.random.choice(qlen,p=qlen_prob)
        end = start + length
        return (start,length,end)

    def greedy_note_duration_selector(self, a,presorted=True):
        """ early finish note selection 
            given a list of (start,length,end) - "duration" - tuples
            returns a maximum mutually compatible list of note durations    
        """
        if not presorted:
            s = sorted(a,key=lambda x: x[1][2])
        else:
            s = a
        A = []
        A.append(s[0])
        k = 1
        for m in range(1,len(s)):
            if s[m][1][0] >= s[k][1][2]:
                A.append(s[m])
                k = m
        return A

    def play_score(self,print_text=True):
        score = self.create_score_from_parts()
        if print_text:
            score.show('text')
        score.show()





if __name__ == '__main__':

    m = Compose("g-")

    m.play_score(print_text=True)
    #m.play_score() #uncomment if you have MuseScore setup and configured; probably also works for lillypad?


    ### output sample inputs/outputs of greedy to csv
    # a = [(f"n{i}", m.get_note_with_duration()) for i in range(100)]

    # import pandas as pd

    # df = pd.DataFrame(a)
    # df.to_csv("../resources/sample_note_duration_list_input.csv")

    # r = m.greedy_note_duration_selector(a,presorted=False)

    # df2 = pd.DataFrame(r)
    # df2.to_csv("../resources/sample_note_duration_selection_output.csv")



