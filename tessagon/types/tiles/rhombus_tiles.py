from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile, \
    top_tile, top_left_tile, top_right_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/rhombus.svg


class RhombusTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class RhombusTile1(RhombusTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0.0, 1.0 / 3.0,
                      equivalent=[left_tile(5)])

        self.add_vert(1,
                      1.0, 0.0,
                      equivalent=[right_tile(4),
                                  bottom_right_tile(2),
                                  bottom_tile(7)])

        self.add_vert(2,
                      0.0, 1.0,
                      equivalent=[left_tile(7),
                                  top_left_tile(1),
                                  top_tile(4)])

        self.add_vert(3,
                      1.0, 2.0 / 3.0,
                      equivalent=[right_tile(6)])

    def calculate_faces(self):
        self.add_face('A', [1,
                            0,
                            left_tile(4),
                            bottom_tile(6)],
                      equivalent=[left_tile('D'),
                                  bottom_left_tile('C'),
                                  bottom_tile('F')])

        self.add_face('B', [0,
                            1,
                            3,
                            2])

    def color_pattern1(self):
        self.color_face('A', 1)

    def color_pattern2(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('B', 2)
        else:
            self.color_face('B', 1)


class RhombusTile2(RhombusTile):

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'D': None,
                'E': None,
                'F': None}

    def calculate_verts(self):
        self.add_vert(4,
                      0.0, 0.0,
                      equivalent=[left_tile(1),
                                  bottom_left_tile(7),
                                  bottom_tile(2)])

        self.add_vert(5,
                      1.0, 1.0 / 3.0,
                      equivalent=[right_tile(0)])

        self.add_vert(6,
                      0.0, 2.0 / 3.0,
                      equivalent=[left_tile(3)])

        self.add_vert(7,
                      1.0, 1.0,
                      equivalent=[right_tile(2),
                                  top_right_tile(4),
                                  top_tile(1)])

    def calculate_faces(self):
        self.add_face('E', [4,
                            5,
                            7,
                            6])

    def color_pattern1(self):
        self.color_face('E', 2)

    def color_pattern2(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('E', 2)
        else:
            self.color_face('E', 1)
