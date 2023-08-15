from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/dodeca_tri.svg


class DodecaTriTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def u_units(self):
        # u_unit is the length of the edges expressed as a
        # proportion of the tile
        u_unit = 2.0 * (2.0 - sqrt(3))

        u1 = 0
        u2 = 0.5*u_unit
        u3 = 1 - u2
        u4 = 1

        return (u1, u2, u3, u4)

    def v_units(self):
        v_unit = 2.0 / (3.0 + 2.0 * sqrt(3))
        v_h = 0.5*sqrt(3)*v_unit  # height of triangle of side v_unit
        v1 = 0.5*v_unit
        v2 = v1 + v_h
        v3 = 1 - v2
        v4 = 1 - v1

        return (v1, v2, v3, v4)


class DodecaTriTile1(DodecaTriTile):
    BOUNDARY = dict(
        top=['face', 'split'],
        left=['edge', 'vert', 'face-1', 'split', 'face-2'],
        bottom=['face', 'split'],
        right=['edge', 'vert', 'face-1', 'split', 'face-2']
    )

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_verts(self):
        (u1, u2, u3, u4) = self.u_units()
        (v1, v2, v3, v4) = self.v_units()

        self.add_vert(0,
                      u1, v4,
                      left_boundary='vert')

        self.add_vert(1,
                      u2, v3)

        self.add_vert(2,
                      u3, v2)

        self.add_vert(3,
                      u4, v1,
                      right_boundary='vert')

    def calculate_faces(self):
        self.add_face('A', [3,
                            2,
                            1,
                            left_boundary('face-2')])

        self.add_face('B', [1,
                            0,
                            left_boundary('face-1')])

        self.add_face('C', [2,
                            3,
                            right_boundary('face-1')])

        self.add_face('D', [0,
                            1,
                            2,
                            right_boundary('face-2')])

    def color_pattern1(self):
        self.color_face('A', 1)


class DodecaTriTile2(DodecaTriTile):
    BOUNDARY = dict(
        top=['split', 'face'],
        left=['face-1', 'split', 'face-2', 'vert', 'edge'],
        bottom=['split', 'face'],
        right=['face-1', 'split', 'face-2', 'vert', 'edge']
    )

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None}

    def calculate_verts(self):
        (u1, u2, u3, u4) = self.u_units()
        (v1, v2, v3, v4) = self.v_units()

        self.add_vert(4,
                      u1, v1,
                      left_boundary='vert')

        self.add_vert(5,
                      u2, v2)

        self.add_vert(6,
                      u3, v3)

        self.add_vert(7,
                      u4, v4,
                      right_boundary='vert')

    def calculate_faces(self):
        self.add_face('E', [6,
                            5,
                            4,
                            bottom_boundary('face')])

        self.add_face('F', [4,
                            5,
                            left_boundary('face-2')])

        self.add_face('G', [7,
                            6,
                            right_boundary('face-2')])

        self.add_face('H', [5,
                            6,
                            7,
                            top_boundary('face')])

    def color_pattern1(self):
        pass
