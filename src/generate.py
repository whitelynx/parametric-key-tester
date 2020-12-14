#!/usr/bin/env python
import argparse
from os.path import abspath, dirname, join

from solid import *

from key_grid_tester import key_grid_tester


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "length",
        metavar="LENGTH",
        type=int,
        help="the length of the tester, in number of keys",
    )
    parser.add_argument(
        "width",
        metavar="WIDTH",
        type=int,
        help="the width of the tester, in number of keys",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        type=str,
        default=None,
        help="the name of the file to write to",
    )

    args = parser.parse_args()

    filepath = join(
        dirname(dirname(abspath(__file__))),
        "files",
        args.output or f"key_grid_tester_{args.length}x{args.width}.scad",
    )

    print(f"Writing {args.length}x{args.width} key tester frame to {filepath} . . .")

    scad_render_to_file(
        key_grid_tester(args.length, args.width),
        filepath=filepath,
        include_orig_code=True,
    )
