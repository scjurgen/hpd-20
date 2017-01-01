from instrumentname import get_instrument_name, get_instrument_pitch
from pad import Pads
from kit import Kits

def getNoteName(value):
    notes = [' C', 'C#', ' D', 'Eb',
             ' E', ' F', 'F#', ' G',
             'Ab', ' A', 'Bb', ' B']
    if value < 0:
        return "--"
    return notes[value % 12]+str(int((value-24)/12));

fh = file('Backup/BKUP-021.HS0', 'rb')
memoryBlock = bytearray(fh.read())

padsMemory = memoryBlock[51596:51596 + 200 * 17 * 68]
kitsMemory = memoryBlock[6922:6922 + 200 * 224]
kits = Kits(kitsMemory)
pads = Pads(padsMemory)
kit = 130
kit -= 1  # zero based

print("Kit {0}: {1} {2}".format(kit+1, kits.get_kit(kit).main_name(), kits.get_kit(kit).sub_name()))

for i in range(0, 17):
    pitch = pads.get_pad(kit * 17 + i).get_pitch(0)
    pitch = pitch + get_instrument_pitch(pads.get_pad(kit * 17 + i).get_patch(0))
    realNote = getNoteName(pitch/100)
    print ("{0}: {1} {2} {3} {4}".format(pads.get_pad_name(i), realNote, pads.get_pad(kit * 17 + i).get_volume(0),
                                     get_instrument_name(pads.get_pad(kit * 17 + i).get_patch(0)),
                                     pads.get_pad(kit * 17 + i).get_pitch(0)))



class Operations:

    def putScale(self, scale, instrumentset):
        self.scale = scale
        self.instrumentset = instrumentset
