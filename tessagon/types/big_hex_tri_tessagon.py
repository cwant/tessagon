from math import atan2, sqrt, sin, cos, pi
from tessagon.core.tessagon import Tessagon
from tessagon.core.alternating_tile import AlternatingTile
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import right_tile, left_tile, \
    top_tile, top_left_tile, bottom_tile

metadata = TessagonMetadata(name='Big Hexagons and Triangles',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['hexagons', 'triangles'],
                            sides=[6, 3],
                            uv_ratio=1.0/sqrt(3),
                            extra_parameters={
                                'hexagon_ratio': {
                                    'type': 'float',
                                    'min': 0.0,
                                    # Any higher than 0.70, and verts are
                                    # pushed to neighboring tiles
                                    'max': 0.70,
                                    'default': 0.5,
                                    'description':
                                    'Control the size of the Hexagons'
                                }
                            })


class BigHexTriTile(AlternatingTile):
    #  See the SVG for decomposition:
    # https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/big_hex_tri.svg

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

        self.hexagon_ratio = kwargs.get('hexagon_ratio', 0.5)

        # in u units
        self.hex_radius = 4 * self.hexagon_ratio / sqrt(7)
        # multiplier to get v units ...
        self.uv_ratio = self.tessagon.metadata.uv_ratio

        # Tilt
        self.theta_offset = -atan2(1, 3 * sqrt(3)) + pi/6
        self.hex_theta = [(self.theta_offset + number * pi / 3.0)
                          for number in range(6)]

    def hex_vert_coord(self, center, number):
        # number in range(6)
        return [center[0] +
                self.hex_radius * cos(self.hex_theta[number]),
                center[1] +
                self.hex_radius * sin(self.hex_theta[number]) * self.uv_ratio]

    def init_verts(self):
        if self.tile_type == 0:
            verts = {0: None,
                     1: None}
        else:
            verts = {2: None,
                     3: None,
                     4: None,
                     5: None}

        return verts

    def init_faces(self):
        if self.tile_type == 0:
            faces = {'A': None,
                     'B': None,
                     'C': None,
                     'D': None,
                     'E': None,
                     'F': None,
                     'G': None,
                     'H': None}
        else:
            faces = {'I': None,
                     'J': None,
                     'K': None,
                     'L': None,
                     'M': None,
                     'N': None,
                     'O': None,
                     'P': None,
                     'Q': None,
                     'R': None}

        return faces

    def calculate_verts(self):
        if self.tile_type == 0:
            self.add_vert([0], *self.hex_vert_coord([0, 1], 5))
            self.add_vert([1], *self.hex_vert_coord([1, 0], 2))
        else:
            self.add_vert([2], *self.hex_vert_coord([1, 1], 3))
            self.add_vert([3], *self.hex_vert_coord([1, 1], 4))
            self.add_vert([4], *self.hex_vert_coord([0, 0], 1))
            self.add_vert([5], *self.hex_vert_coord([0, 0], 0))

    def calculate_faces(self):
        if self.tile_type == 0:
            self.add_face('A',
                          [0,
                           top_tile(5),
                           top_tile(4),
                           top_left_tile(1),
                           left_tile(2),
                           left_tile(3)],
                          equivalent=[top_tile('T'),
                                      top_left_tile('H'),
                                      left_tile('I')])

            self.add_face('B',
                          [0,
                           right_tile(2),
                           top_tile(5)],
                          equivalent=[top_tile('S'),
                                      right_tile('K')])

            self.add_face('C',
                          [0,
                           right_tile(4),
                           right_tile(2)],
                          equivalent=[right_tile('L')])

            self.add_face('D',
                          [0,
                           1,
                           right_tile(4)],
                          equivalent=[right_tile('M')])

            self.add_face('E',
                          [1,
                           0,
                           left_tile(3)],
                          equivalent=[left_tile('P')])

            self.add_face('F',
                          [1,
                           left_tile(3),
                           left_tile(5)],
                          equivalent=[left_tile('Q')])

            self.add_face('G',
                          [1,
                           left_tile(5),
                           bottom_tile(2)],
                          equivalent=[left_tile('R')])

        else:
            self.add_face('N',
                          [2,
                           4,
                           3])

            self.add_face('O',
                          [3,
                           4,
                           5])

    def color_pattern1(self):
        if self.tile_type == 0:
            self.color_face('A', 2)
            self.color_face('B', 1)
            self.color_face('D', 1)
            self.color_face('F', 1)
        else:
            self.color_face('N', 1)


class BigHexTriTessagon(Tessagon):
    tile_class = BigHexTriTile
    metadata = metadata
