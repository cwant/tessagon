from tessagon.core.tile import Tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/dissected_square.svg


class DissectedSquareTile(Tile):
    BOUNDARY = dict(
        top=['vert-1', 'edge', 'vert-2'],
        left=['vert-1', 'edge', 'vert-2'],
        bottom=['vert-1', 'edge', 'vert-2'],
        right=['vert-1', 'edge', 'vert-2']
    )

    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


class DissectedSquareTile1(DissectedSquareTile):

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0, 0,
                      left_boundary='vert-2')

        self.add_vert(1,
                      1, 0,
                      bottom_boundary='vert-2')

        self.add_vert(2,
                      0, 1,
                      top_boundary='vert-2')

        self.add_vert(3,
                      1, 1,
                      right_boundary='vert-2')

    def calculate_faces(self):
        self.add_face('A',
                      [0, 3, 2])

        self.add_face('B',
                      [0, 1, 3])

    def color_pattern1(self):
        if self.fingerprint[0] % 2 == 0:
            self.color_face('A', 1)
        else:
            self.color_face('B', 1)

    def color_pattern2(self):
        fingerprint = (self.fingerprint[0] - self.fingerprint[1]) % 8

        if fingerprint == 0:
            self.color_face('A', 1)
            self.color_face('B', 1)
        elif fingerprint == 2:
            self.color_face('B', 1)
        elif fingerprint == 6:
            self.color_face('A', 1)


class DissectedSquareTile2(DissectedSquareTile):

    def init_verts(self):
        return {4: None,
                5: None,
                6: None,
                7: None}

    def init_faces(self):
        return {'C': None,
                'D': None}

    def calculate_verts(self):
        self.add_vert(4,
                      0, 0,
                      left_boundary='vert-2')

        self.add_vert(5,
                      1, 0,
                      bottom_boundary='vert-2')

        self.add_vert(6,
                      0, 1,
                      top_boundary='vert-2')

        self.add_vert(7,
                      1, 1,
                      right_boundary='vert-2')

    def calculate_faces(self):
        self.add_face('C',
                      [4, 5, 6])

        self.add_face('D',
                      [5, 7, 6])

    def color_pattern1(self):
        if self.fingerprint[0] % 2 == 0:
            self.color_face('D', 1)
        else:
            self.color_face('C', 1)

    def color_pattern2(self):
        fingerprint = (self.fingerprint[1] + self.fingerprint[0]) % 8

        if fingerprint == 1:
            self.color_face('D', 1)
        elif fingerprint == 5:
            self.color_face('C', 1)
        elif fingerprint == 7:
            self.color_face('C', 1)
            self.color_face('D', 1)
