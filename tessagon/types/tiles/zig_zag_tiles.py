from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    top_tile, top_left_tile, top_right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/zig_zag.svg


class ZigZagTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class ZigZagTile1(ZigZagTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None,
                5: None,
                6: None,
                7: None,
                8: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0, 0,
                      equivalent=[left_tile(11),
                                  bottom_left_tile(4),
                                  bottom_tile(15)])

        self.add_vert(1,
                      0.5, 0,
                      equivalent=[bottom_tile(14)])

        self.add_vert(2,
                      1, 0,
                      equivalent=[right_tile(9),
                                  bottom_right_tile(6),
                                  bottom_tile(13)])

        self.add_vert(3,
                      1, 0.5,
                      equivalent=[right_tile(16)])

        self.add_vert(4,
                      1, 1,
                      equivalent=[right_tile(15),
                                  top_right_tile(0),
                                  top_tile(11)])

        self.add_vert(5,
                      0.5, 1,
                      equivalent=[top_tile(10)])

        self.add_vert(6,
                      0, 1,
                      equivalent=[left_tile(13),
                                  top_left_tile(2),
                                  top_tile(9)])

        self.add_vert(7,
                      0, 0.5,
                      equivalent=[left_tile(12)])

        self.add_vert(8,
                      0.5, 0.5)

    def calculate_faces(self):
        self.add_face('A', [0,
                            1,
                            8,
                            5,
                            6,
                            7])

        self.add_face('B', [3,
                            8,
                            1,
                            2,
                            right_tile(10),
                            right_tile(17)],
                      equivalent=[right_tile('D')])

        self.add_face('C', [4,
                            3,
                            8,
                            5,
                            top_tile(17),
                            top_tile(12)],
                      equivalent=[top_tile('E')])

    def color_pattern1(self):
        self.color_face('A', 1)


class ZigZagTile2(ZigZagTile):

    def init_verts(self):
        return {9: None,
                10: None,
                11: None,
                12: None,
                13: None,
                14: None,
                15: None,
                16: None,
                17: None}

    def init_faces(self):
        return {'D': None,
                'E': None,
                'F': None}

    def calculate_verts(self):
        self.add_vert(9,
                      0, 0,
                      equivalent=[left_tile(11),
                                  bottom_left_tile(4),
                                  bottom_tile(15)])

        self.add_vert(10,
                      0.5, 0,
                      equivalent=[bottom_tile(14)])

        self.add_vert(11,
                      1, 0,
                      equivalent=[right_tile(9),
                                  bottom_right_tile(6),
                                  bottom_tile(13)])

        self.add_vert(12,
                      1, 0.5,
                      equivalent=[right_tile(16)])

        self.add_vert(13,
                      1, 1,
                      equivalent=[right_tile(15),
                                  top_right_tile(0),
                                  top_tile(11)])

        self.add_vert(14,
                      0.5, 1,
                      equivalent=[top_tile(10)])

        self.add_vert(15,
                      0, 1,
                      equivalent=[left_tile(13),
                                  top_left_tile(2),
                                  top_tile(9)])

        self.add_vert(16,
                      0, 0.5,
                      equivalent=[left_tile(12)])

        self.add_vert(17,
                      0.5, 0.5)

    def calculate_faces(self):
        self.add_face('F', [12,
                            13,
                            14,
                            15,
                            16,
                            17])

    def color_pattern1(self):
        self.color_face('F', 1)
