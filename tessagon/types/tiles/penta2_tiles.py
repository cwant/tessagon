from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile, \
    top_tile, top_left_tile, top_right_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/penta2.svg


class Penta2Tile(Tile):
    uv_ratio = 1.0 / (2.0 + sqrt(3.0))

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def v_units(self):
        v_unit = 2.0 / (2.0 + sqrt(3.0))
        v1 = 0
        v2 = v_unit * 0.5 * (1.0 + 1.0 / sqrt(3.0))
        v3 = 1.0 - v2
        v4 = 1.0

        return (v1, v2, v3, v4)


class Penta2Tile1(Penta2Tile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None}

    def calculate_verts(self):
        (v1, v2, v3, v4) = self.v_units()

        self.add_vert(0,
                      0, v1,
                      equivalent=[left_tile(4),
                                  bottom_left_tile(3),
                                  bottom_tile(7)])

        self.add_vert(1,
                      0, v2,
                      equivalent=[left_tile(5)])

        self.add_vert(2,
                      1, v3,
                      equivalent=[right_tile(6)])

        self.add_vert(3,
                      1, v4,
                      equivalent=[right_tile(7),
                                  top_right_tile(0),
                                  top_tile(4)])

    def calculate_faces(self):
        self.add_face('A', [2,
                            1,
                            0,
                            right_tile(4),
                            right_tile(5)],
                      equivalent=[right_tile('C')])

        self.add_face('B', [1,
                            2,
                            3,
                            left_tile(7),
                            left_tile(6)],
                      equivalent=[left_tile('D')])

    def color_pattern1(self):
        self.color_face('B', 1)


class Penta2Tile2(Penta2Tile):

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'C': None,
                'D': None}

    def calculate_verts(self):
        (v1, v2, v3, v4) = self.v_units()

        self.add_vert(4,
                      1, v1,
                      equivalent=[right_tile(0),
                                  bottom_right_tile(7),
                                  bottom_tile(3)])

        self.add_vert(5,
                      1, v2,
                      equivalent=[right_tile(1)])

        self.add_vert(6,
                      0, v3,
                      equivalent=[left_tile(2)])

        self.add_vert(7,
                      0, v4,
                      equivalent=[left_tile(3),
                                  top_left_tile(4),
                                  top_tile(0)])

    def calculate_faces(self):
        pass

    def color_pattern1(self):
        pass
