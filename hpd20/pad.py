
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

    def __init__(self, memory_block, index):
        self.memory_block = memory_block
        self.index = index

    def get_volume(self, layer):
        return self.memory_block[self.index+Pad.VOL_INDEX + layer]

    def set_volume(self, layer, value):
        self.memory_block[self.index+Pad.VOL_INDEX + layer] = value

    def get_pan(self, layer):
        return MemoryOp.get_int8(self.memory_block, self.index+Pad.PAN_INDEX + layer)

    def set_pan(self, layer, value):
        MemoryOp.set_int8(self.memory_block, self.index+Pad.PAN_INDEX + layer, value)

    def get_color(self, layer):
        return self.memory_block[self.index+Pad.COLOR_INDEX + layer]

    def set_color(self, layer, value):
        self.memory_block[self.index+Pad.COLOR_INDEX + layer] = value

    def get_sweep(self, layer):
        return MemoryOp.get_int8(self.memory_block,self.index+ Pad.SWEEP_INDEX + layer)

    def set_sweep(self, layer, value):
        MemoryOp.set_int8(self.memory_block, self.index+Pad.SWEEP_INDEX + layer, value)

    def get_ambientsend(self, layer):
        return self.memory_block[self.index+Pad.AMB_INDEX + layer]

    def set_ambientsend(self, layer, value):
        self.memory_block[self.index+Pad.AMB_INDEX + layer] = value

    def get_muffling(self, layer):
        return self.memory_block[self.index+Pad.MUFFLING_INDEX + layer]

    def set_muffling(self, layer, value):
        self.memory_block[self.index+Pad.MUFFLING_INDEX + layer] = value

    def get_patch(self, layer):
        return MemoryOp.get_unsigned_int16(self.memory_block, self.index+Pad.PATCH_INDEX + layer * 2)

    def set_patch(self, layer, patch_number):
        MemoryOp.set_unsigned_int16(self.memory_block, self.index+Pad.PATCH_INDEX + layer * 2, patch_number)

    def get_internal_patch(self, layer):
        return MemoryOp.get_unsigned_int16(self.memory_block, self.index+Pad.PATCH_INTERNAL_INDEX + layer * 2)

    def set_internal_patch(self, layer, value):
        MemoryOp.set_unsigned_int16(self.memory_block, self.index+Pad.PATCH_INTERNAL_INDEX + layer * 2, value)

    def get_pitch(self, layer):
        return MemoryOp.get_int16(self.memory_block, self.index+Pad.PITCH_INDEX + layer * 2)

    def set_pitch(self, layer, pitch):
        MemoryOp.set_int16(self.memory_block, self.index+Pad.PITCH_INDEX + layer * 2, pitch)

    def get_midi(self):
        return self.memory_block[self.index+Pad.MIDI_INDEX]

    def set_midi(self, value):
        self.memory_block[self.index+Pad.MIDI_INDEX] = value

    def get_layer(self):
        return self.memory_block[self.index+Pad.LAYER_INDEX]

    def set_layer(self, value):
        self.memory_block[self.index+Pad.LAYER_INDEX] = value

    def get_velofade(self):
        return self.memory_block[self.index+Pad.FADE_VALUE_INDEX]

    def set_velofade(self, value):
        self.memory_block[self.index+Pad.FADE_VALUE_INDEX] = value

    def get_trigger(self):
        return self.memory_block[self.index+Pad.TRIGGER_INDEX]

    def set_trigger(self, value):
        self.memory_block[self.index+Pad.TRIGGER_INDEX] = value

    def get_fixvelo(self):
        return self.memory_block[self.index+Pad.FIX_VELOCITY_INDEX]

    def set_fixvelo(self, value):
        self.memory_block[self.index+Pad.FIX_VELOCITY_INDEX] = value

    def get_mute_group(self):
        return self.memory_block[self.index+Pad.FIX_GROUP_INDEX]

    def set_mute_group(self, value):
        self.memory_block[self.index+Pad.FIX_GROUP_INDEX] = value

    def get_mono_poly(self):
        return self.memory_block[self.index+Pad.MONO_POLY_INDEX]

    def set_mono_poly(self, value):
        self.memory_block[self.index+Pad.MONO_POLY_INDEX] = value

    def save(self, fh):
        slice_view = memoryview(self.memory_block)[self.index:self.index + 68]
        fh.write(slice_view)

    def load(self, fh):
        slice_view = memoryview(self.memory_block)[self.index:self.index + 68]
        slice_view = fh.readinto(68)


class Pads:
    def __init__(self, memory_block, indexFrom, indexTo):
        self.indexFrom = indexFrom
        self.memory_block = memory_block
        self.pads = []
        self.pad_names = ['M1', 'M2', 'M3', 'M4', 'M5',
                          'S1', 'S2', 'S3', 'S4',
                          'S5', 'S6', 'S7', 'S8',
                          'D-Beam', 'Head', 'Rim', 'HH']
        for i in range(17 * 200):
            self.pads.append(Pad(memory_block, indexFrom+68 * i))

    def get_pad_name(self, index):
        return self.pad_names[index]

    def get_pad(self, index):
        return self.pads[index]
