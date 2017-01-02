import instrumentname

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
        "Glockenspiel": [428, 433]
    }

    scale_patterns = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 9, 10],
        "harmonic minor": [0, 2, 3, 5, 7, 9, 11],
        "pentatonic major": [0, 2, 4, 7, 9],
        "pentatonic minor": [0, 3, 5, 7, 10],
    }

    @staticmethod
    def get_nearest_note_and_pitch(first, last, ideal):
        best_pitch = ideal - instrumentname.get_instrument_pitch(first)
        best_index = first
        first += 1
        while first < last:
            delta = ideal- instrumentname.get_instrument_pitch(first)
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
            values = Scale.get_nearest_note_and_pitch(low, high, (first_note+h)*100)
            list.append(values)
        return list

print(Scale.get_scale("Steel Drum", 60, 12, "major", Scale.LYDIAN))
print(Scale.get_scale("Vibraphone", 60, 12, "major", Scale.LYDIAN))

