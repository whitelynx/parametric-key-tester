#!/usr/bin/env python
import argparse
from os.path import abspath, dirname, join

from solid import cube, rotate, scad_render_to_file
from solid.utils import up, down, left, right, forward

from board_mount import pro_micro
from key_grid_tester import (
    default_wall_height,
    key_grid_tester,
    key_grid_tester_wall_dimensions,
    switch_spacing,
    wall_thickness,
)
from switch_plate import (
    mount_width,
    mount_length,
)


def function_row(
    width_units,
    wall_height=default_wall_height,
    margin_length=0,
    margin_width=0
):
    x_grid_size = mount_width + switch_spacing
    y_grid_size = mount_length + switch_spacing

    case = key_grid_tester(
        1,
        width_units,
        wall_height=wall_height,
        margin_length=margin_length,
        margin_width=margin_width,
    )

    wall_length, wall_width = key_grid_tester_wall_dimensions(
        1, width_units, wall_height, margin_length, margin_width
    )

    board_left = wall_width / 2 - 70
    board_up = 10
    board_forward = wall_length / 2 - wall_thickness

    def position_board(part):
        if 1 == 1:
            return left(board_left)(down(1)(rotate((0, 0, 90))(part)))

        return left(board_left)(
            up(board_up)(forward(board_forward)(rotate((0, -90, 90))(part)))
        )

    full_case = (
        case
        - left(wall_width / 2 - 20)(
            cube((15, 1 * y_grid_size * 2, 23 * 2), center=True)
        )
        - position_board(pro_micro.board_profile(3))
    )

    big_block = cube((200, 200, 200), center=True)
    return (
        full_case - right(100 - (x_grid_size / 2 if width_units % 2 else 0))(big_block),
        full_case - left(100 + (x_grid_size / 2 if width_units % 2 else 0))(big_block),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "width",
        metavar="WIDTH",
        type=int,
        help="the width of the function row, in number of keys",
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
        "-o",
        "--output",
        metavar="FILE",
        type=str,
        default=None,
        help="the name of the file to write to",
    )

    args = parser.parse_args()

    def build_filepath(side):
        return join(
            dirname(dirname(abspath(__file__))),
            "files",
            args.output or f"function_row_{args.width}_{side}.scad",
        )

    left_filepath = build_filepath('left')
    right_filepath = build_filepath('right')

    print(f"Building {args.width}-key function row frame . . .")

    left_side, right_side = function_row(
        args.width,
        wall_height=args.height,
        margin_length=args.margin_length,
        margin_width=args.margin_width,
    )

    print(f"Writing left side to {left_filepath} . . .")
    scad_render_to_file(
        left_side,
        filepath=left_filepath,
        include_orig_code=True,
    )

    print(f"Writing right side to {right_filepath} . . .")
    scad_render_to_file(
        right_side,
        filepath=right_filepath,
        include_orig_code=True,
    )
