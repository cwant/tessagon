from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/dodeca.svg


class DodecaTile(Tile):
    BOUNDARY = dict(
        top=['face-1', 'split', 'face-2'],
        left=['face-1', 'split', 'face-2', 'split', 'face-3'],
        bottom=['face-1', 'split', 'face-2'],
        right=['face-1', 'split', 'face-2', 'split', 'face-3']
    )

    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def u_units(self):
        # u_unit is the length of the edges expressed as a
        # proportion of the tile
        u_unit = 2.0 / (3.0 + sqrt(3))

        u1 = 0.5*u_unit
        u2 = u_unit
        u3 = 1 - u2
        u4 = 1 - u1

        return (u1, u2, u3, u4)

    def v_units(self):
        v_unit = 2.0 / (3.0*(1.0 + sqrt(3)))
        v_h = 0.5*sqrt(3)*v_unit  # height of triangle of side v_unit
        v1 = 0.5*v_unit
        v2 = v1 + v_h
        v3 = v_unit + v_h
        v4 = 1 - v3
        v5 = 1 - v2
        v6 = 1 - v1

        return (v1, v2, v3, v4, v5, v6)


class DodecaTile1(DodecaTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None,
                5: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None,
                'F': None,
                'G': None}

    def calculate_verts(self):
        (u1, u2, u3, u4) = self.u_units()
        (v1, v2, v3, v4, v5, v6) = self.v_units()

        self.add_vert(0, u1, v3)
        self.add_vert(1, u3, v2)
        self.add_vert(2, u4, v1)
        self.add_vert(3, u1, v6)
        self.add_vert(4, u2, v5)
        self.add_vert(5, u4, v4)

    def calculate_faces(self):
        self.add_face('A', [2,
                            1,
                            0,
                            left_boundary('face-3')])

        self.add_face('B', [0,
                            4,
                            3,
                            left_boundary('face-2')])

        self.add_face('C', [0,
                            1,
                            5,
                            4])

        self.add_face('D', [5,
                            1,
                            2,
                            right_boundary('face-2')])

        self.add_face('E', [2,
                            bottom_boundary('face-2')])

        self.add_face('F', [3,
                            top_boundary('face-2')])

        self.add_face('G', [3,
                            4,
                            5,
                            right_boundary('face-3')])

    def color_pattern1(self):
        self.color_face('A', 1)
        self.color_face('B', 2)
        self.color_face('D', 2)


class DodecaTile2(DodecaTile):

    def init_verts(self):
        return {6: None,
                7: None,
                8: None,
                9: None,
                10: None,
                11: None}

    def init_faces(self):
        return {'H': None,
                'I': None,
                'J': None,
                'K': None,
                'L': None,
                'M': None,
                'N': None}

    def calculate_verts(self):
        (u1, u2, u3, u4) = self.u_units()
        (v1, v2, v3, v4, v5, v6) = self.v_units()

        self.add_vert(6, u1, v1)
        self.add_vert(7, u2, v2)
        self.add_vert(8, u4, v3)
        self.add_vert(9, u1, v4)
        self.add_vert(10, u3, v5)
        self.add_vert(11, u4, v6)

    def calculate_faces(self):
        self.add_face('H', [6,
                            left_boundary('face-3')])

        self.add_face('I', [8,
                            7,
                            6,
                            bottom_boundary('face-2')])

        self.add_face('J', [6,
                            7,
                            9,
                            left_boundary('face-2')])

        self.add_face('K', [7,
                            8,
                            10,
                            9])

        self.add_face('L', [11,
                            10,
                            8,
                            right_boundary('face-2')])

        self.add_face('M', [9,
                            10,
                            11,
                            top_boundary('face-2')])

        self.add_face('N', [11,
                            right_boundary('face-3')])

    def color_pattern1(self):
        pass
