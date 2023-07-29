from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    top_tile, top_left_tile, top_right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/hex_tri.svg


class HexTriTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class HexTriTile1(HexTriTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0, 1,
                      equivalent=[left_tile(5),
                                  top_left_tile(2),
                                  top_tile(3)])

        self.add_vert(1,
                      0.5, 0.5)

        self.add_vert(2,
                      1, 0,
                      equivalent=[right_tile(3),
                                  bottom_right_tile(0),
                                  bottom_tile(5)])

    def calculate_faces(self):
        self.add_face('A', [1,
                            0,
                            left_tile(4)],
                      equivalent=[left_tile('G')])

        self.add_face('B', [2,
                            1,
                            left_tile(4),
                            left_tile(3),
                            bottom_left_tile(1),
                            bottom_tile(4)],
                      equivalent=[left_tile('H'),
                                  bottom_left_tile('D'),
                                  bottom_tile('F')])

        self.add_face('C', [1,
                            2,
                            right_tile(4)],
                      equivalent=[left_tile('E')])

    def color_pattern1(self):
        self.color_face('B', 1)


class HexTriTile2(HexTriTile):

    def init_verts(self):
        return {3: None,
                4: None,
                5: None}

    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None}

    def calculate_verts(self):
        self.add_vert(3,
                      0, 0,
                      equivalent=[left_tile(2),
                                  bottom_left_tile(5),
                                  bottom_tile(0)])

        self.add_vert(4,
                      0.5, 0.5)

        self.add_vert(5,
                      1, 1,
                      equivalent=[right_tile(0),
                                  top_right_tile(3),
                                  top_tile(2)])

    def calculate_faces(self):
        pass

    def color_pattern1(self):
        pass
