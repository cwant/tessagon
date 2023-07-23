import os
import sys

# This script runs with the Inkscape Simple Scripting extension.

# Replace with your tessagon source directory if you like.
demo_directory = os.path.dirname(extension.options.py_source)
tessagon_directory = os.path.realpath(demo_directory + '/..')
sys.path.append(tessagon_directory)

import tessagon
from tessagon.adaptors.list_adaptor import ListAdaptor
from tessagon import TessagonDiscovery

LIGHT_GREYS = ['#eeeeee', '#dddddd', '#cccccc']

class InkscapeSimpleDemo:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.swatch_width = 40
        self.swatch_height = 40

    def main(self):
        tessagon_classes = TessagonDiscovery().to_list()

        for tessagon_class in tessagon_classes:
            g = self.make_tessagon(tessagon_class)
            self.update_position()

    def bounding_box(self):
        x_min = self.x * (self.swatch_width - 10) + 10
        y_min = self.y * (self.swatch_height) + 10
        return [[x_min, x_min + self.swatch_width],
                [y_min, y_min + self.swatch_height]]

    def update_position(self):
        self.x += 1
        if self.x > 5:
            self.x = 0
            self.y += 1

    def make_grid(self, tessagon):
        u_num = tessagon.u_num
        v_num = tessagon.v_num
        delta_u = 1/u_num
        delta_v = 1/v_num
        g = group()
        for i in range(1, u_num):
            l = line(tessagon.f(i*delta_u, delta_v),
                     tessagon.f(i*delta_u, 1-delta_v),
                     stroke_width=0.3,
                     stroke='#404040',
                     stroke_dasharray='1')
            g.append(l)

        for i in range(1, v_num):
            l = line(tessagon.f(delta_u, i*delta_v),
                     tessagon.f(1-delta_u, i*delta_v),
                     stroke_width=0.3,
                     stroke='#404040',
                     stroke_dasharray='1')
            g.append(l)

    def num_tiles(self, tessagon_class):
        u_num = 4
        v_num = 4
        uv_ratio = tessagon_class.metadata.uv_ratio

        ratio = u_num * uv_ratio / v_num
        if ratio > 1:
            while (ratio > 1):
                v_num += 1
                ratio = u_num * uv_ratio / v_num
            v_num -= 1
        elif ratio < 1:
            while (ratio < 1):
                u_num += 1
                ratio = u_num * uv_ratio / v_num
            u_num -= 1

        return (u_num, v_num)

    def make_tessagon(self, tessagon_class, **kwargs):
        (u_num, v_num) = self.num_tiles(tessagon_class)

        bounding_box = self.bounding_box()
        options = {
            'simple_2d': True,
            'bounding_box_2d': bounding_box,
            'center_bounding_box_2d': True,
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': u_num,
            'v_num': v_num,
            'u_cyclic': False,
            'v_cyclic': False,
            'color_pattern': 1,
            'adaptor_class' : ListAdaptor
        }
        tessagon = tessagon_class(**options)

        cp = clip_path(rect(tessagon.f(1/u_num, 1/v_num),
                            tessagon.f((u_num-1)/u_num, (v_num-1)/v_num)))

        g = self.render_tessagon(tessagon, colors=LIGHT_GREYS, clip_path=cp)

        self.make_grid(tessagon)

        text_x = (bounding_box[0][0] + bounding_box[0][1]) / 2
        text_y = bounding_box[1][0] + 5
        text(tessagon_class.__name__, (text_x, text_y),
             font_size='1.5pt', text_anchor='middle')

    def render_tessagon(self, tessagon, colors=None, clip_path=None):
        corners = tessagon.corners

        y_min = tessagon.f(*corners[0])[1]
        y_max = tessagon.f(*corners[3])[1]

        out = tessagon.create_mesh()
        g = group(clip_path=clip_path)
        for f in range(len(out['face_list'])):
            face = out['face_list'][f]
            verts = []
            for v in face:
                vert = out['vert_list'][v]
                # Flip because inkscape y is down
                verts.append((vert[0], y_max - vert[1] + y_min))

            if colors:
                if type(colors) == list:
                    color = colors[out['color_list'][f]]
                else:
                    color = colors
                p = polygon(verts,
                            stroke='#888888',
                            stroke_width=1*pt,
                            fill=color).to_path(True)
            else:
                p = polygon(verts,
                            stroke='#b0b0b0',
                            stroke_width=0.3*pt).to_path(True)
            g.append(p)
        return g

InkscapeSimpleDemo().main()
