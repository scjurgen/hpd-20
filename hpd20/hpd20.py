#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import mkdir

import sys

from instrumentname import get_instrument_name, get_instrument_pitch
from melodypadpattern import melody_pad_pattern
from pad import Pads
from kit import Kits
import hashlib

from scales import Scale

version = "0.0.8"


class Semantics:
    pad_names = ['M1 ◵', 'M2 ◶', 'M3 ◴', 'M4 ◷', 'M5 ●',
                 'S1', 'S2', 'S3', 'S4',
                 'S5', 'S6', 'S7', 'S8',
                 'D-Beam', 'Head', 'Rim', 'HH']

def get_note_name(value):
    notes = [' C', 'C#', ' D', 'Eb',
             ' E', ' F', 'F#', ' G',
             'Ab', ' A', 'Bb', ' B']
    if value < 0:
        return "--"
    return notes[int(value % len(notes))] + str(int((value - 2*len(notes)) / len(notes)))


class hpd:
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

    def __init__(self, file_name: str):
        print("loading file {0}".format(file_name))
        with open(file_name, 'rb') as fh:
            memory_block = bytearray(fh.read())
        self.md5_memory = memory_block[-16:]
        print(" ".join(hex(n) for n in self.md5_memory))

        self.memoryBlock = memory_block[0:-16]   # strip md5
        self.kits = Kits(self.memoryBlock, hpd.KIT_MEMINDEX, hpd.KIT_MEMINDEX + hpd.KITS_COUNT * hpd.KIT_MEMSIZE)
        self.pads = Pads(self.memoryBlock, hpd.PAD_MEMINDEX, hpd.PAD_MEMINDEX + hpd.PADS_COUNT * hpd.PAD_MEMSIZE)

    def digest_kits(self):
        result = "Kits:\n"
        for i in range(hpd.KITS_COUNT):
            result += str(i+1) + ':\t'
            result += self.kits.get_kit(i).main_name().strip()
            result += '\t' + self.kits.get_kit(i).sub_name().strip()
            result += '\n'
        return result

    def digest_single_kit(self, kit: int):
        kit -= 1  # zero based

        result = "Kit {0}: {1} {2}\n".format(kit + 1, self.kits.get_kit(kit).main_name(), self.kits.get_kit(kit).sub_name())
        for i in range(0, hpd.PADS_PER_KIT):
            pitch = self.pads.get_pad(kit * hpd.PADS_PER_KIT + i).get_pitch(0)
            pitch = pitch + get_instrument_pitch(self.pads.get_pad(kit * hpd.PADS_PER_KIT + i).get_patch(0))
            real_note = get_note_name((pitch+50) / 100)
            result += "{0}: {1} {2} {3} {4}\n".format(self.pads.get_pad_name(i), real_note,
                                                      self.pads.get_pad(kit * hpd.PADS_PER_KIT + i).get_volume(0),
                                                      get_instrument_name(self.pads.get_pad(kit * hpd.PADS_PER_KIT + i).get_patch(0)),
                                                      self.pads.get_pad(kit * hpd.PADS_PER_KIT + i).get_pitch(0))
        result += '\n'
        return result

    def save_file(self, file_name: str):

        m = hashlib.md5()
        m.update(self.memoryBlock)
        md5_digest = m.digest()
        with open(file_name, 'wb') as fh:
            fh.write(self.memoryBlock)
            print(" ".join(hex(n) for n in md5_digest))
            fh.write(md5_digest)

    def save_kit(self, kit_index: int, file_name: str, inc_filename_if_exists: bool=False):
        try:
            if inc_filename_if_exists:
                pass

            with open(file_name, 'wb') as fh:
                kit = self.kits.get_kit(kit_index)
                kit.save(fh)
                for pad_index in range(hpd.PADS_PER_KIT):
                    pad = self.pads.get_pad(hpd.PADS_PER_KIT * kit_index + pad_index)
                    pad.save(fh)
        except Exception as e:
            print("Exception {0}".format(e))

    def load_kit(self, kit_index:int, file_name:str):
        try:
            with open(file_name, 'rb') as fh:
                kit = self.kits.get_kit(kit_index)
                kit.load(fh)
                for pad_index in range(hpd.PADS_PER_KIT):
                    final_pad_index = hpd.PADS_PER_KIT * kit_index + pad_index
                    pad = self.pads.get_pad(final_pad_index)
                    pad.load(fh)
                    self.memoryBlock[hpd.PAD_MEMINDEX + hpd.PAD_MEMSIZE * final_pad_index:hpd.PAD_MEMINDEX + hpd.PAD_MEMSIZE * (final_pad_index + 1)] = pad.memory_block
                self.memoryBlock[hpd.KIT_MEMINDEX + hpd.KIT_MEMSIZE * kit_index:hpd.KIT_MEMINDEX + hpd.KIT_MEMSIZE * (kit_index + 1)] = kit.memory_block
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
        for kit_index in range(hpd.KITS_COUNT):
            self.save_kit(kit_index, self.create_kit_filename(kit_index))

    def apply_pad(self, pad_index):
        pad = self.pads.get_pad(pad_index)
        self.memoryBlock[hpd.PAD_MEMINDEX + hpd.PAD_MEMSIZE * pad_index:hpd.PAD_MEMINDEX + hpd.PAD_MEMSIZE * (
                        pad_index + 1)] = pad.memory_block

    def apply_scale(self, layer, instrument_name, scale, mode, first_note, kit_index, pad_list):
        instruments = Scale.get_scale(instrument_name, first_note, len(pad_list), scale, mode)

        for i in range(len(pad_list)):
            final_pad_index = hpd.PADS_PER_KIT * kit_index + pad_list[i]
            instrument_number = instruments[i][0]
            instrument_pitch = instruments[i][1]
            pad = self.pads.get_pad(final_pad_index)
            pad.set_patch(layer, instrument_number)
            pad.set_pitch(layer, instrument_pitch)
            self.apply_pad(final_pad_index)


def usage(argv):
    print("Usage: " + argv[0] + "[OPTIONS] <backup-file> [COMMAND]")
    print("Version: " + version)
    print("OPTIONS: ")
    print("  -h,--help              Show this help")
    print("  -v,--verbose           Create verbose output")

    print("COMMANDS:")
    print("  show chains")
    print("  show kits")
    print("  show kit #")


def run_main():
    argv = list()
    for arg in sys.argv:
        argv.append(arg)
    verbose = 0
    if len(argv) < 2:
        usage(argv)
        sys.exit(2)
    arg_pos = 1

    while argv[arg_pos].startswith('-'):
        if argv[arg_pos].startswith('--'):
            option = argv[arg_pos][2:]
        else:
            option = argv[arg_pos]
        arg_pos += 1
        if option == 'verbose' or option == '-v':
            verbose += 1
        elif option == 'help' or option == '-h':
            usage(argv)
            sys.exit(2)
        else:
            print("unknown option --{0}".format(option))
            usage(argv)
            sys.exit(2)

    hpd_m = hpd(argv[arg_pos])
    arg_pos += 1
    result = ""
    while arg_pos < len(argv):
        operation = argv[arg_pos]
        arg_pos += 1
        if operation == 'show':
            showing = argv[arg_pos]
            arg_pos += 1
            if showing == 'kits':
                result += hpd_m.digest_kits()
            if showing == 'kit':
                result += hpd_m.digest_single_kit(int(argv[arg_pos]))
                arg_pos += 1

    if result is not None:
        sys.stdout.write(result)
    sys.stdout.write('\n')

if __name__ == "__main__":
    run_main()
