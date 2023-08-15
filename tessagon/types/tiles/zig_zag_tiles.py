from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/zig_zag.svg


class ZigZagTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class ZigZagTile1(ZigZagTile):
    BOUNDARY = dict(
        top=['vert-1', 'face', 'vert-2', 'edge', 'vert-3'],
        left=['vert-1', 'edge', 'vert-2', 'edge', 'vert-3'],
        bottom=['vert-1', 'edge', 'vert-2', 'edge', 'vert-3'],
        right=['vert-1', 'face', 'vert-2', 'edge', 'vert-3'],
    )

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
                      left_boundary='vert-3')

        self.add_vert(1,
                      0.5, 0,
                      bottom_boundary='vert-2')

        self.add_vert(2,
                      1, 0,
                      bottom_boundary='vert-3')

        self.add_vert(3,
                      1, 0.5,
                      right_boundary='vert-2')

        self.add_vert(4,
                      1, 1,
                      right_boundary='vert-3')

        self.add_vert(5,
                      0.5, 1,
                      top_boundary='vert-2')

        self.add_vert(6,
                      0, 1,
                      top_boundary='vert-3')

        self.add_vert(7,
                      0, 0.5,
                      left_boundary='vert-2')

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
                            right_boundary('face')])

        self.add_face('C', [5,
                            8,
                            3,
                            4,
                            top_boundary('face')])

    def color_pattern1(self):
        self.color_face('A', 1)


class ZigZagTile2(ZigZagTile):
    BOUNDARY = dict(
        top=['vert-1', 'edge', 'vert-2', 'edge', 'vert-3'],
        left=['vert-1', 'edge', 'vert-2', 'face', 'vert-3'],
        bottom=['vert-1', 'edge', 'vert-2', 'face', 'vert-3'],
        right=['vert-1', 'edge', 'vert-2', 'edge', 'vert-3'],
    )

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
                      left_boundary='vert-3')

        self.add_vert(10,
                      0.5, 0,
                      bottom_boundary='vert-2')

        self.add_vert(11,
                      1, 0,
                      bottom_boundary='vert-3')

        self.add_vert(12,
                      1, 0.5,
                      right_boundary='vert-2')

        self.add_vert(13,
                      1, 1,
                      right_boundary='vert-3')

        self.add_vert(14,
                      0.5, 1,
                      top_boundary='vert-2')

        self.add_vert(15,
                      0, 1,
                      top_boundary='vert-3')

        self.add_vert(16,
                      0, 0.5,
                      left_boundary='vert-2')

        self.add_vert(17,
                      0.5, 0.5)

    def calculate_faces(self):
        self.add_face('D', [9,
                            10,
                            17,
                            16,
                            left_boundary('face')])

        self.add_face('E', [11,
                            12,
                            17,
                            10,
                            bottom_boundary('face')])

        self.add_face('F', [12,
                            13,
                            14,
                            15,
                            16,
                            17])

    def color_pattern1(self):
        self.color_face('F', 1)
