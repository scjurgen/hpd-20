

class MemoryOp:

    @staticmethod
    def get_int8(mem_view:memoryview, index: int):
        value = mem_view[index]
        if value > 127:
            return -(256 - value)
        return value

    @staticmethod
    def set_int8(mem_view:memoryview, index: int, value: int):
        if mem_view[index] != value & 0xff:
            print("value set: old: ", mem_view[index])
            mem_view[index] = value & 0xff
            print("value set: new: ", mem_view[index])

    @staticmethod
    def get_unsigned_int8(mem_view:memoryview, index: int):
        value = mem_view[index]
        return value

    @staticmethod
    def get_int16(mem_view:memoryview, index: int):
        value = mem_view[index] * 256 + mem_view[index + 1]
        if value > 32767:
            return -(65536 - value)
        return value

    @staticmethod
    def set_int16(mem_view:memoryview, index: int, value: int):
        mem_view[index] = (value >> 8) & 0xff
        mem_view[index + 1] = value & 0xff

    @staticmethod
    def get_unsigned_int16(mem_view:memoryview, index: int):
        value = mem_view[index] * 256 + mem_view[index + 1]
        return value

    @staticmethod
    def set_unsigned_int16(mem_view:memoryview, index: int, value: int):
        mem_view[index] = (value >> 8) & 0xff
        mem_view[index + 1] = value & 0xff

    @staticmethod
    def get_string(mem_view:memoryview, index:int, size:int):
        if index < 0 or index + size > len(mem_view):
            raise ValueError("Index and size out of bounds of the memoryview")
        char_list = []

        for i in range(index, index + size):
            byte_value = mem_view[i]
            if byte_value == 0:
                break
            else:
                char_list.append(chr(byte_value))
        extracted_string = ''.join(char_list)
        return extracted_string

    @staticmethod
    def set_string(mem_view:memoryview, index:int, string:str):
        encoded_string = string.encode('utf-8') + b'\x00'
        if index < 0 or index + len(encoded_string) > len(mem_view):
            raise ValueError("Index and encoded string length out of bounds of the memoryview")
        mem_view[index:index + len(encoded_string)] = encoded_string
