from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/hex.svg


class HexTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class HexTile1(HexTile):
    BOUNDARY = dict(
        top=['face', 'split'],
        left=['edge', 'vert', 'face'],
        bottom=['face', 'split'],
        right=['edge', 'vert', 'face'],
    )

    def init_verts(self):
        return {0: None,
                1: None}

    def init_faces(self):
        return {'A': None,
                'B': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0, 2.0/3.0,
                      left_boundary='vert')
        self.add_vert(1,
                      1, 1.0/3.0,
                      right_boundary='vert')

    def calculate_faces(self):
        self.add_face('A', [1,
                            0,
                            left_boundary('face')])

        self.add_face('B', [0,
                            1,
                            right_boundary('face')])

    def color_pattern1(self):
        if self.fingerprint[0] % 6 == 0:
            self.color_face('B', 1)

    def color_pattern2(self):
        self.color_pattern1()
        if self.fingerprint[0] % 6 == 2:
            self.color_face('B', 2)


class HexTile2(HexTile):
    BOUNDARY = dict(
        top=['split', 'face'],
        left=['face', 'vert', 'edge'],
        bottom=['split', 'face'],
        right=['face', 'vert', 'edge'],
    )

    def init_verts(self):
        return {2: None,
                3: None}

    def init_faces(self):
        return {'C': None,
                'D': None}

    def calculate_verts(self):
        self.add_vert(2,
                      0, 1.0/3.0,
                      left_boundary='vert')
        self.add_vert(3,
                      1, 2.0/3.0,
                      right_boundary='vert')

    def calculate_faces(self):
        self.add_face('C', [3,
                            2,
                            bottom_boundary('face')])

        self.add_face('D', [2,
                            3,
                            top_boundary('face')])

    def color_pattern1(self):
        if self.fingerprint[0] % 6 == 3:
            self.color_face('C', 1)

    def color_pattern2(self):
        self.color_pattern1()
        if self.fingerprint[0] % 6 == 5:
            self.color_face('C', 2)
