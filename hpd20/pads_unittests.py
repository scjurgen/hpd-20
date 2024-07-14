#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest

from pad import Pad, Pads


class ScalesTest(unittest.TestCase):
    @staticmethod
    def create_testpads():
        memory_block = bytearray(300000)
        return Pads(memory_block)

    def test_writeReadBlock(self):
        sut = self.create_testpads()
        sut.pads[0].set_pan(0, 100)
        pan = sut.pads[0].get_pan(0)
        self.assertEqual(pan, 100)

if __name__ == '__main__':
    unittest.main()
