from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    top_tile, bottom_tile, bottom_left_tile, bottom_right_tile, \
    top_left_tile, top_right_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/dissected_hex_quad.svg


class DissectedHexQuadTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


# The verts can be reused for DissectedHexTri tiles
class DissectedHexQuadTile1Verts(Tile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None,
                5: None,
                6: None}

    def calculate_verts(self):
        self.add_vert(0, 0, 0, equivalent=[left_tile(8),
                                           bottom_left_tile(6),
                                           bottom_tile(12)])
        self.add_vert(1, 1, 0, equivalent=[right_tile(7),
                                           bottom_right_tile(5),
                                           bottom_tile(13)])
        self.add_vert(2, 0, 2.0 / 3.0, equivalent=[left_tile(11)])
        self.add_vert(3, 0.5, 0.5)
        self.add_vert(4, 1, 1.0 / 3.0, equivalent=[right_tile(9)])
        self.add_vert(5, 0, 1, equivalent=[left_tile(13),
                                           top_left_tile(1),
                                           top_tile(7)])
        self.add_vert(6, 1, 1, equivalent=[right_tile(12),
                                           top_right_tile(0),
                                           top_tile(8)])


class DissectedHexQuadTile1(DissectedHexQuadTile,
                            DissectedHexQuadTile1Verts):

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_faces(self):
        self.add_face('A', [0,
                            3,
                            2,
                            left_tile(10)],
                      equlvalent=[left_tile('F')])
        self.add_face('B', [0,
                            1,
                            4,
                            3])
        self.add_face('C', [2,
                            3,
                            6,
                            5])
        self.add_face('D', [6,
                            3,
                            4,
                            right_tile(10)],
                      equlvalent=[left_tile('G')])

    def color_pattern1(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('C', 1)
            self.color_face('D', 1)
        else:
            self.color_face('A', 1)
            self.color_face('B', 1)

    def color_pattern2(self):
        if self.fingerprint[0] % 6 in [0, 3]:
            self.color_face('C', 1)
            self.color_face('D', 1)
        elif self.fingerprint[0] % 6 in [1, 4]:
            self.color_face('A', 1)
            self.color_face('B', 1)


class DissectedHexQuadTile2Verts(Tile):

    def init_verts(self):
        return {7: None,
                8: None,
                9: None,
                10: None,
                11: None,
                12: None,
                13: None}

    def calculate_verts(self):
        self.add_vert(7, 0, 0, equivalent=[left_tile(1),
                                           bottom_left_tile(13),
                                           bottom_tile(5)])
        self.add_vert(8, 1, 0, equivalent=[right_tile(0),
                                           bottom_right_tile(12),
                                           bottom_tile(6)])
        self.add_vert(9, 0, 1.0 / 3.0, equivalent=[left_tile(4)])
        self.add_vert(10, 0.5, 0.5)
        self.add_vert(11, 1, 2.0 / 3.0, equivalent=[right_tile(2)])
        self.add_vert(12, 0, 1, equivalent=[left_tile(6),
                                            top_left_tile(8),
                                            top_tile(0)])
        self.add_vert(13, 1, 1, equivalent=[right_tile(5),
                                            top_right_tile(7),
                                            top_tile(1)])


class DissectedHexQuadTile2(DissectedHexQuadTile,
                            DissectedHexQuadTile2Verts):
    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None}

    def calculate_faces(self):
        self.add_face('E', [7,
                            8,
                            10,
                            9])
        self.add_face('H', [10,
                            11,
                            13,
                            12])

    def color_pattern1(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('G', 1)
            self.color_face('H', 1)
        else:
            self.color_face('E', 1)
            self.color_face('F', 1)

    def color_pattern2(self):
        if self.fingerprint[0] % 6 in [1, 4]:
            self.color_face('G', 1)
            self.color_face('H', 1)
        elif self.fingerprint[0] % 6 in [0, 3]:
            self.color_face('E', 1)
            self.color_face('F', 1)
