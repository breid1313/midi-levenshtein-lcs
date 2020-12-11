# -*- coding: utf-8 -*-

# Analysis for the main driver code underlying the LCS and Lev modules.
# We will analyize only this algorithmic code.
# We will not be analyzing the time that it takes the music21 helper
# to read and convert MIDI files into a workable format.

import random
import string
import time
import os
import sys
import argparse
import matplotlib.pyplot as plt

# add ../modules to the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "modules"))
# add ../lib to the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from helpers import Music21Helper

class TestGenerator():
    def __init__(self):
        self.helper = Music21Helper()

    @staticmethod
    def generateString(size, allowed_chars=string.ascii_letters):
        return ''.join(random.choice(allowed_chars) for i in range(size))

    def testCaseLCS(self, input_size, iterations):
        times = []
        for i in range(iterations):
            print("Starting iteration {}".format(i))
            token1 = self.generateString(input_size)
            token2 = self.generateString(input_size)
            start_time = time.time()
            self.helper.lcsDP(token1, token2)
            elapsed = time.time() - start_time
            times.append(elapsed)
            print("Iteration {} complete".format(i))
        return times

    def testCaseLevenshtein(self, input_size, iterations):
        times = []
        for i in range(iterations):
            print("Starting iteration {}".format(i))
            token1 = self.generateString(input_size)
            token2 = self.generateString(input_size)
            start_time = time.time()
            self.helper.levenshteinDistanceDP(token1, token2)
            elapsed = time.time() - start_time
            times.append(elapsed)
            print("Iteration {} complete".format(i))
        return times

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--input-size', nargs='+', help='Input sizes to run. ex: -s 10 100 1000', required=True)
    parser.add_argument('-i', '--iterations', help='Number of iterations to run for each input size', required=True)
    args = parser.parse_args()

    input_size = args.input_size
    iterations = args.iterations

    if input_size == ['big']:
        r = range(10000)
        input_size = [num for num in r if num % 100 == 0]

    print("recieved input size(s): " + str(input_size))
    print("received iteration count: " + str(iterations))

    testGen = TestGenerator()

    plt.xlabel("Input size")
    plt.ylabel("Running time")

    avg_times = []

    # get times for running LCS
    print("========== Beginning LCS Tests ===========")
    for size in input_size:
        print("running test for size {}".format(size))
        times = testGen.testCaseLCS(int(size), int(iterations))
        average = sum(times)/len(times)
        avg_times.append(average)

    # plot LCS
    plt.plot(input_size, avg_times, label="LCS Runtime")

    # clear times
    avg_times = []

    # get times for running Lev
    print("========== Beginning Levenshtein Tests ===========")
    for size in input_size:
        print("running test for size {}".format(size))
        times = testGen.testCaseLCS(int(size), int(iterations))
        average = sum(times)/len(times)
        avg_times.append(average)

    # plot Lev
    plt.plot(input_size, avg_times, label="Levenshtein Runtime")

    plt.legend()
    plt.show()