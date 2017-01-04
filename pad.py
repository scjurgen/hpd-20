
from memoryops import MemoryOp


class Pad:
    VOL_INDEX = 0
    AMB_INDEX = 2
    PATCH_INDEX = 4
    PATCH_INTERNAL_INDEX = 8
    PITCH_INDEX = 12
    MUFFLING_INDEX = 16
    PAN_INDEX = 18
    COLOR_INDEX = 23
    MFX_ASSIGN_INDEX = 25
    SWEEP_INDEX = 27
    MIDI_INDEX = 33
    MIDI_GATE_INDEX = 34
    SEND_ALL_PADS_INDEX = 36
    SEND_TO_KIT_INDEX = 37
    REC_PITCH_INDEX = 39
    MUTE_INDEX = 40
    RT_PITCH_INDEX = 41
    ROLL_INDEX = 42
    LAYER_INDEX = 43
    FADE_VALUE_INDEX = 44
    TRIGGER_INDEX = 45
    FIX_VELOCITY_INDEX = 47
    FIX_GROUP_INDEX = 48
    MONO_POLY_INDEX = 49

    def __init__(self, memory_block):
        self.memory_block = memory_block

    def get_volume(self, layer):
        return self.memory_block[Pad.VOL_INDEX + layer]

    def get_pan(self, layer):
        return self.memory_block[Pad.PAN_INDEX + layer]

    def get_color(self, layer):
        return self.memory_block[Pad.COLOR_INDEX + layer]

    def get_sweep(self, layer):
        return self.memory_block[Pad.SWEEP_INDEX + layer]

    def get_muffling(self, layer):
        return self.memory_block[Pad.MUFFLING_INDEX + layer]

    def get_patch(self, layer):
        return MemoryOp.get_unsigned_int16(self.memory_block, Pad.PATCH_INDEX + layer * 2)

    def set_patch(self, layer, patch_number):
        MemoryOp.set_unsigned_int16(self.memory_block, Pad.PATCH_INDEX + layer * 2, patch_number)

    def get_internal_patch(self, layer):
        return MemoryOp.get_unsigned_int16(self.memory_block, Pad.PATCH_INTERNAL_INDEX + layer * 2)

    def set_internal_patch(self, layer, value):
        MemoryOp.set_unsigned_int16(self.memory_block, Pad.PATCH_INTERNAL_INDEX + layer * 2, value)

    def get_pitch(self, layer):
        return MemoryOp.get_int16(self.memory_block, Pad.PITCH_INDEX + layer * 2)

    def set_pitch(self, layer, pitch):
        MemoryOp.set_int16(self.memory_block, Pad.PITCH_INDEX + layer * 2, pitch)

    def get_midi(self):
        return self.memory_block[Pad.MIDI_INDEX]

    def get_layer(self):
        return self.memory_block[Pad.LAYER_INDEX]

    def save(self, fh):
        fh.write(self.memory_block)

    def load(self, fh):
        self.memory_block = fh.read(68)


class Pads:
    def __init__(self, memory_block):
        self.memory_block = memory_block
        self.pads = []
        self.pad_names = ['M1', 'M2', 'M3', 'M4', 'M5',
                          'S1', 'S2', 'S3', 'S4',
                          'S5', 'S6', 'S7', 'S8',
                          'D-Beam', 'Head', 'Rim', 'HH']
        for i in range(17 * 200):
            sliced_memory = self.memory_block[68 * i:68 * (i + 1)]
            self.pads.append(Pad(sliced_memory))

    def get_pad_name(self, index):
        return self.pad_names[index]

    def get_pad(self, index):
        return self.pads[index]
