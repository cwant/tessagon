from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/penta2.svg


class Penta2Tile(Tile):
    uv_ratio = 1.0 / (2.0 + sqrt(3.0))

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def v_units(self):
        v_unit = 2.0 / (2.0 + sqrt(3.0))
        v1 = 0
        v2 = v_unit * 0.5 * (1.0 + 1.0 / sqrt(3.0))
        v3 = 1.0 - v2
        v4 = 1.0

        return (v1, v2, v3, v4)


class Penta2Tile1(Penta2Tile):
    BOUNDARY = dict(
        top=['vert', 'edge'],
        left=['split', 'face', 'vert-1', 'edge', 'vert-2'],
        bottom=['vert', 'edge'],
        right=['split', 'face', 'vert-1', 'edge', 'vert-2']
    )

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None}

    def calculate_verts(self):
        (v1, v2, v3, v4) = self.v_units()

        self.add_vert(0,
                      0, v1,
                      left_boundary='vert-2')

        self.add_vert(1,
                      0, v2,
                      left_boundary='vert-1')

        self.add_vert(2,
                      1, v3,
                      right_boundary='vert-1')

        self.add_vert(3,
                      1, v4,
                      right_boundary='vert-2')

    def calculate_faces(self):
        self.add_face('A', [2,
                            1,
                            0,
                            right_boundary('face')])

        self.add_face('B', [1,
                            2,
                            3,
                            left_boundary('face')])

    def color_pattern1(self):
        self.color_face('B', 1)


class Penta2Tile2(Penta2Tile):
    BOUNDARY = dict(
        top=['edge', 'vert'],
        left=['vert-1', 'edge', 'vert-2', 'face', 'split'],
        bottom=['edge', 'vert'],
        right=['vert-1', 'edge', 'vert-2', 'face', 'split']
    )

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'C': None,
                'D': None}

    def calculate_verts(self):
        (v1, v2, v3, v4) = self.v_units()

        self.add_vert(4,
                      1, v1,
                      bottom_boundary='vert')

        self.add_vert(5,
                      1, v2,
                      right_boundary='vert-2')

        self.add_vert(6,
                      0, v3,
                      left_boundary='vert-2')

        self.add_vert(7,
                      0, v4,
                      top_boundary='vert')

    def calculate_faces(self):
        self.add_face('C', [4,
                            5,
                            6,
                            left_boundary('face')])

        self.add_face('D', [7,
                            6,
                            5,
                            right_boundary('face')])

    def color_pattern1(self):
        pass
