
#class MapPatchSomehow
from memoryops import MemoryOp

NAME_INDEX = 2
SUBNAME_INDEX = 14


class Kit:
    def __init__(self, memory_block):
        self.memory_block = memory_block

    def main_name(self):
        return MemoryOp.get_string(self.memory_block, NAME_INDEX, 12)

    def sub_name(self):
        return MemoryOp.get_string(self.memory_block, SUBNAME_INDEX, 16)


class Kits:
    def __init__(self, memory_block):
        self.memory_block = memory_block
        self.kits = []
        for i in range(200):
            slice_block = self.memory_block[224*i:224*(i+1)]
            self.kits.append(Kit(slice_block))

    def get_kit(self, index):
        return self.kits[index]



