#!/usr/bin/env python

from random import randint, seed
from sys import argv, exit
from datetime import datetime
import argparse


notes = [
    "Ab",
    "A",
    "A#",
    "Bb",
    "B",
    "C",
    "C#",
    "Db",
    "D",
    "D#",
    "Eb",
    "E",
    "F",
    "F#",
    "Gb",
    "G",
    "G#",
]


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

usage = """
Usage: random_chords.py NUM_CHORDS

Args:
  NUM_CHORDS - How many chords to generate
"""

parser = argparse.ArgumentParser(
    description="Generate random chords for practice purposes"
)

parser.add_argument(
    "num_chords",
    metavar="N",
    type=int,
    help="The number of chords to generate",
)


if __name__ == "__main__":
    args = parser.parse_args()

    seed(datetime.now())

    chords = []
    for i in range(0, args.num_chords):
        quality_index = randint(0, len(qualities_with_extensions) - 1)
        quality = list(qualities_with_extensions.keys())[quality_index]
        possible_extensions = qualities_with_extensions[quality]
        extension = ""
        if possible_extensions:
            extension_index = randint(0, len(possible_extensions) - 1)
            extension = possible_extensions[extension_index]
        note = notes[randint(0, len(notes) - 1)]
        chord = f"{note}{quality}{extension}"
        chords.append(chord)

    # TODO [jturner 2021-06-17]: use a real table writer for this
    s = ""
    for i, chord in enumerate(chords):
        if i % 4 == 0 and s != "":
            print("|" + s)
            s = ""
        s += " {:<8} |".format(chord)
    print("|" + s)
