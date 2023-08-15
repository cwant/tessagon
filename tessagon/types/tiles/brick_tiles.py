from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/brick.svg


class BrickTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class BrickTile1(BrickTile):
    BOUNDARY = dict(
        top=['edge', 'vert', 'face'],
        left=['face', 'split'],
        bottom=['edge', 'vert', 'face'],
        right=['face', 'split']
    )

    def init_verts(self):
        return {0: None,
                1: None}

    def init_faces(self):
        return {'A': None,
                'B': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0.5, 0.0,
                      bottom_boundary='vert')

        self.add_vert(1,
                      0.5, 1.0,
                      top_boundary='vert')

    def calculate_faces(self):
        self.add_face('A',
                      [0,
                       1,
                       top_boundary('face')])
        self.add_face('B',
                      [1,
                       0,
                       bottom_boundary('face')])

    def color_pattern1(self):
        if (self.fingerprint[0] % 2) == 0:
            self.color_face('A', 1)
        else:
            self.color_face('B', 1)


class BrickTile2(BrickTile):
    BOUNDARY = dict(
        top=['face', 'vert', 'edge'],
        left=['split', 'face'],
        bottom=['face', 'vert', 'edge'],
        right=['split', 'face']
    )

    def init_verts(self):
        return {2: None,
                3: None}

    def init_faces(self):
        return {'C': None,
                'D': None}

    def calculate_verts(self):
        self.add_vert(2,
                      0.5, 0.0,
                      bottom_boundary='vert')

        self.add_vert(3,
                      0.5, 1.0,
                      top_boundary='vert')

    def calculate_faces(self):
        self.add_face('C',
                      [2,
                       3,
                       left_boundary('face')])

        self.add_face('D',
                      [3,
                       2,
                       right_boundary('face')])

    def color_pattern1(self):
        pass
