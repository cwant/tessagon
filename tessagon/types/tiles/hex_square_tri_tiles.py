from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile

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

        self.add_vert(0, u1, v2,
                      equivalent=[left_tile(7)])
        self.add_vert(1, u2, v4)
        self.add_vert(2, u3, v1)
        self.add_vert(3, u4, v3,
                      equivalent=[right_tile(4)])

    def calculate_faces(self):
        self.add_face('A', [2,
                            0,
                            left_tile(5),
                            bottom_left_tile(1),
                            bottom_tile(4),
                            bottom_tile(6)],
                      equivalent=[left_tile('I'),
                                  bottom_left_tile('G'),
                                  bottom_tile('M')])

        self.add_face('B', [2,
                            bottom_tile(6),
                            bottom_right_tile(1),
                            right_tile(5)],
                      equivalent=[bottom_tile('N'),
                                  bottom_right_tile('F'),
                                  right_tile('H')])

        self.add_face('C', [0,
                            1,
                            left_tile(6)],
                      equivalent=[left_tile('L')])

        self.add_face('D', [0,
                            2,
                            3,
                            1])

        self.add_face('E', [3,
                            2,
                            right_tile(5)],
                      equivalent=[right_tile('J')])

    def color_pattern1(self):
        self.color_face('A', 1)
        self.color_face('D', 2)
        self.color_face('F', 2)


class HexSquareTriTile2(HexSquareTriTile):

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

        self.add_vert(4, u1, v3,
                      equivalent=[left_tile(3)])
        self.add_vert(5, u2, v1)
        self.add_vert(6, u3, v4)
        self.add_vert(7, u4, v2,
                      equivalent=[right_tile(0)])

    def calculate_faces(self):
        self.add_face('K', [4,
                            5,
                            7,
                            6])

    def color_pattern1(self):
        self.color_face('K', 2)
