#!/usr/bin/env python

from hashlib import blake2b
from random import randint, seed
from sys import argv, exit
from datetime import datetime
import argparse


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

usage = """
Usage: random_chords.py NUM_CHORDS

Args:
  NUM_CHORDS - How many chords to generate
"""


def next_note_cof():
    """picks the next note in the circle of fifths"""
    while True:
        for i in range(0, len(notes)):
            yield i


def next_note_rand():
    """picks the next note at random"""
    while True:
        yield randint(0, len(notes) - 1)


parser = argparse.ArgumentParser(
    description="Generate random chords for practice purposes"
)

parser.add_argument(
    "num_chords",
    metavar="N",
    type=int,
    help="The number of chords to generate",
)

# TODO [jturner 2021-06-17]: This should probably take an interval so that you
# can do things like have chords that move in thirds
parser.add_argument(
    "--order",
    default="random",
    choices=["random", "cof"],
    help="The order in which to enumerate chords. One of random or cof (Circle of Fifths)",
)

parser.add_argument(
    "--qualities",
    dest="qualities",
    action="extend",
    nargs="+",
)


if __name__ == "__main__":
    args = parser.parse_args()

    seed(datetime.now())

    # get our iterator for picking the next note, default to random
    get_next_note_picker = next_note_rand
    if args.order == "cof":
        get_next_note_picker = next_note_cof
    next_note_picker = get_next_note_picker()

    # get the chord qualities that we're allowed to choose from, default to all
    available_qualities = args.qualities
    if not available_qualities:
        available_qualities = ["min", "maj", "dim7", "7", "min7b5"]

    # assemble a list of N chords, which are note + quality + extensions,
    # e.g. A + min + 6/9 = Amin6/9
    chords = []
    for i in range(0, args.num_chords):
        which_quality = randint(0, len(available_qualities) - 1)
        quality = available_qualities[which_quality]

        possible_extensions = qualities_with_extensions[quality]
        extension = ""
        if possible_extensions:
            which_extension = randint(0, len(possible_extensions) - 1)
            extension = possible_extensions[which_extension]

        which_note = next(next_note_picker)
        note = notes[which_note]

        chord = f"{note}{quality}{extension}"
        chords.append(chord)

    # Pretty print the chords
    # TODO [jturner 2021-06-17]: use a real table writer for this
    s = ""
    for i, chord in enumerate(chords):
        if i % 4 == 0 and s != "":
            print("|" + s)
            s = ""
        s += " {:<8} |".format(chord)
    print("|" + s)
