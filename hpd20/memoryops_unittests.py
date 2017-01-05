#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest

from memoryops import MemoryOp


class ScalesTest(unittest.TestCase):
    @staticmethod
    def create_testblock():
        return bytearray([i % 256 for i in range(512)])

    def test_fetch8bit(self):
        test_block = ScalesTest.create_testblock()
        self.assertEqual(1, MemoryOp.get_unsigned_int8(test_block, 1))
        self.assertEqual(129, MemoryOp.get_unsigned_int8(test_block, 129))
        self.assertEqual(-1, MemoryOp.get_int8(test_block, 255))

    def test_write8bit(self):
        test_block = ScalesTest.create_testblock()
        MemoryOp.set_int8(test_block, 1, 2)
        self.assertEqual(2, MemoryOp.get_unsigned_int8(test_block, 1))
        MemoryOp.set_int8(test_block, 129, -6)
        self.assertEqual(250, MemoryOp.get_unsigned_int8(test_block, 129))
        self.assertEqual(-6, MemoryOp.get_int8(test_block, 129))

    def test_fetch16bit(self):
        test_block = ScalesTest.create_testblock()
        #0x01 0x02 = 256+2
        self.assertEqual(258, MemoryOp.get_unsigned_int16(test_block, 1))
        #0xfe 0xff = 65279
        self.assertEqual(65279, MemoryOp.get_unsigned_int16(test_block, 254))
        self.assertEqual(-257, MemoryOp.get_int16(test_block, 254))

    def test_write16bit(self):
        test_block = ScalesTest.create_testblock()
        MemoryOp.set_int16(test_block, 1, -2)
        self.assertEqual(-2, MemoryOp.get_int16(test_block, 1))
        MemoryOp.set_unsigned_int16(test_block, 1, 0x8990)
        self.assertEqual(0x8990, MemoryOp.get_unsigned_int16(test_block, 1))

    def test_fetch_string(self):
        test_block = ScalesTest.create_testblock()
        self.assertEqual("01234567", MemoryOp.get_string(test_block, 48, 8))

    def test_write_string(self):
        test_block = ScalesTest.create_testblock()
        MemoryOp.set_string(test_block, 48, "foobar??")
        self.assertEqual("foobar??", MemoryOp.get_string(test_block, 48, 8))
        MemoryOp.set_string(test_block, 54, "!!")
        self.assertEqual("foobar!!", MemoryOp.get_string(test_block, 48, 8))


if __name__ == '__main__':
    unittest.main()
