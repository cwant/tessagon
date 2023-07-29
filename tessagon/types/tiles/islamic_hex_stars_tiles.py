from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile, \
    top_tile, top_left_tile, top_right_tile

# See page 3 of "Islamic Design" by Daud Sutton
# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/islamic_hex_stars.svg


class IslamicHexStarsTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class IslamicHexStarsTile1(IslamicHexStarsTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None,
                5: None,
                6: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0.0, 1.0 / 3.0,
                      equivalent=[left_tile(11)])
        self.add_vert(1,
                      0.5, 0.5)
        self.add_vert(2,
                      0.5, 1.0 / 6.0)
        self.add_vert(3,
                      1.0, 0.0,
                      equivalent=[right_tile(7),
                                  bottom_right_tile(6),
                                  bottom_tile(13)])
        self.add_vert(4,
                      1.0, 2.0 / 3.0,
                      equivalent=[right_tile(10)])
        self.add_vert(5,
                      0.5, 5.0 / 6.0)
        self.add_vert(6,
                      0.0, 1.0,
                      equivalent=[left_tile(13),
                                  top_left_tile(3),
                                  top_tile(7)])

    def calculate_faces(self):
        self.add_face('A', [3,
                            2,
                            1,
                            0,
                            left_tile(9),
                            left_tile(8),
                            left_tile(7),
                            bottom_left_tile(5),
                            bottom_left_tile(1),
                            bottom_tile(10),
                            bottom_tile(9),
                            bottom_tile(12)],
                      equilalent=[left_tile('F'),
                                  bottom_left_tile('D'),
                                  bottom_tile('G')])

        self.add_face('B', [4,
                            1,
                            2,
                            3,
                            right_tile(8),
                            right_tile(9)],
                      equilalent=[right_tile('E')])

        self.add_face('C', [6,
                            5,
                            1,
                            0,
                            left_tile(9),
                            left_tile(12)],
                      equilalent=[left_tile('H')])

    def color_pattern1(self):
        self.color_face('A', 1)


class IslamicHexStarsTile2(IslamicHexStarsTile):

    def init_verts(self):
        return {7: None,
                8: None,
                9: None,
                10: None,
                11: None,
                12: None,
                13: None}

    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None}

    def calculate_verts(self):
        self.add_vert(7,
                      0.0, 0.0,
                      equivalent=[left_tile(3),
                                  bottom_left_tile(13),
                                  bottom_tile(6)])
        self.add_vert(8,
                      0.5, 1.0 / 6.0)
        self.add_vert(9,
                      0.5, 0.5)
        self.add_vert(10,
                      0.0, 2.0 / 3.0,
                      equivalent=[left_tile(4)])
        self.add_vert(11,
                      1.0, 1.0 / 3.0,
                      equivalent=[right_tile(0)])
        self.add_vert(12,
                      0.5, 5.0 / 6.0)
        self.add_vert(13,
                      1.0, 1.0,
                      equivalent=[right_tile(6),
                                  top_right_tile(7),
                                  top_tile(3)])

    def calculate_faces(self):
        pass

    def color_pattern1(self):
        pass
