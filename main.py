#!/usr/bin/env python

from table_printer import TablePrinter
from chord_generator import ChordGenerator
import click


@click.group()
def cli():
    pass


@cli.command()
# TODO [jturner 2021-06-17]: This should probably take an interval so that you
# can do things like have chords that move in thirds
@click.option(
    "--order",
    help="The order in which to enumerate chords. One of random or cof (Circle of Fifths)",
    show_choices=True,
    default="random",
    type=click.Choice(
        ["random", "cof"],
    ),
)
@click.option(
    "--qualities",
    type=str,
    callback=(
        lambda _ctx, _param, value: [s.strip() for s in value.split(",")]
        if value
        else []
    ),
    help="A comma-separated list of chord qualities to include",
)
@click.option("--no-extensions", is_flag=True, default=False)
@click.argument("N", nargs=1, type=int)
def gen_chords(order, qualities, no_extensions, n):
    # get the chord qualities that we're allowed to choose from, default to all
    available_qualities = qualities
    if not available_qualities:
        available_qualities = ["min", "maj", "dim7", "7", "min7b5"]

    # set whether or not we're allowed to add extensions
    # TODO [jturner 2021-06-17]: this should really be a list of extensions that
    # are allowed, as with qualities
    extensions_allowed = not no_extensions

    chord_generator = ChordGenerator(order, extensions_allowed, available_qualities)

    # assemble a list of N chords, which are note + quality + extensions,
    # e.g. A + min + 6/9 = Amin6/9
    chords = []
    for i in range(0, n):
        chords.append(chord_generator.get_chord())

    printer = TablePrinter(chords)
    content = printer.print()
    print(content)


if __name__ == "__main__":
    cli()
