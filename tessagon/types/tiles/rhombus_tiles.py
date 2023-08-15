from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/rhombus.svg


class RhombusTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class RhombusTile1(RhombusTile):
    BOUNDARY = dict(
        top=['face', 'vert'],
        left=['vert-1', 'edge', 'vert-2', 'face'],
        bottom=['face', 'vert'],
        right=['vert-1', 'edge', 'vert-2', 'face']
    )

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0.0, 1.0 / 3.0,
                      left_boundary='vert-2')

        self.add_vert(1,
                      1.0, 0.0,
                      bottom_boundary='vert')

        self.add_vert(2,
                      0.0, 1.0,
                      top_boundary='vert')

        self.add_vert(3,
                      1.0, 2.0 / 3.0,
                      right_boundary='vert-2')

    def calculate_faces(self):
        self.add_face('A', [1,
                            0,
                            left_boundary('face')])

        self.add_face('B', [0,
                            1,
                            3,
                            2])

        self.add_face('C', [2,
                            3,
                            right_boundary('face')])

    def color_pattern1(self):
        self.color_face('A', 1)

    def color_pattern2(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('B', 2)
        else:
            self.color_face('B', 1)


class RhombusTile2(RhombusTile):
    BOUNDARY = dict(
        top=['vert', 'face'],
        left=['face', 'vert-1', 'edge', 'vert-2'],
        bottom=['vert', 'face'],
        right=['face', 'vert-1', 'edge', 'vert-2']
    )

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'D': None,
                'E': None,
                'F': None}

    def calculate_verts(self):
        self.add_vert(4,
                      0.0, 0.0,
                      left_boundary='vert-2')

        self.add_vert(5,
                      1.0, 1.0 / 3.0,
                      right_boundary='vert-1')

        self.add_vert(6,
                      0.0, 2.0 / 3.0,
                      left_boundary='vert-1')

        self.add_vert(7,
                      1.0, 1.0,
                      right_boundary='vert-2')

    def calculate_faces(self):
        self.add_face('D', [5,
                            4,
                            bottom_boundary('face')])

        self.add_face('E', [4,
                            5,
                            7,
                            6])

        self.add_face('F', [6,
                            7,
                            top_boundary('face')])

    def color_pattern1(self):
        self.color_face('E', 2)

    def color_pattern2(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('E', 2)
        else:
            self.color_face('E', 1)
