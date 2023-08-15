from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

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
    BOUNDARY = dict(
        top=['face', 'vert'],
        left=['vert-1', 'face-1', 'vert-2', 'face-2'],
        bottom=['face', 'vert'],
        right=['vert-1', 'face-1', 'vert-2', 'face-2']
    )

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
                      left_boundary='vert-2')

        self.add_vert(1,
                      0.5, 0.5)

        self.add_vert(2,
                      0.5, 1.0 / 6.0)

        self.add_vert(3,
                      1.0, 0.0,
                      bottom_boundary='vert')

        self.add_vert(4,
                      1.0, 2.0 / 3.0,
                      right_boundary='vert-2')

        self.add_vert(5,
                      0.5, 5.0 / 6.0)

        self.add_vert(6,
                      0.0, 1.0,
                      top_boundary='vert')

    def calculate_faces(self):
        self.add_face('A', [3,
                            2,
                            1,
                            0,
                            left_boundary('face-2')])

        self.add_face('B', [4,
                            1,
                            2,
                            3,
                            right_boundary('face-1')])

        self.add_face('C', [0,
                            1,
                            5,
                            6,
                            left_boundary('face-1')])

        self.add_face('D', [6,
                            5,
                            1,
                            4,
                            right_boundary('face-2')])

    def color_pattern1(self):
        self.color_face('A', 1)


class IslamicHexStarsTile2(IslamicHexStarsTile):
    BOUNDARY = dict(
        top=['vert', 'face'],
        left=['face-1', 'vert-1', 'face-2', 'vert-2'],
        bottom=['vert', 'face'],
        right=['face-1', 'vert-1', 'face-2', 'vert-2']
    )

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
                      left_boundary='vert-2')

        self.add_vert(8,
                      0.5, 1.0 / 6.0)

        self.add_vert(9,
                      0.5, 0.5)

        self.add_vert(10,
                      0.0, 2.0 / 3.0,
                      left_boundary='vert-1')

        self.add_vert(11,
                      1.0, 1.0 / 3.0,
                      right_boundary='vert-1')

        self.add_vert(12,
                      0.5, 5.0 / 6.0)

        self.add_vert(13,
                      1.0, 1.0,
                      right_boundary='vert-2')

    def calculate_faces(self):
        self.add_face('E', [7,
                            8,
                            9,
                            10,
                            left_boundary('face-2')])

        self.add_face('F', [11,
                            9,
                            8,
                            7,
                            bottom_boundary('face')])

        self.add_face('G', [10,
                            9,
                            12,
                            13,
                            top_boundary('face')])

        self.add_face('H', [13,
                            12,
                            9,
                            11,
                            right_boundary('face-2')])

    def color_pattern1(self):
        pass
