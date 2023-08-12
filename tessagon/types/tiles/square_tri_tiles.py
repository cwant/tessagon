from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_tile, top_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/square_tri.svg


class SquareTriTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def units(self):
        # unit is the length of the edges expressed as a
        # proportion of the tile
        unit = 2.0 / (1.0 + sqrt(3))

        a1 = 0.5 * unit
        a2 = 1.0 - a1

        return (a1, a2)


class SquareTriTile1(SquareTriTile):

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
        (a1, a2) = self.units()

        self.add_vert(0,
                      a1, 0,
                      equivalent=[bottom_tile(6)])

        self.add_vert(1,
                      1, a1,
                      equivalent=[right_tile(7)])

        self.add_vert(2,
                      a2, 1,
                      equivalent=[top_tile(4)])

        self.add_vert(3,
                      0, a2,
                      equivalent=[left_tile(5)])

    def calculate_faces(self):
        self.add_face('A', [0,
                            3,
                            left_tile(4)],
                      equivalent=[left_tile('G')],
                      face_type='triangle')

        self.add_face('B', [1,
                            0,
                            bottom_tile(5)],
                      equivalent=[bottom_tile('H')],
                      face_type='triangle')

        self.add_face('C', [2,
                            1,
                            right_tile(6)],
                      equivalent=[right_tile('I')],
                      face_type='triangle')

        self.add_face('D', [3,
                            2,
                            top_tile(7)],
                      equivalent=[top_tile('F')],
                      face_type='triangle')

        self.add_face('E', [0,
                            1,
                            2,
                            3],
                      face_type='square')

    def color_pattern1(self):
        self.color_face('E', 1)

    def color_pattern2(self):
        self.color_face('E', 1)

        self.color_face('B', 2)
        self.color_face('D', 2)


class SquareTriTile2(SquareTriTile):

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'F': None,
                'G': None,
                'H': None,
                'I': None,
                'J': None}

    def calculate_verts(self):
        (a1, a2) = self.units()

        self.add_vert(4,
                      a2, 0,
                      equivalent=[bottom_tile(2)])

        self.add_vert(5,
                      1, a2,
                      equivalent=[right_tile(3)])

        self.add_vert(6,
                      a1, 1,
                      equivalent=[top_tile(0)])

        self.add_vert(7,
                      0, a1,
                      equivalent=[left_tile(1)])

    def calculate_faces(self):
        self.add_face('J', [4,
                            5,
                            6,
                            7],
                      face_type='square')

    def color_pattern1(self):
        self.color_face('J', 1)

    def color_pattern2(self):
        self.color_face('J', 1)