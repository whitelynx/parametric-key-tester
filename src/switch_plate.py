from solid import cube, mirror, scad_render_to_file
from solid.utils import up, down, left, forward, back


SEGMENTS = 48

keyswitch_length = 14.0
keyswitch_width = 14.0
keyswitch_depth = 5.08  # From the base of the switch to the mounting plate face

plate_thickness = 3
notch_plate_thickness = 1.3  # The thickness of the plate at the notches where the switch's clips are located
notch_width = 5
notch_depth = 0.5
backplate_thickness = 1.25
backplate_orientation = 180
mount_width = keyswitch_width + 3
mount_length = keyswitch_length + 3


def switch_plate():
    top_wall = forward((1.5 + keyswitch_length) / 2)(
        up(plate_thickness / 2)(
            cube((keyswitch_width + 3, 1.5, plate_thickness), center=True)
            - down(notch_plate_thickness)(  # Notch for switch clips
                back(0.75)(
                    cube((notch_width, notch_depth * 2, plate_thickness), center=True)
                )
            )
        )
    )

    left_wall = left((1.5 + keyswitch_width) / 2)(
        up(plate_thickness / 2)(
            cube((1.5, keyswitch_length + 3, plate_thickness), center=True)
        )
    )

    plate_half = top_wall + left_wall

    return plate_half + mirror((0, 1, 0))(mirror((1, 0, 0))(plate_half))


if __name__ == "__main__":
    scad_render_to_file(
        switch_plate(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
    )
