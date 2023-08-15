from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/weave.svg


class WeaveTile(Tile):
    BOUNDARY = dict(
        top=['face-1', 'split', 'face-2'],
        left=['face-1', 'split', 'face-2'],
        bottom=['face-1', 'split', 'face-2'],
        right=['face-1', 'split', 'face-2'],
    )
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False
        self.square_ratio = kwargs.get('square_ratio', 0.5)


class WeaveTile1(WeaveTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None}

    def calculate_verts(self):
        half_square_size = 0.5 * self.square_ratio
        a1 = 0.5 - half_square_size
        a2 = 0.5 + half_square_size

        self.add_vert(0, a1, a1)
        self.add_vert(1, a2, a1)
        self.add_vert(2, a2, a2)
        self.add_vert(3, a1, a2)

    def calculate_faces(self):
        self.add_face('A', [1,
                            0,
                            left_boundary('face-2')],
                      face_type='oct')

        self.add_face('B', [2,
                            1,
                            bottom_boundary('face-2')],
                      face_type='oct')

        self.add_face('C', [3,
                            2,
                            right_boundary('face-2')],
                      face_type='oct')

        self.add_face('D', [0,
                            3,
                            top_boundary('face-2')],
                      face_type='oct')

        self.add_face('E', [0,
                            1,
                            2,
                            3],
                      face_type='square')

    def color_pattern1(self):
        self.color_face('A', 2)
        self.color_face('B', 1)


class WeaveTile2(WeaveTile):

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'F': None,
                'G': None,
                'H': None,
                'I': None,
                'J': None}

    def calculate_verts(self):
        half_square_size = 0.5 * self.square_ratio
        a1 = 0.5 - half_square_size
        a2 = 0.5 + half_square_size

        self.add_vert(4, a1, a1)
        self.add_vert(5, a2, a1)
        self.add_vert(6, a2, a2)
        self.add_vert(7, a1, a2)

    def calculate_faces(self):
        self.add_face('F', [4,
                            7,
                            left_boundary('face-2')],
                      face_type='oct')

        self.add_face('G', [5,
                            4,
                            bottom_boundary('face-2')],
                      face_type='oct')

        self.add_face('H', [6,
                            5,
                            right_boundary('face-2')],
                      face_type='oct')

        self.add_face('I', [7,
                            6,
                            top_boundary('face-2')],
                      face_type='oct')

        self.add_face('J', [4,
                            5,
                            6,
                            7],
                      face_type='square')

    def color_pattern1(self):
        pass
