import instrumentname

# note names are C4 = 60 (midi spec)

# http://www.huygens-fokker.org/docs/scales.zip
# http://www.huygens-fokker.org/docs/scalesdir.txt
class Scale:
    IONIAN = 0
    DORIAN = 1
    PHRYGIAN = 2
    LYDIAN = 3
    MIXOLYDIAN = 4
    AEOLIAN = 5
    LOCRIAN = 6

    melodic_sets = {
        "Steel Drum": [348, 355],
        "Balaphone": [356, 359],
        "Slit Drum": [362, 366],
        "Gyilli": [367, 371],
        "Lithophone": [372, 376],
        "Khongwong": [377, 381],
        "Kalimba": [382, 386],
        "Santoor": [387, 395],
        "Hand Pan": [396, 403],
        "Tone Plate": [404, 408],
        "Vibraphone": [409, 417],
        "Marimba": [418, 427],
        "Glockenspiel": [428, 433],
        "Tublar Bells": [434, 435]    ## don't change, named as in Roland set
    }

    scale_patterns = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 9, 10],
        "harmonic minor": [0, 2, 3, 5, 7, 9, 11],
        "pentatonic major": [0, 2, 4, 7, 9],
        "pentatonic minor": [0, 3, 5, 7, 10],
        "pentatonic blues min + maj 3rd": [0, 3, 4, 5, 7, 10],
        "pentatonic blues min + b5": [0, 3, 5, 6, 7, 10],
        "pentatonic blues min + 3rd+b5": [0, 3, 4, 5, 6, 7, 10],
    }

    keys = [
        "C", "Db", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"
    ]

    @staticmethod
    def get_note_name(height):
        return Scale.keys[height % 12] + str(int(height / 12) - 1)

    @staticmethod
    def get_relative_note_name(height):
        return Scale.keys[height % 12]

    @staticmethod
    def get_root_notes():
        notes = []
        for i in range(2, 8):
            for k in Scale.keys:
                notes.append(str(k) + str(i))
        notes.append(str(k) + "9")
        return notes

    @staticmethod
    def get_height_of_note(note_as_string):
        try:
            val = Scale.get_root_notes().index(note_as_string)
            return val + 36
        except:
            return 0

    @staticmethod
    def get_scales():
        return Scale.scale_patterns.keys()

    @staticmethod
    def get_melodic_instruments():
        return Scale.melodic_sets.keys()

    @staticmethod
    def get_nearest_note_and_pitch(first, last, ideal):
        best_pitch = ideal - instrumentname.get_instrument_pitch(first)
        best_index = first
        first += 1
        while first < last:
            delta = ideal - instrumentname.get_instrument_pitch(first)
            if abs(delta) < abs(best_pitch):
                best_pitch = delta
                best_index = first
            first += 1
        return [best_index, best_pitch]

    @staticmethod
    def get_scale(instrument_name, first_note, note_count, scale_name, mode=IONIAN):
        note_pattern = Scale.scale_patterns[scale_name]
        low, high = Scale.melodic_sets[instrument_name]
        list = []
        for i in range(note_count):
            nh = i + mode
            h = note_pattern[nh % len(note_pattern)] + 12 * int(nh / len(note_pattern))
            values = Scale.get_nearest_note_and_pitch(low, high, (first_note + h) * 100)
            list.append(values)
        return list
