from os import mkdir

from instrumentname import get_instrument_name, get_instrument_pitch
from pad import Pads
from kit import Kits
import hashlib

CHAIN_MEMINDEX = 1180
CHAIN_MEMSIZE = 128

KIT_MEMINDEX = 6922
KIT_MEMSIZE = 224

PAD_MEMINDEX = 51596
PAD_MEMSIZE = 68

CHAINS_COUNT = 15
PADS_PER_KIT = 17
KITS_COUNT = 200
PADS_COUNT = KITS_COUNT * PADS_PER_KIT


def getNoteName(value):
    notes = [' C', 'C#', ' D', 'Eb',
             ' E', ' F', 'F#', ' G',
             'Ab', ' A', 'Bb', ' B']
    if value < 0:
        return "--"
    return notes[value % len(notes)] + str(int((value - 2*len(notes)) / len(notes)))


class HPD:
    def __init__(self, file_name):
        fh = file(file_name, 'rb')
        memory_block = bytearray(fh.read())
        self.md5_memory = memory_block[-16:]
        print(" ".join(hex(n) for n in self.md5_memory))

        self.memoryBlock = memory_block[0:-16]   # strip md5
        pads_memory = memory_block[PAD_MEMINDEX:PAD_MEMINDEX +PADS_COUNT * PAD_MEMSIZE]
        kits_memory = memory_block[KIT_MEMINDEX:KIT_MEMINDEX + KITS_COUNT * KIT_MEMSIZE]
        self.kits = Kits(kits_memory)
        self.pads = Pads(pads_memory)

    def showkit(self, kit):
        kit -= 1  # zero based

        print("Kit {0}: {1} {2}".format(kit + 1, self.kits.get_kit(kit).main_name(), self.kits.get_kit(kit).sub_name()))
        for i in range(0, PADS_PER_KIT):
            pitch = self.pads.get_pad(kit * PADS_PER_KIT + i).get_pitch(0)
            pitch = pitch + get_instrument_pitch(self.pads.get_pad(kit * PADS_PER_KIT + i).get_patch(0))
            real_note = getNoteName(pitch / 100)
            print("{0}: {1} {2} {3} {4}".format(self.pads.get_pad_name(i), real_note,
                                                self.pads.get_pad(kit * PADS_PER_KIT + i).get_volume(0),
                                                get_instrument_name(self.pads.get_pad(kit * PADS_PER_KIT + i).get_patch(0)),
                                                self.pads.get_pad(kit * PADS_PER_KIT + i).get_pitch(0)))

    def save_file(self, file_name):
        m = hashlib.md5()
        m.update(str(self.memoryBlock))
        md5_digest = m.digest()
        fh = file(file_name, 'wb')
        fh.write(self.memoryBlock)
        print(" ".join(hex(ord(n)) for n in md5_digest))
        fh.write(md5_digest)

    def putScale(self, scale, instrumentset):
        pass

    def loadPadFromKit(self, file_name, target_index_kit, target_index_pad):
        pass

    def save_kit(self, kit_index, file_name, inc_filename_ifexists = False):
        try:
            if inc_filename_ifexists:
                pass

            fh = file(file_name, 'wb')
            kit = self.kits.get_kit(kit_index)
            kit.save(fh)
            for pad_index in range(PADS_PER_KIT):
                pad = self.pads.get_pad(PADS_PER_KIT*kit_index+pad_index)
                pad.save(fh)
        except Exception as e:
            print("Exception {0}".format(e))

    def load_kit(self, kit_index, file_name):
        try:
            fh = file(file_name, 'rb')
            kit = self.kits.get_kit(kit_index)
            kit.load(fh)
            for pad_index in range(PADS_PER_KIT):
                final_pad_index = PADS_PER_KIT*kit_index+pad_index
                pad = self.pads.get_pad(final_pad_index)
                pad.load(fh)
                hpd.memoryBlock[PAD_MEMINDEX + PAD_MEMSIZE * final_pad_index:PAD_MEMINDEX + PAD_MEMSIZE * (final_pad_index + 1)] = pad.memory_block
            hpd.memoryBlock[KIT_MEMINDEX + KIT_MEMSIZE * kit_index:KIT_MEMINDEX + KIT_MEMSIZE * (kit_index+1)] = kit.memory_block
        except Exception as e:
            print("Exception {0}".format(e))

    def create_kit_filename(self, kit_index):
        kit = self.kits.get_kit(kit_index)
        kit_name = kit.main_name().strip()
        if len(kit.sub_name().strip()) != 0:
            kit_name += " (" + kit.sub_name().strip() + ")"
        kit_as_file_name = "kits/" + "".join(
            [x if x.isalnum() or x in ['!', '&', '(', ')', '_', '.', '{', '}', ' '] else "_" for x in kit_name])
        return kit_as_file_name + ".kit"

    def save_all_kits(self):
        for kit_index in range(KITS_COUNT):
            self.save_kit(kit_index, self.create_kit_filename(kit_index))


# some tests for now
hpd = HPD('Backup/BKUP-022.HS0')
hpd.showkit(130)
hpd.showkit(151)
hpd.showkit(53)
hpd.load_kit(188, "kits/Brushes.kit")
hpd.save_file('BKUP-001.HS0')

# mkdir('kits')
# hpd.save_all_kits()


