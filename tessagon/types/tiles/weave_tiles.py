from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/weave.svg


class WeaveTile(Tile):
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
                            left_tile(5),
                            left_tile(4),
                            bottom_left_tile(3),
                            bottom_left_tile(2),
                            bottom_tile(7),
                            bottom_tile(6)],
                      equivalent=[left_tile('G'),
                                  bottom_left_tile('C'),
                                  bottom_tile('I')],
                      face_type='oct')

        self.add_face('B', [2,
                            1,
                            bottom_tile(6),
                            bottom_tile(5),
                            bottom_right_tile(0),
                            bottom_right_tile(3),
                            right_tile(4),
                            right_tile(7)],
                      equivalent=[bottom_tile('H'),
                                  bottom_right_tile('D'),
                                  right_tile('F')],
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
        self.add_face('J', [4,
                            5,
                            6,
                            7],
                      face_type='square')

    def color_pattern1(self):
        pass
