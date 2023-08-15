from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# Non-convex pattern. Might work better for 2D than 3D
# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/stanley_park.svg


class StanleyParkTile(Tile):
    BOUNDARY = dict(
        top=['face-1', 'vert', 'face-2'],
        left=['face-1', 'split', 'face-2', 'split', 'face-3'],
        bottom=['face-1', 'vert', 'face-2'],
        right=['face-1', 'split', 'face-2', 'split', 'face-3'],
    )

    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False  # Actually it is though

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None,
                5: None,
                6: None,
                7: None,
                8: None,
                9: None,
                10: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None,
                'F': None}

    def calculate_verts(self):
        self.add_vert(0,
                      7.0 / 12.0, 0,
                      bottom_boundary='vert')

        self.add_vert(1,
                      1.0 / 12.0, 1.0 / 6.0)

        self.add_vert(2,
                      5.0 / 12.0, 1.0 / 6.0)

        self.add_vert(3,
                      7.0 / 12.0, 2.0 / 6.0)

        self.add_vert(4,
                      11.0 / 12.0, 2.0 / 6.0)

        self.add_vert(5,
                      5.0 / 12.0, 0.5)

        self.add_vert(6,
                      1.0 / 12.0, 5.0 / 6.0)

        self.add_vert(7,
                      5.0 / 12.0, 5.0 / 6.0)

        self.add_vert(8,
                      7.0 / 12.0, 4.0 / 6.0)

        self.add_vert(9,
                      11.0 / 12.0, 4.0 / 6.0)

        self.add_vert(10,
                      7.0 / 12.0, 1,
                      top_boundary='vert')

    def calculate_faces(self):
        self.add_face('A', [0,
                            2,
                            1,
                            left_boundary('face-3')])

        self.add_face('B', [4,
                            3,
                            2,
                            0,
                            bottom_boundary('face-2')])

        self.add_face('C', [1,
                            2,
                            3,
                            5,
                            8,
                            7,
                            6,
                            left_boundary('face-2')])

        self.add_face('D', [9,
                            8,
                            5,
                            3,
                            4,
                            right_boundary('face-2')])

        self.add_face('E', [6,
                            7,
                            10,
                            top_boundary('face-2')])

        self.add_face('F', [10,
                            7,
                            8,
                            9,
                            right_boundary('face-3')])

    def color_pattern1(self):
        self.color_face('C', 1)

    def color_pattern2(self):
        if self.fingerprint[0] % 2 == 0:
            self.color_face('A', 1)
            self.color_face('C', 1)
