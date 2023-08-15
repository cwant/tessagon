from tessagon.core.tile import Tile


class SquareTile(Tile):
    uv_ratio = 1.0

    BOUNDARY = dict(
        top=['vert-1', 'edge', 'vert-2'],
        left=['vert-1', 'edge', 'vert-2'],
        bottom=['vert-1', 'edge', 'vert-2'],
        right=['vert-1', 'edge', 'vert-2']
    )

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None}

    def calculate_verts(self):
        self.add_vert(0,
                      0, 0,
                      left_boundary='vert-2')

        self.add_vert(1,
                      1, 0,
                      bottom_boundary='vert-2')

        self.add_vert(2,
                      1, 1,
                      right_boundary='vert-2')

        self.add_vert(3,
                      0, 1,
                      top_boundary='vert-2')

    def calculate_faces(self):
        self.add_face('A', [0,
                            1,
                            2,
                            3])

    def color_pattern1(self):
        if (self.fingerprint[0] + self.fingerprint[1]) % 2 == 0:
            self.color_face('A', 0)
        else:
            self.color_face('A', 1)

    def color_pattern2(self):
        if (self.fingerprint[0] + self.fingerprint[1]) % 2 == 0:
            self.color_face('A', 0)
        elif self.fingerprint[0] % 2 == 0:
            self.color_face('A', 1)
        else:
            self.color_face('A', 2)

    def color_pattern3(self):
        if (self.fingerprint[0] * self.fingerprint[1]) % 2 == 0:
            self.color_face('A', 0)
        else:
            self.color_face('A', 1)

    def color_pattern4(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('A', 0)
        else:
            if ((self.fingerprint[1] // 2) + self.fingerprint[0]) % 2 == 0:
                self.color_face('A', 0)
            else:
                self.color_face(['A'], 1)

    def color_pattern5(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('A', 0)
        else:
            self.color_face('A', 1)

    def color_pattern6(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('A', 0)
        else:
            if self.fingerprint[0] % 2 == 0:
                self.color_face('A', 1)
            else:
                self.color_face('A', 2)

    def color_pattern7(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face('A', 0)
        else:
            if ((self.fingerprint[1] // 2) + self.fingerprint[0]) % 2 == 0:
                self.color_face('A', 1)
            else:
                self.color_face('A', 2)

    def color_pattern8(self):
        if self.fingerprint[1] % 2 == 0:
            if self.fingerprint[0] % 2 == 0:
                self.color_face('A', 0)
            else:
                self.color_face('A', 1)
        else:
            if self.fingerprint[0] % 2 == 0:
                self.color_face('A', 2)
            else:
                self.color_face('A', 3)
