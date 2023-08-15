from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/hex_square_tri.svg


class HexSquareTriTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def u_units(self):
        # u_unit is the length of the edges expressed as a
        # proportion of the tile
        u_unit = 2.0 / (1.0 + sqrt(3))
        u1 = 0
        u2 = 0.5 * u_unit
        u3 = 1.0 - 0.5*u_unit
        u4 = 1.0

        return (u1, u2, u3, u4)

    def v_units(self):
        v_unit = 2.0 / (3.0 + sqrt(3))
        v1 = 0.5 * v_unit
        v2 = v_unit
        v3 = 1 - v_unit
        v4 = 1 - 0.5 * v_unit

        return (v1, v2, v3, v4)


class HexSquareTriTile1(HexSquareTriTile):
    BOUNDARY = dict(
        top=['face-1', 'split', 'face-2'],
        left=['face-1', 'split', 'face-2', 'vert', 'face-3'],
        bottom=['face-1', 'split', 'face-2'],
        right=['face-1', 'split', 'face-2', 'vert', 'face-3']
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
                'E': None,
                'F': None,
                'G': None}

    def calculate_verts(self):
        (u1, u2, u3, u4) = self.u_units()
        (v1, v2, v3, v4) = self.v_units()

        self.add_vert(0,
                      u1, v2,
                      left_boundary='vert')

        self.add_vert(1,
                      u2, v4)

        self.add_vert(2,
                      u3, v1)

        self.add_vert(3,
                      u4, v3,
                      right_boundary='vert')

    def calculate_faces(self):
        self.add_face('A', [2,
                            0,
                            left_boundary('face-3')])

        self.add_face('B', [2,
                            bottom_boundary('face-2')])

        self.add_face('C', [0,
                            1,
                            left_boundary('face-2')])

        self.add_face('D', [0,
                            2,
                            3,
                            1])

        self.add_face('E', [3,
                            2,
                            right_boundary('face-2')])

        self.add_face('F', [1,
                            top_boundary('face-2')])

        self.add_face('G', [1,
                            3,
                            right_boundary('face-3')])

    def color_pattern1(self):
        self.color_face('A', 1)
        self.color_face('D', 2)
        self.color_face('F', 2)


class HexSquareTriTile2(HexSquareTriTile):
    BOUNDARY = dict(
        top=['face-1', 'split', 'face-2'],
        left=['face-1', 'vert', 'face-2', 'split', 'face-3'],
        bottom=['face-1', 'split', 'face-2'],
        right=['face-1', 'vert', 'face-2', 'split', 'face-3']
    )

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'H': None,
                'I': None,
                'J': None,
                'K': None,
                'L': None,
                'M': None,
                'N': None}

    def calculate_verts(self):
        (u1, u2, u3, u4) = self.u_units()
        (v1, v2, v3, v4) = self.v_units()

        self.add_vert(4,
                      u1, v3,
                      left_boundary='vert')

        self.add_vert(5,
                      u2, v1)

        self.add_vert(6,
                      u3, v4)

        self.add_vert(7,
                      u4, v2,
                      right_boundary='vert')

    def calculate_faces(self):
        self.add_face('H', [5,
                            left_boundary('face-3')])

        self.add_face('I', [7,
                            5,
                            bottom_boundary('face-2')])

        self.add_face('J', [5,
                            4,
                            left_boundary('face-2')])

        self.add_face('K', [4,
                            5,
                            7,
                            6])

        self.add_face('L', [6,
                            7,
                            right_boundary('face-2')])

        self.add_face('M', [4,
                            6,
                            top_boundary('face-2')])

        self.add_face('N', [6,
                            right_boundary('face-3')])

    def color_pattern1(self):
        self.color_face('K', 2)
