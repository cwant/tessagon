from math import asin, sqrt, sin, cos, pi, tan
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

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
    BOUNDARY = dict(
        top=['vert', 'face'],
        left=['face-1', 'split', 'face-2', 'split', 'face-3', 'vert'],
        bottom=['vert', 'face'],
        right=['face-1', 'split', 'face-2', 'split', 'face-3', 'vert']
    )

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0, 0,
                      left_boundary='vert')

        self.add_vert(1,
                      *self.hex_vert_coord([0, 0], 0))

        self.add_vert(2,
                      *self.hex_vert_coord([1, 1], 3))

        self.add_vert(3,
                      1, 1,
                      right_boundary='vert')

    def calculate_faces(self):
        self.add_face('A',
                      [0,
                       1,
                       right_boundary('face-3'),
                       3,
                       2,
                       left_boundary('face-3')])

        self.add_face('B',
                      [1,
                       0,
                       bottom_boundary('face')])

        self.add_face('C',
                      [1,
                       right_boundary('face-2')])

        self.add_face('D',
                      [2,
                       left_boundary('face-2')])

        self.add_face('E',
                      [2,
                       3,
                       top_boundary('face')])

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
    BOUNDARY = dict(
        top=['face', 'vert'],
        left=['vert', 'face-1', 'split', 'face-2', 'split', 'face-3'],
        bottom=['face', 'vert'],
        right=['vert', 'face-1', 'split', 'face-2', 'split', 'face-3']
    )

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None,
                8: None,
                9: None}

    def init_faces(self):
        return {'F': None,
                'G': None,
                'H': None,
                'I': None,
                'J': None,
                'K': None,
                'L': None}

    def calculate_verts(self):
        self.add_vert(4,
                      1, 0,
                      bottom_boundary='vert')

        self.add_vert(5,
                      *self.hex_vert_coord([1, 0], 2))

        self.add_vert(6,
                      *self.hex_vert_coord([1, 0], 1))

        self.add_vert(7,
                      *self.hex_vert_coord([0, 1], 4))

        self.add_vert(8,
                      *self.hex_vert_coord([0, 1], 5))

        self.add_vert(9,
                      0, 1,
                      top_boundary='vert')

    def calculate_faces(self):
        self.add_face('F',
                      [4,
                       5,
                       left_boundary('face-3')])

        self.add_face('G',
                      [5,
                       7,
                       left_boundary('face-2')])

        self.add_face('H',
                      [4,
                       6,
                       8,
                       9,
                       7,
                       5])

        self.add_face('I',
                      [6,
                       4,
                       right_boundary('face-1')],
                      indirect=True)

        self.add_face('J',
                      [7,
                       9,
                       left_boundary('face-1')],
                      indirect=True)

        self.add_face('K',
                      [8,
                       6,
                       right_boundary('face-2')])

        self.add_face('L',
                      [9,
                       8,
                       right_boundary('face-3')])

    def color_pattern1(self):
        self.color_face('G', 1)
        self.color_face('K', 1)

    def color_pattern2(self):
        self.color_face('G', 3)
        self.color_face('K', 3)

        color = ((self.fingerprint[0] // 2 + self.fingerprint[1] % 2)) % 3
        self.color_face('H', color)

    def color_pattern3(self):
        self.color_face('G', 3)
        self.color_face('K', 3)
        self.color_face('H', 2)
