#!/usr/bin/env python

from table_printer import TablePrinter
from chord_generator import ChordGenerator, next_note_cof, next_note_rand
from random import randint, seed
from datetime import datetime
import argparse


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

parser.add_argument("--no-extensions", type=bool, nargs="?", default=argparse.SUPPRESS)


if __name__ == "__main__":
    args = parser.parse_args()

    # get our iterator for picking the next note, default to random
    next_note_picker = next_note_rand
    if args.order == "cof":
        next_note_picker = next_note_cof

    # get the chord qualities that we're allowed to choose from, default to all
    available_qualities = args.qualities
    if not available_qualities:
        available_qualities = ["min", "maj", "dim7", "7", "min7b5"]

    # set whether or not we're allowed to add extensions
    # TODO [jturner 2021-06-17]: this should really be a list of extensions that
    # are allowed, as with qualities
    extensions_allowed = not hasattr(args, "no_extensions")

    chord_gen = ChordGenerator(
        next_note_picker, extensions_allowed, available_qualities
    )

    # assemble a list of N chords, which are note + quality + extensions,
    # e.g. A + min + 6/9 = Amin6/9
    chords = []
    for i in range(0, args.num_chords):
        chords.append(chord_gen.get_chord())

    printer = TablePrinter(chords)
    content = printer.print()
    print(content)
