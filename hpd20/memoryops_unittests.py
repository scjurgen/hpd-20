
import unittest

from memoryops import MemoryOp


def create_testblock():
    return bytearray([i % 256 for i in range(512)])


class ScalesTest(unittest.TestCase):

    def test_fetch8bit(self):
        test_block = create_testblock()
        self.assertEqual(1, MemoryOp.get_unsigned_int8(test_block, 1))
        self.assertEqual(129, MemoryOp.get_unsigned_int8(test_block, 129))
        self.assertEqual(-1, MemoryOp.get_int8(test_block, 255))

    def test_fetch16bit(self):
        test_block = create_testblock()
        #0x01 0x02 = 256+2
        self.assertEqual(258, MemoryOp.get_unsigned_int16(test_block, 1))
        #0xfe 0xff = 65279
        self.assertEqual(65279, MemoryOp.get_unsigned_int16(test_block, 254))

    def test_fetch_string(self):
        test_block = create_testblock()
        print(MemoryOp.get_string(test_block, 48, 4))
        self.assertEqual("0123", "0123")
        pass

if __name__ == '__main__':
    unittest.main()
