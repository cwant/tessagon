from math import sqrt, atan2, sin, cos, pi
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import \
    left_tile, top_tile, top_left_tile, \
    right_tile, bottom_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/dodeca.svg


class HexBigTriTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)

        self.u_symmetric = False
        self.v_symmetric = False

        # Future use to control hexagon size?
        self.hexagon_ratio = 0.5

        # in u units
        self.hex_radius = 4 * self.hexagon_ratio / sqrt(7)

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


class HexBigTriTile1(HexBigTriTile):

    def init_verts(self):
        return {0: None, 1: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}

    def calculate_verts(self):
        self.add_vert([0], *self.hex_vert_coord([0, 1], 5))
        self.add_vert([1], *self.hex_vert_coord([1, 0], 2))

    def calculate_faces(self):
        # Top Hexagon
        self.add_face('A',
                      [0,
                       top_tile(5),
                       top_tile(4),
                       top_left_tile(1),
                       left_tile(2),
                       left_tile(3)],
                      equivalent=[left_tile('F'),
                                  top_left_tile('D'),
                                  top_tile('I')])

        # Left Triangle
        self.add_face('B',
                      [1,
                       0,
                       left_tile(3),
                       left_tile(4),
                       left_tile(5),
                       bottom_tile(2)],
                      equivalent=[bottom_tile('E'),
                                  left_tile('H')])

        # Right Triangle
        self.add_face('C',
                      [0,
                       1,
                       right_tile(4),
                       right_tile(3),
                       right_tile(2),
                       top_tile(5)],
                      equivalent=[right_tile('G'),
                                  top_tile('J')])

    def color_pattern1(self):
        self.color_face('A', 1)

    def color_pattern2(self):
        self.color_face('A', 1)
        self.color_face('B', 2)


class HexBigTriTile2(HexBigTriTile):

    def init_verts(self):
        return {2: None,
                3: None,
                4: None,
                5: None}

    def init_faces(self):
        return {'E': None,
                'F': None,
                'G': None,
                'H': None,
                'I': None,
                'J': None}

    def calculate_verts(self):
        self.add_vert([2], *self.hex_vert_coord([1, 1], 3))
        self.add_vert([3], *self.hex_vert_coord([1, 1], 4))
        self.add_vert([4], *self.hex_vert_coord([0, 0], 1))
        self.add_vert([5], *self.hex_vert_coord([0, 0], 0))

    def calculate_faces(self):
        pass

    def color_pattern1(self):
        pass

    def color_pattern2(self):
        pass
