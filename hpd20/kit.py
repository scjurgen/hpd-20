from memoryops import MemoryOp

NAME_INDEX = 2
SUBNAME_INDEX = 14
KIT_MEMSIZE = 224

VOL_INDEX = 30
HH_VOL_INDEX = 31
BALANCE_INDEX = 67
PAD_SENSITIVITY = 55

class Kit:
    def __init__(self, memory_block, index):
        self.index = index
        self.memory_block = memory_block

    def main_name(self):
        value = MemoryOp.get_string(self.memory_block, self.index+NAME_INDEX, 12)
        return value

    def sub_name(self):
        return str(MemoryOp.get_string(self.memory_block, self.index+SUBNAME_INDEX, 16))

    def get_volume(self):
        return MemoryOp.get_unsigned_int8(self.memory_block, self.index+VOL_INDEX)

    def get_hh_volume(self):
        return MemoryOp.get_unsigned_int8(self.memory_block, self.index+HH_VOL_INDEX)

    def get_balance(self):
        return MemoryOp.get_int8(self.memory_block, self.index+BALANCE_INDEX)

    def get_pad_sensitvity(self):
        return MemoryOp.get_int8(self.memory_block, self.index+PAD_SENSITIVITY)

    def save(self, fh):
        fh.write(self.memory_block)

    def load(self, fh):
        self.memory_block = fh.read(KIT_MEMSIZE)


class Kits:
    def __init__(self, memory_block, indexFrom, indexTo):
        self.indexFrom = indexFrom
        self.indexTo = indexTo
        self.memory_block = memory_block
        self.kits = []
        for i in range(200):
            self.kits.append(Kit(self.memory_block, self.indexFrom+KIT_MEMSIZE*i))

    def get_list_of_kits(self):
        res = []
        for i in range(200):
            res.append(str(i+1) + " " + self.kits[i].main_name().strip())
        return res

    def get_kit(self, index):
        return self.kits[index]



