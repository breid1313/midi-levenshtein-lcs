# Overview

This repository contains an implementations of Levenstein Metric (Edit Distance) and Longest Common Subsequence
algorithms applied to music. Both algorithms are implemented using a dynammic programming, bottom-up approach.
The main algorithmic code can be found in `lib/helpers.py` in the `Music21Helper`. Fittingly, the two
methods are named `levensteinDistanceDP` and `lcsDP`.

## Contents

### data/
The `data/` directory contains about two dozen string quartets by Mozart and Haydn in MIDI
(Musical Instrument Digital Interface) format. We chose to work with MIDI file because they are significantly
more compact than other file formats such as MP3 or MP4 files.
Additionally, MIDI files contain "instructional" data that is very useful in analyzing music using string matching methods.
That instructional data consists of a pitch, duration, and velocity (relative volume) for every note by the score on an instrument-by-instrument basis. 

### lib/
The `lib/` directory contains `helpers.py` which consists of a `Music21Helper` class.
This class contains numerous methods that assist in converting MIDI data to a string of note letter names so that we may apply string matching techniques.
This class also contains the main algorithmic code that we use to compare music.

### modules/
The `modules/` directory contains two scripts that facilitate easy demonstration of the algorithmic code in the `Music21Helper`. See [running the code](#running-the-code) for how to do this.

### tests/
The `tests/` directory contains unit tests for the Levenshtein Distance (`testLevenshtein.py`) and LCS (`testLCS.py`) code. The unit tests are very simple and are designed to ensure that we are receiving the proper output from the implementations of our algorithms given a few short strings.

In this directory we also have `analyze.py`, which can be used to analyze the performance of the Levenshtein and LCS implementation.

## Running the Code

### Dependencies

The implementation of these algorithms depends on only two non-standard Python libraries: `music21` and `numpy`.
If you wish to execute the runtime analysis file, `tests/analysis.py`, you must also install `matplotlib`.

- Install music21: `pip install music21`
- Install numpy: `pip install numpy`
- Install matplotlib: `pip install matplotlib`

### Sample Input/Output

To produce an example input/output for each of the algorithms, two scripts have been provided in the `modules/` directory.

#### Levenstein Distance

From the root of the repository, run `python3 modules/composition_levenstein_score.py`.
At runtime, two string quartets will be randomly selected from `data/` (they can be the same).
A series of pre-processing steps will them be taken in order to convert the data into a workable format.
Finally, a part will be randomly selected from each composition (canonically, a string quartet
consists of Violin I, Violin II, Viola, and Cello) for comparison.
Lastly, we compute the Levenstein Distance between the two processed parts and print the results.

#### Longest Commonsubsequence
From the root of the repository, run `python3 modules/composition_lcs_score.py`. The same selection and pre-processing steps will occur as in the above section. Then, the LCS of the two selected parts is calculated and we print the results.

### Unit tests
The unit tests can easily be run for either the Levenstein or LCS implementation by running
`python3 tests/testLCS.py` or `python3 tests/testLevenshtein.py`.

### Running Time Analysis
To view a graph of the running time for the Levenstein and LCS implementations, leverage the `tests/analyze.py`.
The script takes two mandatory flags: `-s/--input-size` and `-i/--iterations`.

Pass a series of numbers to the `-s/--input-size` flag to designate the input sizes to test the implementation on. You may also pass `-s big` to the script to run input sizes 10-10,000 in increments of 100.

Pass an integer to the `-i/--iterations` to specify the number of test interations to perform for each input size.

For example:

`python3 tests/analyze.py -s 500 1000 1500 2000 -i 5`

will perform analysis on input sizes 500, 1000, 1500, and 2000 with 5 iterations per input size.

The analysis will randomly generate a string of the desired input size for each iteration, and pass that input to the Levenshtein or LCS implementation.
All analysis is done first on the Levenshtein implementaion before moving on to LCS.
Upon test completion, `matplotlib` will show a graph of both algorithms with input size on the x-axis and running time on the y-axis.