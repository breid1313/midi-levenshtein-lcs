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

class TestLCS(unittest.TestCase):

    def testUnique(self):
        token1 = "AAAAAAAAAAA"
        token2 = "BBBBBBBBBBB"

        lcs = helper.lcsDP(token1, token2)

        assert int(lcs) == 0

    def testIdentical(self):
        token1 = token2 = "testString"

        lcs = helper.lcsDP(token1, token2)

        assert int(lcs) == len(token1)

    def testLCS(self):
        token1 = "AAAAABAAAA"
        token2 = "BBBBBBBBBB"

        lcs = helper.lcsDP(token1, token2)

        assert int(lcs) == 1

if __name__ == '__main__':
    unittest.main()
