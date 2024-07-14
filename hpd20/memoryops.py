

class MemoryOp:

    @staticmethod
    def get_int8(memory_block, index: int):
        value = memory_block[index]
        if value > 127:
            return -(256 - value)
        return value

    @staticmethod
    def set_int8(memory_block, index: int, value: int):
        if memory_block[index] != value & 0xff:
            print("value set: old: ", memory_block[index])
            memory_block[index] = value & 0xff
            print("value set: new: ", memory_block[index])

    @staticmethod
    def get_unsigned_int8(memory_block, index: int):
        value = memory_block[index]
        return value

    @staticmethod
    def get_int16(memory_block, index: int):
        value = memory_block[index] * 256 + memory_block[index + 1]
        if value > 32767:
            return -(65536 - value)
        return value

    @staticmethod
    def set_int16(memory_block, index: int, value: int):
        memory_block[index] = (value >> 8) & 0xff
        memory_block[index + 1] = value & 0xff

    @staticmethod
    def get_unsigned_int16(memory_block, index: int):
        value = memory_block[index] * 256 + memory_block[index + 1]
        return value

    @staticmethod
    def set_unsigned_int16(memory_block, index: int, value: int):
        memory_block[index] = (value >> 8) & 0xff
        memory_block[index + 1] = value & 0xff

    @staticmethod
    def get_string(memory_block, index:int, size:int):
        return memory_block[index:index+size].decode('utf-8')

    @staticmethod
    def set_string(memory_block, index:int, string:str):
        memory_block[index:index+len(string)] = string
