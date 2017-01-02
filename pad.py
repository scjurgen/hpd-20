# class MapPatchSomehow
from memoryops import MemoryOp

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


class Pad:
    def __init__(self, memory_block):
        self.memory_block = memory_block

    def get_volume(self, instrument):
        return self.memory_block[VOL_INDEX + instrument]

    def get_pan(self, instrument):
        return self.memory_block[PAN_INDEX + instrument]

    def get_color(self, instrument):
        return self.memory_block[COLOR_INDEX + instrument]

    def get_sweep(self, instrument):
        return self.memory_block[SWEEP_INDEX + instrument]

    def get_muffling(self, instrument):
        return self.memory_block[MUFFLING_INDEX + instrument]

    def get_patch(self, instrument):
        return MemoryOp.get_unsigned_int16(self.memory_block, PATCH_INDEX + instrument * 2)

    def get_internal_patch(self, instrument):
        return MemoryOp.get_unsigned_int16(self.memory_block, PATCH_INTERNAL_INDEX + instrument * 2)

    def get_pitch(self, instrument):
        return MemoryOp.get_int16(self.memory_block, PITCH_INDEX + instrument * 2)

    def get_midi(self):
        return self.memory_block[MIDI_INDEX]

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
