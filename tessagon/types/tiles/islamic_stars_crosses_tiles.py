from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary

# See page 9 of "Islamic Design" by Daud Sutton

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/islamic_stars_crosses.svg


class IslamicStarsCrossesTile(Tile):
    BOUNDARY = dict(
        top=['face', 'vert'],
        left=['vert', 'face'],
        bottom=['face', 'vert'],
        right=['vert', 'face']
    )
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class IslamicStarsCrossesTile1(IslamicStarsCrossesTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None}

    def init_faces(self):
        return {'A': None,
                'B': None}

    def calculate_verts(self):
        c = 2.0 / (2 * (sqrt(2) + 1))
        a = c / sqrt(2)

        self.add_vert(0,
                      1.0, 0.0,
                      bottom_boundary='vert')

        self.add_vert(1,
                      1.0 - a, a)

        self.add_vert(2,
                      a, a)

        self.add_vert(3,
                      a, 1.0 - a)

        self.add_vert(4,
                      0.0, 1.0,
                      top_boundary='vert')

    def calculate_faces(self):
        self.add_face('A',
                      [0,
                       1,
                       2,
                       3,
                       4,
                       left_boundary('face')],
                      face_type='cross')

        # Top left cross
        self.add_face('B',
                      [4,
                       3,
                       2,
                       1,
                       0,
                       right_boundary('face')],
                      face_type='star')

    def color_pattern1(self):
        self.color_face('A', 1)


class IslamicStarsCrossesTile2(IslamicStarsCrossesTile1):
    rotate = 90


class IslamicStarsCrossesTile3(IslamicStarsCrossesTile1):
    rotate = 180


class IslamicStarsCrossesTile4(IslamicStarsCrossesTile1):
    rotate = 270
