from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile
from tessagon.core.tessagon_metadata import TessagonMetadata
from math import atan2, sqrt, sin, cos

metadata = TessagonMetadata(name='Big Hexagons and Triangles',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['hexagons', 'triangles'],
                            sides=[6, 3])


class BigHexTriTile(Tile):
    #  See the SVG for decomposition:
    # https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/big_hex_tri.svg

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
                14: None}


    def init_faces(self):
        return {
            # Hex
            'a': None,
            'b': None,
            'c': None,

            # Triangles
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
            17: None,
            18: None,
            19: None,
            20: None,
            21: None,
            22: None,
            23: None,
            24: None}

    def transform(self, x0, y0):
        # set t=1, see SVG
        x1 = 0.5 * sqrt(3) * x0
        y1 = y0
        theta = -atan2(0.5, 1.5*sqrt(3))
        x2 = cos(theta) * x1 - sin(theta) * y1
        y2 = sin(theta) * x1 + cos(theta) * y1
        x3 = x2 / sqrt(7)
        y3 = y2 / sqrt(21)

        return (x3, y3)
       
    def calculate_verts(self):
        vert = self.add_vert([0], 0, 1)
        self.set_equivalent_vert(['left'], 1, vert)
        self.set_equivalent_vert(['top'], 13, vert)
        self.set_equivalent_vert(['left', 'top'], 14, vert)

        vert = self.add_vert([1], 1, 1)
        self.set_equivalent_vert(['right'], 0, vert)
        self.set_equivalent_vert(['top'], 14, vert)
        self.set_equivalent_vert(['right', 'top'], 13, vert)

        self.add_vert([2], *self.transform(1, 4.5))
        self.add_vert([3], *self.transform(0, 4))
        self.add_vert([4], *self.transform(1, 3.5))
        self.add_vert([5], *self.transform(0, 3))
        self.add_vert([6], *self.transform(2, 3))
        self.add_vert([7], .5, .5)
        self.add_vert([8], *self.transform(0, 2))
        self.add_vert([9], *self.transform(2, 2))
        self.add_vert([10], *self.transform(0, 1))
        self.add_vert([11], *self.transform(2, 1))
        self.add_vert([12], *self.transform(1, 0.5))

        vert = self.add_vert([13], 0, 0)
        self.set_equivalent_vert(['left'], 14, vert)
        self.set_equivalent_vert(['bottom'], 0, vert)
        self.set_equivalent_vert(['left', 'bottom'], 1, vert)

        vert = self.add_vert([14], 1, 0)
        self.set_equivalent_vert(['right'], 13, vert)
        self.set_equivalent_vert(['bottom'], 1, vert)
        self.set_equivalent_vert(['right', 'bottom'], 0, vert)

    def calculate_faces(self):
        face = self.add_face(0, [3,
                                 0,
                                 [['top'], 12]])
        self.set_equivalent_face(['top'], 23, face)

        face = self.add_face(1, [2,
                                 3,
                                 [['top'], 12]])
        self.set_equivalent_face(['top'], 24, face)

        face = self.add_face(2, [2,
                                 [['top'], 12],
                                 [['top'], 11]])
        self.set_equivalent_face(['top'], 21, face)

        face = self.add_face(3, [1,
                                 2,
                                 [['top'], 11]])
        self.set_equivalent_face(['top'], 22, face)

        self.add_face(4, [3,
                          2,
                          4])
        self.add_face(5, [3,
                          4,
                          5])
        self.add_face(6, [4,
                          7,
                          5])
        self.add_face(7, [4,
                          6,
                          7])

        face = self.add_face(8, [6,
                                 [['right'], 5],
                                 [['right'], 8]])
        self.set_equivalent_face(['right'], 9, face)

        face = self.add_face(9, [5,
                                 8,
                                 [['left'], 6]])
        self.set_equivalent_face(['left'], 8, face)

        self.add_face(10, [7,
                          8,
                          5])
        self.add_face(11, [6,
                           9,
                           7])

        face = self.add_face(12, [9,
                                  6,
                                  [['right'], 8]])
        self.set_equivalent_face(['right'], 13, face)

        face = self.add_face(13, [8,
                                  [['left'], 9],
                                  [['left'], 6]])
        self.set_equivalent_face(['left'], 12, face)

        face = self.add_face(14, [9,
                                  [['right'], 8],
                                  [['right'], 10]])
        self.set_equivalent_face(['right'], 15, face)

        face = self.add_face(15, [8,
                                  10,
                                  [['left'], 9]])
        self.set_equivalent_face(['left'], 14, face)

        face = self.add_face(16, [11,
                                  9,
                                  [['right'], 10]])
        self.set_equivalent_face(['right'], 17, face)

        face = self.add_face(17, [10,
                                  [['left'], 9],
                                  [['left'], 11]])
        self.set_equivalent_face(['left'], 16, face)

        face = self.add_face(18, [14,
                                  11,
                                  [['right'], 10]])
        self.set_equivalent_face(['right'], 19, face)

        face = self.add_face(19, [10,
                                  13,
                                  [['left'], 11]])
        self.set_equivalent_face(['left'], 18, face)

        self.add_face(20, [10,
                           12,
                           13])

        face = self.add_face(21, [12,
                                  11,
                                  [['bottom'], 2]])
        self.set_equivalent_face(['bottom'], 2, face)

        face = self.add_face(22, [11,
                                  14,
                                  [['bottom'], 2]])
        self.set_equivalent_face(['bottom'], 3, face)

        face = self.add_face(23, [13,
                                  12,
                                  [['bottom'], 3]])
        self.set_equivalent_face(['bottom'], 0, face)

        face = self.add_face(24, [12,
                                  [['bottom'], 2],
                                  [['bottom'], 3]])
        self.set_equivalent_face(['bottom'], 1, face)

        face = self.add_face('a', [0,
                                   3,
                                   5,
                                   [['left'], 6],
                                   [['left'], 4],
                                   [['left'], 2]])
        self.set_equivalent_face(['left'], 'b', face)

        face = self.add_face('b', [6,
                                   4,
                                   2,
                                   1,
                                   [['right'], 3],
                                   [['right'], 5]])
        self.set_equivalent_face(['right'], 'a', face)

        self.add_face('c', [7,
                            9,
                            11,
                            12,
                            10,
                            8])

    def color_pattern1(self):
        self.color_face(0, 0)
        self.color_face(1, 1)
        self.color_face(2, 0)
        self.color_face(3, 1)
        self.color_face(4, 0)
        self.color_face(5, 1)
        self.color_face(6, 0)
        self.color_face(7, 1)
        self.color_face(8, 0)
        self.color_face(9, 0)
        self.color_face(10, 1)
        self.color_face(11, 0)
        self.color_face(12, 1)
        self.color_face(13, 1)
        self.color_face(14, 0)
        self.color_face(15, 0)

        self.color_face(16, 1)
        self.color_face(17, 1)
        self.color_face(18, 0)
        self.color_face(19, 0)
        self.color_face(20, 1)

        self.color_face(21, 0)
        self.color_face(22, 1)
        self.color_face(23, 0)
        self.color_face(24, 1)

        self.color_face('a', 2)
        self.color_face('b', 2)
        self.color_face('c', 2)

class BigHexTriTessagon(Tessagon):
    tile_class = BigHexTriTile
    metadata = metadata
