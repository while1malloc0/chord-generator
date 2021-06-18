from random import randint, seed
from datetime import datetime

# Lay these out in the circle of fifths so that that logic is easier
notes = ["C", "F", "Bb", "Eb", "Ab", "Db", "F#", "B", "E", "A", "D", "G"]

# TODO [jturner 2021-06-17]: this approach is kind of naive, but it works. For
# more interesting combinations, this would use something like a Markov chain
# so that you could express certain stacks of "second order" extensions (e.g. a
# sus4 with a 9) without having to do annoying filtering for each new extension
# (e.g. "we've added a sus4, so now 6, 9 and 13 are fine but the 'altered'
# extension aren't anymore")
qualities_with_extensions = {
    "maj": ["6", "7", "6/9", "7/9", "7#11", "7#5", "7/13"],
    "min": ["6", "7", "6/9", "7/9", "7/11"],
    "7": ["#11", "b5", "#5", "/9", "b9", "#9", "b13", "/13", "sus4", "sus2"],
    "min7b5": [],
    "dim7": [],
}


def next_note_cof():
    """picks the next note in the circle of fifths"""
    while True:
        for i in range(0, len(notes)):
            yield i


def next_note_rand():
    """picks the next note at random"""
    while True:
        yield randint(0, len(notes) - 1)


class ChordGenerator:
    def __init__(self, note_picker, allow_extensions, qualities):
        seed(datetime.now())
        self.note_picker = note_picker()
        self.allow_extensions = allow_extensions
        self.qualities = qualities

    def get_chord(self):
        which_quality = randint(0, len(self.qualities) - 1)
        quality = self.qualities[which_quality]

        extension = ""
        if self.allow_extensions:
            possible_extensions = qualities_with_extensions[quality]
            if possible_extensions:
                which_extension = randint(0, len(possible_extensions) - 1)
                extension = possible_extensions[which_extension]

        which_note = next(self.note_picker)
        note = notes[which_note]

        chord = f"{note}{quality}{extension}"
        return chord
