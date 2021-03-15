#!/usr/bin/env python
import argparse
from os.path import abspath, dirname, join

from solid import *

from key_grid_tester import key_grid_tester, default_wall_height


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
        "--height",
        metavar="MM",
        type=float,
        default=default_wall_height,
        help="the height of the walls of the tester",
    )
    parser.add_argument(
        "--margin-length",
        metavar="MM",
        type=float,
        default=0,
        help="an extra margin along the length axis to add inside the walls",
    )
    parser.add_argument(
        "--margin-width",
        metavar="MM",
        type=float,
        default=0,
        help="an extra margin along the width axis to add inside the walls",
    )
    parser.add_argument(
        "--function-row",
        action="store_true",
        help="special mode to make a function row to fit next to another keyboard",
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
        key_grid_tester(
            args.length,
            args.width,
            wall_height=args.height,
            margin_length=args.margin_length,
            margin_width=args.margin_width,
            function_row=args.function_row
        ),
        filepath=filepath,
        include_orig_code=True,
    )
