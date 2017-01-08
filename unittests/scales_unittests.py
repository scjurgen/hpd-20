
import unittest

from hpd20.scales import Scale


class ScalesTest(unittest.TestCase):

    def test_scaleHeight(self):
        note_height = Scale.get_height_of_note("C4")
        self.assertEqual(note_height, 60, "Scale height is {0}".format(note_height))
        note_height = Scale.get_height_of_note("C3")
        self.assertEqual(note_height, 48, "Scale height is {0}".format(note_height))

    def test_rootNotesList(self):
        self.assertEqual(Scale.get_root_notes()[0], "C2")
        self.assertEqual(len(Scale.get_root_notes()) % 12, 1)  # from C-C thus 12*n+1

    def test_scaleGeneration(self):
        scale = Scale.get_scale("Balaphone", 60, 5, "major", Scale.IONIAN)
        # check 3rd note is pitch E
        self.assertEqual(-800, scale[2][1])
        scale = Scale.get_scale("Balaphone", 60, 5, "minor", Scale.IONIAN)
        # check 3rd note is now pitch Eb
        self.assertEqual(-900, scale[2][1])

    def test_noteNaming(self):
        self.assertEqual("C4", Scale.get_note_name(60))

if __name__ == '__main__':
    unittest.main()
