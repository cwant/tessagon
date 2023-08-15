from tessagon.core.tile import Tile
from tessagon.core.tile_utils import top_boundary, left_boundary, \
    bottom_boundary, right_boundary

# From: https://gallica.bnf.fr/ark:/12148/btv1b105092395/f12.item
# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/hokusai_hashes.svg


class HokusaiHashesTile(Tile):
    BOUNDARY = dict(
        top=['vert-1', 'face-1', 'split', 'face-2', 'split',
             'face-3', 'split', 'face-4', 'vert-2'],
        left=['vert-1', 'face-1', 'split', 'face-2', 'split',
              'face-3', 'split', 'face-4', 'vert-2'],
        bottom=['vert-1', 'face-1', 'split', 'face-2', 'split',
                'face-3', 'split', 'face-4', 'vert-2'],
        right=['vert-1', 'face-1', 'split', 'face-2', 'split',
               'face-3', 'split', 'face-4', 'vert-2'],
    )
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def init_verts(self):
        return {k: None for k in range(20)}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None,
                'F': None,
                'G': None,
                'H': None,
                'I': None,
                'J': None}

    def transform_vert(self, x, y):
        # Switch from the axis aligned easy coords, to the
        # rotated non-easy coords
        # e.g, (4, 1) --> (1, 0)
        #      (-1, 4) --> (0, 1)
        return [x * 4/17 + y * 1/17, x * (-1/17) + y * 4/17]

    def calculate_verts(self):
        self.add_vert(0,
                      0, 0,
                      boundary_left='vert-2')
        self.add_vert(1,
                      *self.transform_vert(1, 1))
        self.add_vert(2,
                      *self.transform_vert(2, 1))
        self.add_vert(3,
                      *self.transform_vert(3, 1))
        self.add_vert(4,
                      1, 0,
                      boundary_bottom='vert-2')
        self.add_vert(5,
                      *self.transform_vert(3, 2))
        self.add_vert(6,
                      *self.transform_vert(3, 3))
        self.add_vert(7,
                      *self.transform_vert(3, 4))
        self.add_vert(8,
                      1, 1,
                      boundary_right='vert-2')
        self.add_vert(9,
                      *self.transform_vert(2, 4))
        self.add_vert(10,
                      *self.transform_vert(1, 4))
        self.add_vert(11,
                      *self.transform_vert(0, 4))
        self.add_vert(12,
                      0, 1,
                      boundary_top='vert-2')
        self.add_vert(13,
                      *self.transform_vert(0, 3))
        self.add_vert(14,
                      *self.transform_vert(0, 2))
        self.add_vert(15,
                      *self.transform_vert(0, 1))

        self.add_vert(16,
                      *self.transform_vert(1, 2))
        self.add_vert(17,
                      *self.transform_vert(2, 2))
        self.add_vert(18,
                      *self.transform_vert(2, 3))
        self.add_vert(19,
                      *self.transform_vert(1, 3))

    def calculate_faces(self):
        self.add_face('A', [15,
                            0,
                            bottom_boundary('face-1'),
                            1,
                            2,
                            bottom_boundary('face-3'),
                            3,
                            4,
                            right_boundary('face-1'),
                            5,
                            6,
                            right_boundary('face-3'),
                            7,
                            8,
                            top_boundary('face-1'),
                            9,
                            10,
                            top_boundary('face-3'),
                            11,
                            12,
                            left_boundary('face-1'),
                            13,
                            14,
                            left_boundary('face-3')],
                      face_type='hash')

        self.add_face('B', [2,
                            1,
                            bottom_boundary('face-2')],
                      face_type='hash',
                      indirect=True)

        self.add_face('C', [4,
                            3,
                            bottom_boundary('face-4')],
                      face_type='hash',
                      indirect=True)

        self.add_face('D', [6,
                            5,
                            right_boundary('face-2')],
                      face_type='hash',
                      indirect=True)

        self.add_face('E', [8,
                            7,
                            right_boundary('face-4')],
                      face_type='hash',
                      indirect=True)

        self.add_face('F', [10,
                            9,
                            top_boundary('face-2')],
                      face_type='hash',
                      indirect=True)

        self.add_face('G', [12,
                            11,
                            top_boundary('face-4')],
                      face_type='hash',
                      indirect=True)

        self.add_face('H', [14,
                            13,
                            left_boundary('face-2')],
                      face_type='hash',
                      indirect=True)

        self.add_face('I', [0,
                            15,
                            left_boundary('face-4')],
                      face_type='hash',
                      indirect=True)

        self.add_face('J', [16,
                            17,
                            18,
                            19],
                      face_type='square')

    def color_pattern1(self):
        self.color_face('J', 1)

    def color_pattern2(self):
        if (self.fingerprint[0] + self.fingerprint[1]) % 2 == 0:
            self.color_face('J', 1)
        else:
            self.color_face('A', 1)
