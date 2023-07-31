from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import right_tile, left_tile, \
    top_tile, top_left_tile, top_right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/dissected_triangle.svg


class DissectedTriangleTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class DissectedTriangleTile1(DissectedTriangleTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0, 0,
                      equivalent=[left_tile(5),
                                  bottom_left_tile(3),
                                  bottom_tile(6)])

        self.add_vert(1,
                      1, 1.0 / 3.0,
                      equivalent=[right_tile(4)])

        self.add_vert(2,
                      0, 2.0 / 3.0,
                      equivalent=[left_tile(7)])

        self.add_vert(3,
                      1, 1,
                      equivalent=[right_tile(6),
                                  top_right_tile(0),
                                  top_tile(5)])

    def calculate_faces(self):
        self.add_face('A', [0, 3, 2])
        self.add_face('B', [0, 1, 3])
        self.add_face('C', [1, 0, right_tile(5)],
                      equivalent=[right_tile('E')])
        self.add_face('D', [2, 3, left_tile(6)],
                      equivalent=[left_tile('H')])

    def color_pattern1(self):
        if self.fingerprint[1] % 2 == 0:
            if self.fingerprint[0] % 6 == 0:
                self.color_face('A', 1)
                self.color_face('B', 1)
            if self.fingerprint[0] % 6 == 4:
                self.color_face('C', 1)
            if self.fingerprint[0] % 6 == 2:
                self.color_face('D', 1)
        else:
            if self.fingerprint[0] % 6 == 3:
                self.color_face('A', 1)
                self.color_face('B', 1)
            if self.fingerprint[0] % 6 == 1:
                self.color_face('C', 1)
            if self.fingerprint[0] % 6 == 5:
                self.color_face('D', 1)


class DissectedTriangleTile2(DissectedTriangleTile):

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None}

    def calculate_verts(self):
        self.add_vert(4,
                      0, 1.0 / 3.0,
                      equivalent=[left_tile(1)])

        self.add_vert(5,
                      1, 0,
                      equivalent=[right_tile(0),
                                  bottom_right_tile(6),
                                  bottom_tile(3)])

        self.add_vert(6,
                      0, 1,
                      equivalent=[left_tile(3),
                                  top_left_tile(5),
                                  top_tile(0)])
        self.add_vert(7,
                      1, 2.0 / 3.0,
                      equivalent=[right_tile(2)])

    def calculate_faces(self):
        self.add_face('E', [5, 4, left_tile(0)],
                      equivalent=[left_tile('C')])
        self.add_face('F', [5, 6, 4])
        self.add_face('G', [5, 7, 6])
        self.add_face('H', [6, 7, right_tile(3)],
                      equivalent=[right_tile('D')])

    def color_pattern1(self):
        if self.fingerprint[1] % 2 == 0:
            if self.fingerprint[0] % 6 == 3:
                self.color_face('F', 1)
                self.color_face('G', 1)
        else:
            if self.fingerprint[0] % 6 == 0:
                self.color_face('F', 1)
                self.color_face('G', 1)
