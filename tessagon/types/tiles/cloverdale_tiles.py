from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/cloverdale.svg


class CloverdaleTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True


class CloverdaleTile1(CloverdaleTile):
    BOUNDARY = dict(
        top=['vert-1', 'face', 'vert-2', 'edge', 'vert-3'],
        left=['vert-1', 'edge', 'vert-2', 'face'],
        bottom=['face', 'vert-1', 'edge', 'vert-2'],
        right=['vert-1', 'edge', 'vert-2', 'face', 'vert-3']
    )

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None,
                5: None,
                6: None,
                7: None,
                8: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None}

    def calculate_verts(self):
        # a is the side length of square
        # c is half diagonal of square
        c = 2.0 / (sqrt(2.0) + 4.0)
        a = sqrt(2.0) * c

        self.add_vert(0,
                      a / 2.0, 0.0,
                      bottom_boundary='vert-1')

        self.add_vert(1,
                      1.0, 0.0,
                      bottom_boundary='vert-2')

        self.add_vert(2,
                      0.0, a / 2.0,
                      left_boundary='vert-2')

        self.add_vert(3,
                      a / 2.0, a / 2.0)

        self.add_vert(4,
                      1.0, a / 2.0,
                      right_boundary='vert-2')

        self.add_vert(5,
                      a / 2.0 + c, a / 2.0 + c)

        self.add_vert(6,
                      0.0, 1.0,
                      top_boundary='vert-3')

        self.add_vert(7,
                      a / 2.0, 1.0,
                      top_boundary='vert-2')

        self.add_vert(8,
                      1.0, 1.0,
                      right_boundary='vert-3')

    def calculate_faces(self):
        self.add_face('A',
                      [0,
                       3,
                       2,
                       left_boundary('face')])

        self.add_face('B',
                      [2,
                       3,
                       5,
                       7,
                       6])

        self.add_face('C',
                      [0,
                       1,
                       4,
                       5,
                       3])

        self.add_face('D',
                      [7,
                       5,
                       8,
                       top_boundary('face')])

        self.add_face('E',
                      [8,
                       5,
                       4,
                       right_boundary('face')])

    def color_pattern1(self):
        self.color_face('A', 1)
        self.color_face('D', 1)
        self.color_face('E', 1)


class CloverdaleTile2(CloverdaleTile1):
    rotate = 90


class CloverdaleTile3(CloverdaleTile1):
    rotate = 180


class CloverdaleTile4(CloverdaleTile1):
    rotate = 270
