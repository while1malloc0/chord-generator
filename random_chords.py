#!/usr/bin/env python

from random import randint, seed
from sys import argv, exit
from datetime import datetime


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


if __name__ == "__main__":
    if len(argv) <= 1:
        print(usage)
        exit(0)

    seed(datetime.now())
    num_chords = int(argv[1])

    chords = []
    for i in range(0, num_chords):
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

    s = ""
    for i, chord in enumerate(chords):
        if i % 4 == 0 and s != "":
            s = "|" + s
            print(s)
            s = ""
        s += " {:<8} |".format(chord)
