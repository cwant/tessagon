from math import asin, sqrt, sin, cos, pi, tan
from tessagon.core.tessagon import Tessagon
from tessagon.core.alternating_tile import AlternatingTile
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import right_tile, left_tile, \
    top_tile, top_left_tile, bottom_tile, bottom_left_tile, \
    top_right_tile, bottom_right_tile

# The default makes pattern fit on grid of regular triangles
# Solve triangle a = sqrt(7), b = 2, c = 3, angle A = pi/3
# Use sin law gives B = asin(sqrt(3)/sqrt(7))
# The rest comes from inverting theta_offset definition below
default_triangle_ratio = (asin(sqrt(3)/sqrt(7)) - pi/6) / (pi/6)

metadata = TessagonMetadata(name='Hokusai Parallelograms and Triangles',
                            num_color_patterns=3,
                            classification='non_edge',
                            shapes=['parallelograms', 'triangles'],
                            sides=[6, 3],
                            uv_ratio=1.0/sqrt(3),
                            extra_parameters={
                                'triangle_ratio': {
                                    'type': 'float',
                                    'min': 0.0,
                                    'max': 1.0,
                                    'default': default_triangle_ratio,
                                    'description':
                                    'Control the size of the triangles'
                                }
                            })


class HokusaiParallelogramsTile(AlternatingTile):
    # From: https://gallica.bnf.fr/ark:/12148/btv1b105092395/f11.item
    # See the SVG for decomposition:
    # https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/hokusai_parallelograms.svg

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

        self.triangle_ratio = kwargs.get('triangle_ratio',
                                         default_triangle_ratio)
        self.theta_offset = pi/6 + self.triangle_ratio * pi/6

        # in u units
        self.hex_radius = self.get_hex_radius()
        # multiplier to get v units ...
        self.uv_ratio = self.tessagon.metadata.uv_ratio

        self.hex_theta = [(self.theta_offset + number * pi / 3.0)
                          for number in range(6)]

    def get_hex_radius(self):
        a = tan(self.theta_offset)
        b = tan(self.theta_offset + 2*pi / 3)
        # Find magnitude of the intersection of these lines:
        # y = a*x and y = b*(x-2)
        r = 2 * b * sqrt(1 + a**2) / (b - a)
        return r

    def hex_vert_coord(self, center, number):
        # number in range(6)
        return [center[0] +
                self.hex_radius * cos(self.hex_theta[number]),
                center[1] +
                self.hex_radius * sin(self.hex_theta[number]) * self.uv_ratio]

    def init_verts(self):
        if self.tile_type == 0:
            verts = {0: None,
                     1: None,
                     2: None,
                     3: None}
        else:
            verts = {4: None,
                     5: None,
                     6: None,
                     7: None,
                     8: None,
                     9: None}

        return verts

    def init_faces(self):
        if self.tile_type == 0:
            faces = {'A': None,
                     'B': None}
        else:
            faces = {'C': None,
                     'D': None,
                     'E': None}

        return faces

    def calculate_verts(self):
        if self.tile_type == 0:
            self.add_vert([0], 0, 0,
                          equivalent=[left_tile(4),
                                      bottom_tile(9),
                                      bottom_left_tile(3)])
            self.add_vert([1], *self.hex_vert_coord([0, 0], 0))
            self.add_vert([2], *self.hex_vert_coord([1, 1], 3))
            self.add_vert([3], 1, 1,
                          equivalent=[right_tile(9),
                                      top_tile(4),
                                      top_right_tile(0)])
        else:
            self.add_vert([4], 1, 0,
                          equivalent=[right_tile(0),
                                      bottom_tile(3),
                                      bottom_right_tile(9)])
            self.add_vert([5], *self.hex_vert_coord([1, 0], 2))
            self.add_vert([6], *self.hex_vert_coord([1, 0], 1))
            self.add_vert([7], *self.hex_vert_coord([0, 1], 4))
            self.add_vert([8], *self.hex_vert_coord([0, 1], 5))
            self.add_vert([9], 0, 1,
                          equivalent=[left_tile(3),
                                      top_tile(0),
                                      top_left_tile(4)])

    def calculate_faces(self):
        if self.tile_type == 0:
            self.add_face('A',
                          [0,
                           1,
                           right_tile(7),
                           3,
                           2,
                           left_tile(6)])

            self.add_face('B',
                          [1,
                           0,
                           bottom_tile(8),
                           bottom_right_tile(2),
                           right_tile(4),
                           right_tile(5)])

        else:
            self.add_face('C',
                          [5,
                           7,
                           left_tile(1)])

            self.add_face('D',
                          [4,
                           6,
                           8,
                           9,
                           7,
                           5])

            self.add_face('E',
                          [8,
                           6,
                           right_tile(2)])

    def color_pattern1(self):
        if self.tile_type == 0:
            return

        self.color_face('C', 1)
        self.color_face('E', 1)

    def color_pattern2(self):
        if self.tile_type == 1:
            self.color_face('C', 3)
            self.color_face('E', 3)

        color = ((self.fingerprint[0] // 2 + self.fingerprint[1] % 2)) % 3
        if self.tile_type == 0:
            self.color_face('A', (color + self.fingerprint[1] % 2) % 3)
            self.color_face('B', (color + self.fingerprint[1] % 2) % 3)
        else:
            self.color_face('D', color)

    def color_pattern3(self):
        if self.tile_type == 1:
            self.color_face('C', 3)
            self.color_face('E', 3)

        if self.tile_type == 0:
            self.color_face('A', 0)
            self.color_face('B', 1)
        else:
            self.color_face('D', 2)


class HokusaiParallelogramsTessagon(Tessagon):
    tile_class = HokusaiParallelogramsTile
    metadata = metadata
