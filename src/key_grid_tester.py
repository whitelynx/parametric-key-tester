from solid import *
from solid.utils import *

from switch_plate import (
    switch_plate,
    keyswitch_depth,
    plate_thickness,
    mount_width,
    mount_length,
)


switch_spacing = 4

wall_height = keyswitch_depth + 15
wall_length = mount_length + 2 * switch_spacing
wall_thickness = 3


def spaced_switch_plate():
    plate_spacer = up(plate_thickness / 2)(
        forward((max(mount_width, mount_length) + switch_spacing) / 2)(
            cube((wall_length, switch_spacing, plate_thickness), center=True)
        )
    )

    return (
        switch_plate()
        + plate_spacer
        + rotate(90)(plate_spacer)
        + rotate(180)(plate_spacer)
        + rotate(270)(plate_spacer)
    )


def key_grid_tester_walls(length_units, width_units):
    wall_length = (mount_length + switch_spacing) * length_units + switch_spacing
    wall_width = (mount_width + switch_spacing) * width_units + switch_spacing

    top_wall = forward((wall_width - wall_thickness) / 2)(
        cube((wall_width, wall_thickness, wall_height), center=True)
    )

    left_wall = left((wall_length - wall_thickness) / 2)(
        cube((wall_thickness, wall_length, wall_height), center=True)
    )

    return up(wall_height / 2)(
        top_wall + left_wall + rotate(180)(top_wall) + rotate(180)(left_wall)
    )


def key_grid_tester(length_units, width_units):
    x_grid_size = mount_width + switch_spacing
    y_grid_size = mount_length + switch_spacing

    return key_grid_tester_walls(length_units, width_units) + up(
        wall_height - plate_thickness
    )(
        right(x_grid_size * (width_units - 1) / 2)(
            back(y_grid_size * (length_units - 1) / 2)(
                *[
                    left(x_grid_size * x_units)(
                        forward(y_grid_size * y_units)(spaced_switch_plate())
                    )
                    for y_units in range(length_units)
                    for x_units in range(width_units)
                ]
            )
        )
    )
