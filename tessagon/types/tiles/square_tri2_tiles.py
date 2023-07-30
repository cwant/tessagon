from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_tile, bottom_left_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/square_tri2.svg


class SquareTri2Tile(Tile):
    uv_ratio = 1.0 / (2.0 + sqrt(3.0))

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def v_units(self):
        v_unit = 2.0 / (2.0 + sqrt(3.0))
        v1 = v_unit * 0.5
        v2 = 1.0 - v1

        return (v1, v2)


class SquareTri2Tile1(SquareTri2Tile):

    def init_verts(self):
        return {0: None,
                1: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_verts(self):
        (v1, v2) = self.v_units()

        self.add_vert(0,
                      1.0, v1,
                      equivalent=[right_tile(2)])

        self.add_vert(1,
                      0.0, v2,
                      equivalent=[left_tile(3)])

    def calculate_faces(self):
        self.add_face('A', [0,
                            left_tile(2),
                            bottom_left_tile(1),
                            bottom_tile(3)],
                      equivalent=[left_tile('E'),
                                  bottom_left_tile('D'),
                                  bottom_tile('H')],
                      face_type='square')

        self.add_face('B', [0,
                            1,
                            left_tile(2)],
                      equivalent=[left_tile('F')],
                      face_type='triangle')

        self.add_face('C', [1,
                            0,
                            right_tile(3)],
                      equivalent=[left_tile('G')],
                      face_type='triangle')

    def color_pattern1(self):
        self.color_face('A', 1)


class SquareTri2Tile2(SquareTri2Tile):

    def init_verts(self):
        return {2: None,
                3: None}

    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None}

    def calculate_verts(self):
        (v1, v2) = self.v_units()

        self.add_vert(2,
                      0.0, v1,
                      equivalent=[left_tile(0)])

        self.add_vert(3,
                      1.0, v2,
                      equivalent=[right_tile(1)])

    def calculate_faces(self):
        pass

    def color_pattern1(self):
        pass
