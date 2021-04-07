#!/usr/bin/env python
import argparse
from os.path import abspath, dirname, join

from solid import cube, cylinder, rotate, scad_render_to_file
from solid.utils import up, down, left, right, forward, back

from board_mount import BoardMount, pro_micro, m2_shaft_radius
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
from utils import cylinder_outer


distribution_board = BoardMount(18.3, 30, 1.7, has_connector=False)


def control_box(wall_length, wall_width, wall_height):
    max_board_thickness = max(pro_micro.board_thickness, distribution_board.board_thickness)

    board_surface_pos = max(20 + wall_thickness - wall_length, 5)

    case_length = (
        board_surface_pos
        + max_board_thickness
        + 3
        + wall_thickness
    )
    case_width = (
        pro_micro.board_length + distribution_board.board_length + 3 * wall_thickness
    )

    board_offset_forward = (
        board_surface_pos
        + max_board_thickness
        - case_length / 2
    )

    def position_control_box(part):
        """Position the control box on the final model."""
        #return left(case_width / 2)(
        return left(wall_width / 4 - case_width / 2)(
            forward((wall_length + case_length) / 2)(
                up(wall_height / 2)(part)
            )
        )

    def position_controller(part):
        """Position the controller board within the control box."""
        return forward(board_offset_forward)(
            left(case_width / 2 - wall_thickness + wall_thickness / 4)(
                rotate((90, -90, 0))(
                    part
                )
            )
        )

    def position_distribution_board(part):
        """Position the distribution board within the control box."""
        return forward(board_offset_forward)(
            right(case_width / 2 - wall_thickness + wall_thickness / 4)(
                rotate((90, 90, 0))(
                    part
                )
            )
        )

    center_post_length = max_board_thickness + 3
    center_post_offset_right = (
        case_width / 2
        - wall_thickness * 1.5
        - distribution_board.board_length
    )

    inner = (
        down(wall_thickness / 2 + 1)(
            back(wall_thickness + 1)(
                cube(
                    (
                        case_width - 2 * wall_thickness,
                        case_length + 2,
                        wall_height - wall_thickness + 1,
                    ),
                    center=True,
                )
            )
        )
        + rotate((90, 0, 0))(
            right(center_post_offset_right)(
                cylinder_outer(4.5, 100)
            )
        )
    )

    case = position_control_box(
        cube((case_width, case_length, wall_height), center=True)
        - inner
        # Center post (between the two boards):
        + forward(board_surface_pos - case_length / 2 + center_post_length / 2)(
            right(center_post_offset_right)(
                cube((wall_thickness * 2, center_post_length, wall_height), center=True)
                - rotate((90, 0, 0))(
                    cylinder_outer(m2_shaft_radius, center_post_length)
                )
            )
        )
        - position_controller(pro_micro.board_profile(0))
        - position_distribution_board(distribution_board.board_profile(0))
    )

    cutout = position_control_box(inner)

    return (case, cutout)


def function_row(
    width_units, wall_height=default_wall_height, margin_length=0, margin_width=0
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

    control_box_case, control_box_cutout = control_box(
        wall_length, wall_width, wall_height
    )

    split_offset = x_grid_size / 2 if width_units % 2 else 0

    def position_mounting_points(part):
        x_offset = wall_width / 2 - wall_thickness
        y_offset = wall_length / 2 - wall_thickness
        return (
            left(x_offset)(forward(y_offset)(part))
            + right(x_offset)(forward(y_offset)(part))
            + left(x_offset)(back(y_offset)(part))
            + right(x_offset)(back(y_offset)(part))
            + right(split_offset - wall_thickness)(forward(y_offset)(part))
            + right(split_offset + wall_thickness)(forward(y_offset)(part))
            + right(split_offset - wall_thickness)(back(y_offset)(part))
            + right(split_offset + wall_thickness)(back(y_offset)(part))
        )

    full_case = (
        case
        - control_box_cutout
        + control_box_case
        - left(wall_width / 2 - 20)(
            cube((15, 1 * y_grid_size * 2, 23 * 2), center=True)
        )
        #- position_board(pro_micro.board_profile(3))
        + position_mounting_points(cylinder(r1=wall_thickness, r2=0, h=15, segments=16))
        - position_mounting_points(down(2)(cylinder_outer(m2_shaft_radius, 10)))
    )

    big_block = cube((200, 200, 200), center=True)

    alignment_tab = cube((wall_thickness, wall_thickness / 2, wall_height - wall_thickness), center=True)
    alignment_tabs = right(split_offset)(
        up((wall_height - wall_thickness) / 2)(
            forward(wall_length / 2 - wall_thickness)(alignment_tab)
            + back(wall_length / 2 - wall_thickness)(alignment_tab)
        )
    )

    return (
        (
            full_case
            - right(100 + split_offset)(big_block)
            + alignment_tabs
        ),
        (
            full_case
            - left(100 - split_offset)(big_block)
            - alignment_tabs
        ),
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

    left_filepath = build_filepath("left")
    right_filepath = build_filepath("right")

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
