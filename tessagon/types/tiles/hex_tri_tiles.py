from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/hex_tri.svg


class HexTriTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class HexTriTile1(HexTriTile):
    BOUNDARY = dict(
        top=['face', 'vert'],
        left=['vert', 'face-1', 'split', 'face-2'],
        bottom=['face', 'vert'],
        right=['vert', 'face-1', 'split', 'face-2'],
    )

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
                      top_boundary='vert')

        self.add_vert(1,
                      0.5, 0.5)

        self.add_vert(2,
                      1, 0,
                      bottom_boundary='vert')

    def calculate_faces(self):
        self.add_face('A', [1,
                            0,
                            left_boundary('face-1')])

        self.add_face('B', [2,
                            1,
                            left_boundary('face-2')])

        self.add_face('C', [1,
                            2,
                            right_boundary('face-1')])

        self.add_face('D', [0,
                            1,
                            right_boundary('face-2')])

    def color_pattern1(self):
        self.color_face('B', 1)


class HexTriTile2(HexTriTile):
    BOUNDARY = dict(
        top=['vert', 'face'],
        left=['face-1', 'split', 'face-2', 'vert'],
        bottom=['vert', 'face'],
        right=['face-1', 'split', 'face-2', 'vert'],
    )

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
                      left_boundary='vert')

        self.add_vert(4,
                      0.5, 0.5)

        self.add_vert(5,
                      1, 1,
                      right_boundary='vert')

    def calculate_faces(self):
        self.add_face('E', [3,
                            4,
                            left_boundary('face-2')])

        self.add_face('F', [4,
                            5,
                            top_boundary('face')])

        self.add_face('G', [5,
                            4,
                            right_boundary('face-2')])

        self.add_face('H', [4,
                            3,
                            bottom_boundary('face')])

    def color_pattern1(self):
        pass
