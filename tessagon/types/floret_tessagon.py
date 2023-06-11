from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile
from tessagon.core.tessagon_metadata import TessagonMetadata
from math import atan2, sqrt, sin, cos

metadata = TessagonMetadata(name='Florets',
                            num_color_patterns=3,
                            classification='laves',
                            shapes=['pentagons'],
                            sides=[5],
                            uv_ratio=1.0/sqrt(3))


class FloretTile(Tile):
    #  See the SVG for decomposition:
    # https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/floret.svg

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
                7: None,
                8: None,
                9: None,
                10: None,
                11: None,
                12: None,
                13: None,
                14: None,
                15: None,
                16: None,
                17: None,
                18: None,
                19: None,
                20: None,
                21: None,
                22: None}

    def init_faces(self):
        return {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None}

    def transform(self, x0, y0):
        # set t=1, see SVG
        x1 = x0
        y1 = 0.5 * sqrt(3) * y0
        theta = -atan2(0.5*sqrt(3), 4.5)
        x2 = cos(theta) * x1 - sin(theta) * y1
        y2 = sin(theta) * x1 + cos(theta) * y1
        x3 = x2 / sqrt(21)
        y3 = y2 / (3 * sqrt(7))

        return (x3, y3)

    def calculate_verts(self):
        vert = self.add_vert([0], 0, 1)
        self.set_equivalent_vert(['left'], 1, vert)
        self.set_equivalent_vert(['top'], 21, vert)
        self.set_equivalent_vert(['left', 'top'], 22, vert)

        vert = self.add_vert([1], 1, 1)
        self.set_equivalent_vert(['right'], 0, vert)
        self.set_equivalent_vert(['top'], 22, vert)
        self.set_equivalent_vert(['right', 'top'], 21, vert)

        self.add_vert([2], *self.transform(0.5, 9))
        self.add_vert([3], *self.transform(1, 8))
        self.add_vert([4], *self.transform(2, 8))
        self.add_vert([5], *self.transform(-0.5, 7))
        self.add_vert([6], *self.transform(0.5, 7))
        self.add_vert([7], *self.transform(2.5, 7))

        vert = self.add_vert([8], *self.transform(3.5, 7))
        self.set_equivalent_vert(['right'], 9, vert)

        vert = self.add_vert([9], *self.transform(-1, 6))
        self.set_equivalent_vert(['left'], 8, vert)

        self.add_vert([10], *self.transform(-0.5, 5))
        self.add_vert([11], 0.5, 0.5)
        self.add_vert([12], *self.transform(3.5, 5))

        vert = self.add_vert([13], *self.transform(4, 4))
        self.set_equivalent_vert(['right'], 14, vert)

        vert = self.add_vert([14], *self.transform(-0.5, 3))
        self.set_equivalent_vert(['left'], 13, vert)

        self.add_vert([15], *self.transform(0.5, 3))
        self.add_vert([16], *self.transform(2.5, 3))
        self.add_vert([17], *self.transform(3.5, 3))
        self.add_vert([18], *self.transform(1, 2))
        self.add_vert([19], *self.transform(2, 2))
        self.add_vert([20], *self.transform(2.5, 1))

        vert = self.add_vert([21], 0, 0)
        self.set_equivalent_vert(['left'], 22, vert)
        self.set_equivalent_vert(['bottom'], 0, vert)
        self.set_equivalent_vert(['left', 'bottom'], 1, vert)

        vert = self.add_vert([22], 1, 0)
        self.set_equivalent_vert(['right'], 21, vert)
        self.set_equivalent_vert(['bottom'], 1, vert)
        self.set_equivalent_vert(['right', 'bottom'], 0, vert)

    def calculate_faces(self):
        face = self.add_face(0, [2,
                                 0,
                                 [['top'], 18],
                                 [['top'], 19],
                                 [['top'], 20]])
        self.set_equivalent_face(['top'], 16, face)

        face = self.add_face(1, [1,
                                 4,
                                 3,
                                 2,
                                 [['top'], 20]])
        self.set_equivalent_face(['top'], 17, face)

        self.add_face(2, [0,
                          2,
                          3,
                          6,
                          5])

        face = self.add_face(3, [0,
                                 5,
                                 9,
                                 [['left'], 7],
                                 [['left'], 4]])
        self.set_equivalent_face(['left'], 4, face)

        face = self.add_face(4, [8,
                                 7,
                                 4,
                                 1,
                                 [['right'], 5]])
        self.set_equivalent_face(['right'], 3, face)

        self.add_face(5, [5,
                          6,
                          11,
                          10,
                          9])
        self.add_face(6, [3,
                          4,
                          7,
                          11,
                          6])

        face = self.add_face(7, [12,
                                 11,
                                 7,
                                 8,
                                 [['right'], 10]])
        self.set_equivalent_face(['right'], 8, face)

        face = self.add_face(8, [9,
                                 10,
                                 [['left'], 12],
                                 [['left'], 11],
                                 [['left'], 7]])
        self.set_equivalent_face(['left'], 7, face)

        face = self.add_face(9, [13,
                                 12,
                                 [['right'], 10],
                                 [['right'], 11],
                                 [['right'], 15]])
        self.set_equivalent_face(['right'], 10, face)

        face = self.add_face(10, [10,
                                  11,
                                  15,
                                  14,
                                  [['left'], 12]])
        self.set_equivalent_face(['left'], 9, face)

        self.add_face(11, [11,
                           16,
                           19,
                           18,
                           15])
        self.add_face(12, [11,
                           12,
                           13,
                           17,
                           16])

        face = self.add_face(13, [14,
                                  15,
                                  18,
                                  21,
                                  [['left'], 17]])
        self.set_equivalent_face(['left'], 14, face)

        face = self.add_face(14, [22,
                                  17,
                                  13,
                                  [['right'], 15],
                                  [['right'], 18]])
        self.set_equivalent_face(['right'], 13, face)

        self.add_face(15, [22,
                           20,
                           19,
                           16,
                           17])

        face = self.add_face(16, [21,
                                  18,
                                  19,
                                  20,
                                  [['bottom'], 2]])
        self.set_equivalent_face(['bottom'], 0, face)

        face = self.add_face(17, [20,
                                  22,
                                  [['bottom'], 4],
                                  [['bottom'], 3],
                                  [['bottom'], 2]])
        self.set_equivalent_face(['bottom'], 1, face)

    def floret_fingerprint(self, face):
        fingerprint = list(self.fingerprint.copy())
        fingerprint[0] += fingerprint[1]
        if face in [8, 13, 16]:
            fingerprint[0] -= 1
        elif face in [1, 4, 9]:
            fingerprint[0] += 1

        fingerprint[1] *= 2
        if face in [0, 1, 2, 3, 4]:
            fingerprint[1] += 1
        elif face in [13, 14, 15, 16, 17]:
            fingerprint[1] -= 1

        return fingerprint

    def color_pattern1(self):
        pattern = [0, 0, 1]

        for face in self.faces:
            fingerprint = self.floret_fingerprint(face)
            offset = (fingerprint[0] + fingerprint[1]) % 3
            self.color_face(face, pattern[offset])

    def color_pattern2(self):
        for face in self.faces:
            fingerprint = self.floret_fingerprint(face)
            color = (fingerprint[0] + fingerprint[1]) % 3
            self.color_face(face, color)

    def color_pattern3(self):
        # Follow a straight line in the pattern to see this ...
        pattern = [[2, 0, 2, 2, 0, 2],
                   [2, 1, 2, 0, 0, 0]]

        for face in self.faces:
            fingerprint = self.floret_fingerprint(face)
            row = fingerprint[1] % 2
            column = (fingerprint[0] - 2 * fingerprint[1]) % 6
            self.color_face(face, pattern[row][column])


class FloretTessagon(Tessagon):
    tile_class = FloretTile
    metadata = metadata
