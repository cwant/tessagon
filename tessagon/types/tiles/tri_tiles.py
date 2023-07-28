from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile, \
    top_tile, top_left_tile, top_right_tile


class TriTile(Tile):

    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class TriTile1(TriTile):

    def init_verts(self):
        return {0: None,
                1: None}

    def init_faces(self):
        return {'A': None,
                'B': None}

    def calculate_verts(self):
        self.add_vert(0, 0, 0, equivalent=[left_tile(3),
                                           bottom_left_tile(1),
                                           bottom_tile(2)])
        self.add_vert(1, 1, 1, equivalent=[right_tile(2),
                                           top_right_tile(0),
                                           top_tile(3)])

    def calculate_faces(self):
        self.add_face('A', [0,
                            1,
                            left_tile(2)],
                      equivalent=[left_tile('D')])

        self.add_face('B', [1,
                            0,
                            right_tile(3)],
                      equivalent=[right_tile('C')])

    def color_pattern1(self):
        self.color_face('B', 1)

    def color_pattern2(self):
        # Three rows
        if self.fingerprint[1] % 3 == 0:
            self.color_face('A', 1)
            if (self.fingerprint[0] + self.fingerprint[1]) % 6 == 4:
                self.color_face('B', 1)

        elif self.fingerprint[1] % 3 == 1:
            if (self.fingerprint[0] + self.fingerprint[1]) % 6 in [4, 0]:
                self.color_face('B', 1)
            if (self.fingerprint[0] + self.fingerprint[1]) % 6 == 0:
                self.color_face('A', 1)

        else:
            if (self.fingerprint[0] + self.fingerprint[1]) % 6 in [0, 2]:
                self.color_face('A', 1)

    def color_pattern3(self):
        if (self.fingerprint[0] + 3 * self.fingerprint[1]) % 6 in [0, 4]:
            self.color_face('B', 1)


class TriTile2(TriTile):

    def init_verts(self):
        return {2: None,
                3: None}

    def init_faces(self):
        return {'C': None,
                'D': None}

    def calculate_verts(self):
        self.add_vert(2, 0, 1, equivalent=[left_tile(1),
                                           top_left_tile(3),
                                           top_tile(0)])
        self.add_vert(3, 1, 0, equivalent=[right_tile(0),
                                           bottom_right_tile(2),
                                           bottom_tile(1)])

    def calculate_faces(self):
        self.add_face('C', [3,
                            2,
                            left_tile(0)],
                      equivalent=[left_tile('B')])

        self.add_face('D', [2,
                            3,
                            right_tile(1)],
                      equivalent=[right_tile('A')])

    def color_pattern1(self):
        pass

    def color_pattern2(self):
        pass

    def color_pattern3(self):
        pass
