from math import asin, sqrt, sin, cos, pi, tan
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import right_tile, left_tile, \
    top_tile, top_left_tile, bottom_tile, bottom_left_tile, \
    top_right_tile, bottom_right_tile

# From: https://gallica.bnf.fr/ark:/12148/btv1b105092395/f11.item
# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/hokusai_parallelograms.svg

# TODO: how to share this value with the tessagon?
default_triangle_ratio = (asin(sqrt(3)/sqrt(7)) - pi/6) / (pi/6)


class HokusaiParallelogramsTile(Tile):
    uv_ratio = 1.0 / sqrt(3)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

        self.triangle_ratio = kwargs.get('triangle_ratio',
                                         default_triangle_ratio)
        self.theta_offset = pi/6 + self.triangle_ratio * pi/6

        # in u units
        self.hex_radius = self.get_hex_radius()

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


class HokusaiParallelogramsTile1(HokusaiParallelogramsTile):
    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None}

    def calculate_verts(self):
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

    def calculate_faces(self):
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

    def color_pattern1(self):
        pass

    def color_pattern2(self):
        color = ((self.fingerprint[0] // 2 + self.fingerprint[1] % 2)) % 3

        self.color_face('A', (color + self.fingerprint[1] % 2) % 3)
        self.color_face('B', (color + self.fingerprint[1] % 2) % 3)

    def color_pattern3(self):
        self.color_face('A', 0)
        self.color_face('B', 1)


class HokusaiParallelogramsTile2(HokusaiParallelogramsTile):
    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None,
                8: None,
                9: None}

    def init_faces(self):
        return {'C': None,
                'D': None,
                'E': None}

    def calculate_verts(self):
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
        self.color_face('C', 1)
        self.color_face('E', 1)

    def color_pattern2(self):
        self.color_face('C', 3)
        self.color_face('E', 3)

        color = ((self.fingerprint[0] // 2 + self.fingerprint[1] % 2)) % 3
        self.color_face('D', color)

    def color_pattern3(self):
        self.color_face('C', 3)
        self.color_face('E', 3)
        self.color_face('D', 2)
