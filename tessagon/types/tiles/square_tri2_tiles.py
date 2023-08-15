from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/square_tri2.svg


class SquareTri2Tile(Tile):
    uv_ratio = 1.0 / (2.0 + sqrt(3.0))

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def v_units(self):
        v_unit = 2.0 / (2.0 + sqrt(3.0))
        v1 = v_unit * 0.5
        v2 = 1.0 - v1

        return (v1, v2)


class SquareTri2Tile1(SquareTri2Tile):
    BOUNDARY = dict(
        top=['face', 'split'],
        left=['edge', 'vert', 'face-1', 'split', 'face-2'],
        bottom=['face', 'split'],
        right=['edge', 'vert', 'face-1', 'split', 'face-2']
    )

    def init_verts(self):
        return {0: None,
                1: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_verts(self):
        (v1, v2) = self.v_units()

        self.add_vert(0,
                      1.0, v1,
                      right_boundary='vert')

        self.add_vert(1,
                      0.0, v2,
                      left_boundary='vert')

    def calculate_faces(self):
        self.add_face('A', [0,
                            left_boundary('face-2')],
                      face_type='square')

        self.add_face('B', [0,
                            1,
                            left_boundary('face-1')],
                      face_type='triangle')

        self.add_face('C', [1,
                            0,
                            right_boundary('face-1')],
                      face_type='triangle')

        self.add_face('D', [1,
                            right_boundary('face-2')],
                      face_type='square')

    def color_pattern1(self):
        self.color_face('A', 1)


class SquareTri2Tile2(SquareTri2Tile):
    BOUNDARY = dict(
        top=['split', 'face'],
        left=['face-1', 'split', 'face-2', 'vert', 'edge'],
        bottom=['split', 'face'],
        right=['face-1', 'split', 'face-2', 'vert', 'edge']
    )

    def init_verts(self):
        return {2: None,
                3: None}

    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None}

    def calculate_verts(self):
        (v1, v2) = self.v_units()

        self.add_vert(2,
                      0.0, v1,
                      left_boundary='vert')

        self.add_vert(3,
                      1.0, v2,
                      right_boundary='vert')

    def calculate_faces(self):
        self.add_face('E', [2,
                            bottom_boundary('face')],
                      face_type='square')

        self.add_face('F', [3,
                            2,
                            right_boundary('face-2')],
                      face_type='triangle')

        self.add_face('G', [2,
                            3,
                            left_boundary('face-2')],
                      face_type='triangle')

        self.add_face('H', [3,
                            top_boundary('face')],
                      face_type='square')

    def color_pattern1(self):
        pass
