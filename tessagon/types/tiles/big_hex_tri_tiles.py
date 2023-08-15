from math import atan2, sqrt, sin, cos, pi
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/big_hex_tri.svg


class BigHexTriTile(Tile):
    uv_ratio = 1.0 / sqrt(3)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

        self.hexagon_ratio = kwargs.get('hexagon_ratio', 0.5)

        # in u units
        self.hex_radius = 4 * self.hexagon_ratio / sqrt(7)

        # Tilt
        self.theta_offset = -atan2(1, 3 * sqrt(3)) + pi/6
        self.hex_theta = [(self.theta_offset + number * pi / 3.0)
                          for number in range(6)]

    def hex_vert_coord(self, center, number):
        # number in range(6)
        return [center[0] +
                self.hex_radius * cos(self.hex_theta[number]),
                center[1] +
                self.hex_radius * sin(self.hex_theta[number]) * self.uv_ratio]


class BigHexTriTile1(BigHexTriTile):
    BOUNDARY = dict(
        top=['face-1', 'split', 'face-2', 'split'],
        left=['split', 'face-1', 'split', 'face-2',
              'split', 'face-3', 'split', 'face-4'],
        bottom=['face-1', 'split', 'face-2', 'split'],
        right=['split', 'face-1', 'split', 'face-2',
               'split', 'face-3', 'split', 'face-4'],
    )

    def init_verts(self):
        verts = {0: None,
                 1: None,
                 2: None,
                 3: None}

        return verts

    def init_faces(self):
        faces = {'A': None,
                 'B': None,
                 'C': None,
                 'D': None,
                 'E': None,
                 'F': None,
                 'G': None,
                 'H': None,
                 'I': None,
                 'J': None,
                 'K': None,
                 'L': None}

        return faces

    def calculate_verts(self):
        self.add_vert(0,
                      *self.hex_vert_coord([0, 0], 0))
        self.add_vert(1,
                      *self.hex_vert_coord([0, 0], 1))
        self.add_vert(2,
                      *self.hex_vert_coord([1, 1], 4))
        self.add_vert(3,
                      *self.hex_vert_coord([1, 1], 3))

    def calculate_faces(self):
        self.add_face('A',
                      [0,
                       1,
                       left_boundary('face-4')])

        self.add_face('B',
                      [3,
                       top_boundary('face-2')])

        self.add_face('C',
                      [3,
                       left_boundary('face-1')])
        # TODO: skip=True ? No verts to add there
        # (diagonal edge on tile corner)

        self.add_face('D',
                      [1,
                       3,
                       left_boundary('face-2')])

        self.add_face('E',
                      [1,
                       left_boundary('face-3')])

        self.add_face('F',
                      [2,
                       3,
                       1])

        self.add_face('G',
                      [2,
                       1,
                       0])

        self.add_face('H',
                      [2,
                       right_boundary('face-3')])

        self.add_face('I',
                      [2,
                       0,
                       right_boundary('face-2')])

        self.add_face('J',
                      [0,
                       right_boundary('face-1')])

        self.add_face('K',
                      [0,
                       bottom_boundary('face-2')])

        self.add_face('L',
                      [3,
                       2,
                       right_boundary('face-4')])

    def color_pattern1(self):
        self.color_face('F', 1)


class BigHexTriTile2(BigHexTriTile):
    BOUNDARY = dict(
        top=['tangent-split', 'face-1', 'split', 'face-2'],
        left=['face-1', 'split', 'face-2', 'split',
              'face-3', 'split', 'face-4', 'tangent-split'],
        bottom=['tangent-split', 'face-1', 'split', 'face-2'],
        right=['face-1', 'split', 'face-2', 'split',
               'face-3', 'split', 'face-4', 'tangent-split']
    )

    def init_verts(self):
        verts = {4: None,
                 5: None}
        return verts

    def init_faces(self):
        faces = {'M': None,
                 'N': None,
                 'O': None,
                 'P': None,
                 'Q': None,
                 'R': None,
                 'S': None,
                 'T': None}

        return faces

    def calculate_verts(self):
        self.add_vert(4, *self.hex_vert_coord([1, 0], 2))
        self.add_vert(5, *self.hex_vert_coord([0, 1], 5))

    def calculate_faces(self):
        self.add_face('M',
                      [4,
                       bottom_boundary('face-2')])

        self.add_face('N',
                      [4,
                       left_boundary('face-4')])

        self.add_face('O',
                      [4,
                       left_boundary('face-3')])

        self.add_face('P',
                      [4,
                       5,
                       left_boundary('face-2')])

        self.add_face('Q',
                      [5,
                       4,
                       right_boundary('face-2')])

        self.add_face('R',
                      [5,
                       right_boundary('face-3')])

        self.add_face('S',
                      [5,
                       right_boundary('face-4')])

        self.add_face('T',
                      [5,
                       top_boundary('face-2')])

    def color_pattern1(self):
        self.color_face('O', 1)
        self.color_face('Q', 1)
        self.color_face('S', 1)
        self.color_face('T', 2)
