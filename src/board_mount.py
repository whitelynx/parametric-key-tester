from solid import rotate, cube, hull, scad_render_to_file
from solid.utils import up, left, right, forward, back

from utils import cylinder_outer, optional


SEGMENTS = 48

FUDGE = 0.2

m2_head_radius = 5 / 2
m2_shaft_radius = 2 / 2
m2_nut_radius = 3.9 / 2


def mount_post_m2(height):
    return cylinder_outer(4, height) - cylinder_outer(m2_shaft_radius, height)


class BoardMount:
    def __init__(self, board_width, board_length, board_thickness, has_connector=True):
        self.board_width = board_width
        self.board_length = board_length
        self.board_thickness = board_thickness
        self.has_connector = has_connector

        # Distance from the front edge of the board to the front of the large portion of the plug
        self.plug_offset = 2

        # Length of the plug clearance volume
        self.plug_length = 20

    def pcb_only(self, distance_from_surface):
        return up(distance_from_surface + self.board_thickness / 2)(
            back(self.board_length / 2)(
                cube(
                    (self.board_width, self.board_length, self.board_thickness),
                    center=True,
                )
            )
        )

    def connector(self, distance_from_surface):
        return optional(self.has_connector)(
            up(distance_from_surface - 1.25)(
                forward(self.plug_offset)(
                    rotate((90, 0, 0))(
                        hull()(
                            left(4 - 1.25)(cylinder_outer(2.5 / 2, 6)),
                            right(4 - 1.25)(cylinder_outer(2.5 / 2, 6)),
                        )
                    )
                )
                + forward(self.plug_offset + self.plug_length)(
                    rotate((90, 0, 0))(
                        hull()(
                            left(4 - 1.25)(cylinder_outer(8.5 / 2, self.plug_length)),
                            right(4 - 1.25)(cylinder_outer(8.5 / 2, self.plug_length)),
                        )
                    )
                )
            )
        )

    def board_profile(self, distance_from_surface):
        return (
            self.pcb_only(distance_from_surface)
            + self.connector(distance_from_surface)
        )
        # TODO: Maybe add pin clearance!

    def mounting_posts(self, distance_from_surface):
        positioning_post_height = distance_from_surface + self.board_thickness + 3
        positioning_post = forward(1)(
            up(positioning_post_height / 2)(
                cube((4, 4, positioning_post_height), center=True)
            )
        )

        return (
            back(self.board_length + m2_shaft_radius + FUDGE)(
                mount_post_m2(distance_from_surface)
            )
            + left(7)(positioning_post)
            + right(7)(positioning_post)
        )

    def render(self, distance_from_surface):
        return self.mounting_posts(distance_from_surface) - self.board_profile(
            distance_from_surface
        )


pro_micro = BoardMount(18.3, 33.1, 1.7)


if __name__ == "__main__":
    scad_render_to_file(
        pro_micro.render(5) + up(20)(pro_micro.render(5) + pro_micro.board_profile(5)),
        file_header=f"$fn = {SEGMENTS};",
        include_orig_code=True,
    )
