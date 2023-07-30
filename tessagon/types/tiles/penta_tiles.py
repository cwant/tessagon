from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_tile, top_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/penta.svg


class PentaTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def units(self):
        # unit is the length of the edges expressed as a
        # proportion of the tile
        unit = 2.0 / (1.0 + sqrt(3))

        a1 = unit / (2 * sqrt(3))
        a2 = 1.0 - a1

        return (a1, a2)


class PentaTile1(PentaTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_verts(self):
        (a1, a2) = self.units()

        self.add_vert(0,
                      0, a1,
                      equivalent=[left_tile(7)])

        self.add_vert(1,
                      a2, 0,
                      equivalent=[bottom_tile(8)])

        self.add_vert(2,
                      1, a2,
                      equivalent=[right_tile(5)])

        self.add_vert(3,
                      a1, 1,
                      equivalent=[top_tile(6)])

        self.add_vert(4,
                      0.5, 0.5)

    def calculate_faces(self):
        self.add_face('A', [1,
                            4,
                            0,
                            bottom_tile(5),
                            bottom_tile(9)],
                      equivalent=[bottom_tile('G')])

        self.add_face('B', [2,
                            4,
                            1,
                            right_tile(6),
                            right_tile(9)],
                      equivalent=[right_tile('H')])

        self.add_face('C', [3,
                            4,
                            2,
                            top_tile(7),
                            top_tile(9)],
                      equivalent=[top_tile('E')])

        self.add_face('D', [0,
                            4,
                            3,
                            left_tile(8),
                            left_tile(9)],
                      equivalent=[left_tile('F')])

    def color_pattern1(self):
        if self.fingerprint[0] % 2 == 0 and \
           self.fingerprint[1] % 2 == 0:
            self.color_face('A', 1)
            self.color_face('B', 1)
            self.color_face('C', 1)
            self.color_face('D', 1)


class PentaTile2(PentaTile):

    def init_verts(self):
        return {5: None,
                6: None,
                7: None,
                8: None,
                9: None}

    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None}

    def calculate_verts(self):
        (a1, a2) = self.units()

        self.add_vert(5,
                      0, a2,
                      equivalent=[left_tile(2)])

        self.add_vert(6,
                      a1, 0,
                      equivalent=[bottom_tile(3)])

        self.add_vert(7,
                      1, a1,
                      equivalent=[right_tile(0)])

        self.add_vert(8,
                      a2, 1,
                      equivalent=[top_tile(1)])

        self.add_vert(9,
                      0.5, 0.5)

    def calculate_faces(self):
        pass

    def color_pattern1(self):
        pass
