from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/penta.svg


class PentaTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def units(self):
        # unit is the length of the edges expressed as a
        # proportion of the tile
        unit = 2.0 / (1.0 + sqrt(3))

        a1 = unit / (2 * sqrt(3))
        a2 = 1.0 - a1

        return (a1, a2)


class PentaTile1(PentaTile):
    BOUNDARY = dict(
        top=['split', 'face', 'vert', 'edge'],
        left=['split', 'face', 'vert', 'edge'],
        bottom=['split', 'face', 'vert', 'edge'],
        right=['split', 'face', 'vert', 'edge']
    )

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_verts(self):
        (a1, a2) = self.units()

        self.add_vert(0,
                      0, a1,
                      left_boundary='vert')

        self.add_vert(1,
                      a2, 0,
                      bottom_boundary='vert')

        self.add_vert(2,
                      1, a2,
                      right_boundary='vert')

        self.add_vert(3,
                      a1, 1,
                      top_boundary='vert')

        self.add_vert(4,
                      0.5, 0.5)

    def calculate_faces(self):
        self.add_face('A', [1,
                            4,
                            0,
                            bottom_boundary('face')])

        self.add_face('B', [2,
                            4,
                            1,
                            right_boundary('face')])

        self.add_face('C', [3,
                            4,
                            2,
                            top_boundary('face')])

        self.add_face('D', [0,
                            4,
                            3,
                            left_boundary('face')])

    def color_pattern1(self):
        if self.fingerprint[0] % 2 == 0 and \
           self.fingerprint[1] % 2 == 0:
            self.color_face('A', 1)
            self.color_face('B', 1)
            self.color_face('C', 1)
            self.color_face('D', 1)


class PentaTile2(PentaTile):
    BOUNDARY = dict(
        top=['edge', 'vert', 'face', 'split'],
        left=['edge', 'vert', 'face', 'split'],
        bottom=['edge', 'vert', 'face', 'split'],
        right=['edge', 'vert', 'face', 'split']
    )

    def init_verts(self):
        return {5: None,
                6: None,
                7: None,
                8: None,
                9: None}

    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None}

    def calculate_verts(self):
        (a1, a2) = self.units()

        self.add_vert(5,
                      0, a2,
                      left_boundary='vert')

        self.add_vert(6,
                      a1, 0,
                      bottom_boundary='vert')

        self.add_vert(7,
                      1, a1,
                      right_boundary='vert')

        self.add_vert(8,
                      a2, 1,
                      top_boundary='vert')

        self.add_vert(9,
                      0.5, 0.5)

    def calculate_faces(self):
        self.add_face('E', [7,
                            9,
                            6,
                            bottom_boundary('face')])

        self.add_face('F', [8,
                            9,
                            7,
                            right_boundary('face')])

        self.add_face('G', [5,
                            9,
                            8,
                            top_boundary('face')])

        self.add_face('H', [6,
                            9,
                            5,
                            left_boundary('face')])

    def color_pattern1(self):
        pass
