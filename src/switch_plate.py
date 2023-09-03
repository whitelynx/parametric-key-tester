from solid2 import cube, cylinder, mirror, rotate, up, down, left, right, forward, back, scad_render_to_file


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

cherry_backplate_clearance_distance = 3.5


def mx_plate():
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


def mx_backplate():
    return down(plate_thickness - keyswitch_depth - backplate_thickness / 2)(
        rotate(backplate_orientation, [0, 0, 1])(
            cube((keyswitch_width + 3, keyswitch_length + 3, backplate_thickness))
            - (
                cylinder(r=1.9939, h=backplate_thickness + 1, _fs=0.5)
                + right(5.08)(cylinder(r=0.8509, h=backplate_thickness + 1, _fs=0.5))
                + left(5.08)(cylinder(r=0.8509, h=backplate_thickness + 1, _fs=0.5))
                + left(3.81)(forward(2.54)(cylinder(r=1.5, h=backplate_thickness + 1, _fs=0.5)))
                + right(2.54)(forward(5.08)(cylinder(r=1.5, h=backplate_thickness + 1, _fs=0.5)))
                + right(1.27)(back(5.08)(cylinder(r=0.4953, h=backplate_thickness + 1, _fs=0.5)))
                + left(1.27)(back(5.08)(cylinder(r=0.4953, h=backplate_thickness + 1, _fs=0.5)))
                + right(3.81)(back(5.08)(cylinder(r=0.4953, h=backplate_thickness + 1, _fs=0.5)))
                + left(3.81)(back(5.08)(cylinder(r=0.4953, h=backplate_thickness + 1, _fs=0.5)))
            )
        )
    )


def mx_backplate_clearance():
    return back(-7.5 / 2)(
        up(plate_thickness - keyswitch_depth - backplate_thickness - cherry_backplate_clearance_distance / 2)(
            rotate(backplate_orientation, [0, 0, 1])(
                cube((16.5, 7.5, cherry_backplate_clearance_distance))
            )
        )
    )


def mx_plate_with_backplate():
    return mx_plate + mx_backplate


switch_plate = mx_plate


if __name__ == "__main__":
    scad_render_to_file(
        switch_plate(), file_header=f"$fn = {SEGMENTS};", include_orig_code=True
    )
