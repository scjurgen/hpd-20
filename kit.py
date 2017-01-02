
#class MapPatchSomehow
from __builtin__ import file

from memoryops import MemoryOp

NAME_INDEX = 2
SUBNAME_INDEX = 14
KIT_MEMSIZE = 224

VOL_INDEX = 30
HH_VOL_INDEX = 31
BALANCE_INDEX = 67
PAD_SENSITIVITY = 55

class Kit:
    def __init__(self, memory_block):
        self.memory_block = memory_block

    def main_name(self):
        return MemoryOp.get_string(self.memory_block, NAME_INDEX, 12)

    def sub_name(self):
        return MemoryOp.get_string(self.memory_block, SUBNAME_INDEX, 16)

    def save(self, fh):
        fh.write(self.memory_block)

    def load(self, fh):
        self.memory_block = fh.read(KIT_MEMSIZE)


class Kits:
    def __init__(self, memory_block):
        self.memory_block = memory_block
        self.kits = []
        for i in range(200):
            slice_block = self.memory_block[KIT_MEMSIZE*i:KIT_MEMSIZE*(i+1)]
            self.kits.append(Kit(slice_block))

    def get_kit(self, index):
        return self.kits[index]



