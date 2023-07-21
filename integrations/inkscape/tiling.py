#!/usr/bin/env python
"""
This extension allows you to create tiling patterns.
"""

import sys
import os
import inkex
from lxml import etree

# Default: look in current directory for embedded Tessagon
TESSAGON_DIRECTORY = os.environ.get('TESSAGON_DIRECTORY',
                                    'tessagon')
sys.path.append(TESSAGON_DIRECTORY)

from tessagon.adaptors.svg_adaptor import SvgAdaptor  # noqa E402
from tessagon import TessagonDiscovery  # noqa E402


class Tiling(inkex.EffectExtension):
    # Nice blues ...
    DEFAULT_COLORS = [0xD7E3F4FF,
                      0xAFC6E9FF,
                      0x87AADEFF,
                      0x5F8DD3FF,
                      0x3771C8FF,
                      0x2C5AA0FF,
                      0x214478FF,
                      0x162D50FF]

    TOLERANCE = 0.0000001

    def add_arguments(self, pars):
        pars.add_argument("--tab")
        pars.add_argument("--class_name", default="HexTessagon",
                          help="Which pattern to use:")
        pars.add_argument("--x_num", type=int, default=4,
                          help="Number of tiles in the X direction")
        pars.add_argument("--y_num", type=int, default=4,
                          help="Number of tiles in the Y direction")
        pars.add_argument("--x_min", type=float, default=50,
                          help="Lower X bounding box")
        pars.add_argument("--x_max", type=float, default=150,
                          help="Upper X bounding box")
        pars.add_argument("--y_min", type=float, default=50,
                          help="Lower Y bounding box")
        pars.add_argument("--y_max", type=float, default=150,
                          help="Upper Y bounding box")

        pars.add_argument("--stroke_type_unit", default="px",
                          help="Stroke type (none or unit)")
        pars.add_argument("--stroke_width", type=float, default=1.0,
                          help="Stroke width")
        pars.add_argument("--stroke_color", type=inkex.Color,
                          default=inkex.Color(0x000000FF),
                          help="Stroke color")

        pars.add_argument("--fill_type", default="None",
                          help="Now to handle fill colors")
        pars.add_argument("--color_pattern", type=int, default=1,
                          help="Which color pattern to use")

        for i in range(1, 9):
            pars.add_argument("--color_{}".format(i), type=inkex.Color,
                              default=inkex.Color(self.DEFAULT_COLORS[i - 1]),
                              help="Color {}".format(i))

        pars.add_argument("--uv_random_vert_offset_radius",
                          type=float, default=0.0,
                          help="Random vertex offset radius")
        pars.add_argument("--uv_random_face_offset_radius",
                          type=float, default=0.0,
                          help="Random face offset radius")
        pars.add_argument("--uv_rotate_faces_degrees",
                          type=float, default=0.0,
                          help="Rotate polygons (degrees)")
        pars.add_argument("--uv_rotate_faces_random_degrees",
                          type=float, default=0.0,
                          help="Rotate polygons randomly (max degrees)")
        pars.add_argument("--uv_scale_faces",
                          type=float, default=1.0,
                          help="Scale polygons (1.0 is no scaling)")
        pars.add_argument("--uv_scale_faces_random_min",
                          type=float, default=1.0,
                          help="Random scale polygons minimum "
                          "(1.0 is no scaling)")
        pars.add_argument("--uv_scale_faces_random_max",
                          type=float, default=1.0,
                          help="Random scale polygons maximum "
                          "(1.0 is no scaling)")

    def effect(self):
        layer = self.svg.get_current_layer()
        group = self.draw_tessagon_group(self.options)
        if group is not None:
            layer.add(group)

    def validate_options(self, tessagon_class):
        options = self.options

        num_color_patterns = tessagon_class.metadata.num_color_patterns
        if options.fill_type == "pattern":
            if options.color_pattern > num_color_patterns:
                inkex.errormsg(
                    "This tiling only has {} color patterns"
                    "(color pattern {} specified).\n".
                    format(num_color_patterns,
                           options.color_pattern)
                )  # signal an error
                return False

        if self.options.x_max <= self.options.x_min:
            inkex.errormsg("Lower bounding box extent must be "
                           "less than upper bound box (X)")
            return False

        if self.options.y_max <= self.options.y_min:
            inkex.errormsg("Lower bounding box extent must be "
                           "less than upper bound box (Y)")
            return False

        if self.options.uv_scale_faces_random_max < \
           self.options.uv_scale_faces_random_min:
            inkex.errormsg("Minimum of random scale range must be "
                           "less than maximum")
            return False

        return True

    def draw_tessagon_group(self, options):
        tessagon_class = TessagonDiscovery.get_class(options.class_name)
        if not self.validate_options(tessagon_class):
            return None

        multiplier = self.bb_multiplier(tessagon_class)
        kwargs = dict(simple_2d=True,
                      multiplier_2d=multiplier,
                      translate_2d=[options.x_min,
                                    options.y_min],
                      u_num=options.x_num,
                      v_num=options.y_num,
                      u_range=[0, 1],
                      v_range=[0, 1],
                      u_cyclic=False,
                      v_cyclic=False,
                      adaptor_class=SvgAdaptor)

        if options.fill_type == "pattern":
            kwargs['color_pattern'] = options.color_pattern
            kwargs["svg_fill_colors"] = self.options_to_colors()
        elif options.fill_type == "color":
            kwargs["svg_fill_color"] = str(options.color_1)
        elif options.fill_type == "none":
            kwargs["svg_fill_color"] = "none"

        if options.stroke_type_unit == "none":
            kwargs['svg_stroke_color'] = "none"
        else:
            kwargs['svg_stroke_color'] = str(options.stroke_color)
            kwargs['svg_stroke_width'] = \
                "{}{}".format(options.stroke_width, options.stroke_type_unit)

        if options.uv_random_vert_offset_radius > self.TOLERANCE:
            kwargs['uv_random_vert_offset_radius'] = \
                options.uv_random_vert_offset_radius
        if options.uv_random_face_offset_radius > self.TOLERANCE:
            kwargs['uv_random_face_offset_radius'] = \
                options.uv_random_face_offset_radius
        if abs(options.uv_rotate_faces_degrees) > self.TOLERANCE:
            kwargs['uv_rotate_faces_degrees'] = options.uv_rotate_faces_degrees
        if abs(options.uv_rotate_faces_random_degrees) > self.TOLERANCE:
            kwargs['uv_rotate_faces_random_degrees'] = \
                options.uv_rotate_faces_random_degrees
        if abs(1.0 - options.uv_scale_faces) > self.TOLERANCE:
            kwargs['uv_scale_faces'] = options.uv_scale_faces
        if abs(1.0 - options.uv_scale_faces_random_min) > self.TOLERANCE or \
           abs(1.0 - options.uv_scale_faces_random_max) > self.TOLERANCE:
            kwargs['uv_scale_faces_random_range'] = \
                [options.uv_scale_faces_random_min,
                 options.uv_scale_faces_random_max]

        this_tessagon = tessagon_class(**kwargs)
        svg = this_tessagon.create_mesh()
        group = etree.fromstring(svg)

        return group

    def options_to_colors(self):
        return [str(getattr(self.options, "color_{}".format(i)))
                for i in range(1, 9)]

    def bb_multiplier(self, tessagon_class):
        xy_ratio = tessagon_class.metadata.uv_ratio

        x_span = self.options.x_max - self.options.x_min
        y_span = self.options.y_max - self.options.y_min
        tile_aspect = self.options.y_num / self.options.x_num

        y_prime = x_span * tile_aspect / xy_ratio
        y_factor = y_prime / y_span

        # If won't fit in the y direction, scale back
        if y_factor > 1.0:
            return x_span / y_factor

        return x_span


if __name__ == "__main__":
    Tiling().run()
