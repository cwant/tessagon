from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary

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
        self.add_vert(0,
                      0, 0,
                      left_boundary='vert-3')

        self.add_vert(1,
                      1, 0,
                      bottom_boundary='vert-2')

        self.add_vert(2,
                      0, 2.0 / 3.0,
                      left_boundary='vert-2')

        self.add_vert(3,
                      0.5, 0.5)

        self.add_vert(4,
                      1, 1.0 / 3.0,
                      right_boundary='vert-2')

        self.add_vert(5,
                      0, 1,
                      top_boundary='vert-2')

        self.add_vert(6,
                      1, 1,
                      right_boundary='vert-3')


class DissectedHexQuadTile1(DissectedHexQuadTile,
                            DissectedHexQuadTile1Verts):
    BOUNDARY = dict(
        top=['vert-1', 'edge', 'vert-2'],
        left=['vert-1', 'edge', 'vert-2', 'face', 'vert-3'],
        bottom=['vert-1', 'edge', 'vert-2'],
        right=['vert-1', 'edge', 'vert-2', 'face', 'vert-3'],
    )

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_faces(self):
        self.add_face('A', [0,
                            3,
                            2,
                            left_boundary('face')])

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
                            right_boundary('face')])

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
        self.add_vert(7,
                      0, 0,
                      left_boundary='vert-3')

        self.add_vert(8,
                      1, 0,
                      bottom_boundary='vert-2')

        self.add_vert(9,
                      0, 1.0 / 3.0,
                      left_boundary='vert-2')

        self.add_vert(10, 0.5, 0.5)

        self.add_vert(11,
                      1, 2.0 / 3.0,
                      right_boundary='vert-2')

        self.add_vert(12,
                      0, 1,
                      top_boundary='vert-2')

        self.add_vert(13,
                      1, 1,
                      right_boundary='vert-3')


class DissectedHexQuadTile2(DissectedHexQuadTile,
                            DissectedHexQuadTile2Verts):
    BOUNDARY = dict(
        top=['vert-1', 'edge', 'vert-2'],
        left=['vert-1', 'face', 'vert-2', 'edge', 'vert-3'],
        bottom=['vert-1', 'edge', 'vert-2'],
        right=['vert-1', 'face', 'vert-2', 'edge', 'vert-3'],
    )

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

        self.add_face('F', [11,
                            10,
                            8,
                            right_boundary('face')])

        self.add_face('G', [9,
                            10,
                            12,
                            left_boundary('face')])

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
