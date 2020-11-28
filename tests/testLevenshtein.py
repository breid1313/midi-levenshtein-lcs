# -*- coding: utf-8 -*-

import unittest
import sys
import os

# add ../modules to the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "modules"))
# add ../lib to the system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from helpers import Music21Helper

helper = Music21Helper()

class TestLevenshtein(unittest.TestCase):

    def testUnique(self):
        token1 = "AAAAAAAAAAA"
        token2 = "BBBBBBBBBBB"

        lev = helper.levenshteinDistanceDP(token1, token2)

        assert int(lev) == len(token1)

    def testIdentical(self):
        token1 = token2 = "testString"

        lev = helper.levenshteinDistanceDP(token1, token2)

        assert int(lev) == 0

if __name__ == '__main__':
    unittest.main()
