from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# ^  ..o-o..
# |  ./...\.
# |  o.....o
# |  |.....|
# |  o.....o
# |  .\.../.
#    ..o-o..
# V
#    U ---->


class OctaTile(Tile):
    uv_ratio = 1.0

    BOUNDARY = dict(
        top=['face-1', 'vert-1', 'edge', 'vert-2', 'face-2'],
        left=['face-1', 'vert-1', 'edge', 'vert-2', 'face-2'],
        bottom=['face-1', 'vert-1', 'edge', 'vert-2', 'face-2'],
        right=['face-1', 'vert-1', 'edge', 'vert-2', 'face-2']
    )

    CORNER_TO_VERT_RATIO = 1.0 / (2.0 + sqrt(2))

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None,
                4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None}

    def calculate_verts(self):
        self.add_vert(0,
                      self.CORNER_TO_VERT_RATIO, 0.0,
                      bottom_boundary='vert-1')
        self.add_vert(1,
                      1.0 - self.CORNER_TO_VERT_RATIO, 0.0,
                      bottom_boundary='vert-2')
        self.add_vert(2,
                      1.0, self.CORNER_TO_VERT_RATIO,
                      right_boundary='vert-1')
        self.add_vert(3,
                      1.0, 1.0 - self.CORNER_TO_VERT_RATIO,
                      right_boundary='vert-2')
        self.add_vert(4,
                      1.0 - self.CORNER_TO_VERT_RATIO, 1.0,
                      top_boundary='vert-1')
        self.add_vert(5,
                      self.CORNER_TO_VERT_RATIO, 1,
                      top_boundary='vert-2')
        self.add_vert(6,
                      0.0, 1.0 - self.CORNER_TO_VERT_RATIO,
                      left_boundary='vert-1')
        self.add_vert(7,
                      0.0, self.CORNER_TO_VERT_RATIO,
                      left_boundary='vert-2')

    def calculate_faces(self):
        self.add_face('A',
                      [0,
                       1,
                       2,
                       3,
                       4,
                       5,
                       6,
                       7])

        self.add_face('B',
                      [0,
                       7,
                       left_boundary('face-2')])

        self.add_face('C',
                      [2,
                       1,
                       bottom_boundary('face-2')])

        self.add_face('D',
                      [4,
                       3,
                       right_boundary('face-2')])

        self.add_face('E',
                      [6,
                       5,
                       top_boundary('face-2')])

    def color_pattern1(self):
        self.color_face('A', 1)
