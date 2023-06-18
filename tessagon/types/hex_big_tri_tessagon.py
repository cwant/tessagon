from math import sqrt, atan2, sin, cos, pi
from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import \
    left_tile, top_tile, top_left_tile, \
    right_tile, top_right_tile

metadata = TessagonMetadata(name='Hexagons and Big Triangles',
                            num_color_patterns=2,
                            classification='non_edge',
                            shapes=['hexagons', 'triangles'],
                            sides=[6, 3],
                            uv_ratio=1.0/sqrt(3.0))

class HexBigTriTile(Tile):
    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.rot_symmetric = 180

        # Future use to control hexagon size?
        self.hexagon_ratio = 0.5

        # in u units
        self.hex_radius = 2 * self.hexagon_ratio / sqrt(7)

        # multiplier to get v units ...
        self.uv_ratio = self.tessagon.metadata.uv_ratio

        # Tilt...
        self.theta_offset = -atan2(1, 3 * sqrt(3)) + pi/6
        self.hex_theta = [(self.theta_offset + number * pi / 3.0) \
                          for number in range(6)]

    def hex_vert_coord(self, center, number):
        # number in range(6)
        return [center[0] + \
                self.hex_radius * cos(self.hex_theta[number]),
                center[1] + \
                self.hex_radius * sin(self.hex_theta[number]) * self.uv_ratio]

    def init_verts(self):
        verts = {'rotate0': {},
                 'rotate180': {}}

        for i in ['rotate0', 'rotate180']:
            for j in range(6):
                verts[i][j] = None
        return verts

    def init_faces(self):
        faces = {'rotate0': {},
                 'rotate180': {},
                 'middle': None}

        for i in ['rotate0', 'rotate180']:
            for j in range(6):
                faces[i][j] = None
        return faces

    def calculate_verts(self):
        self.add_vert(['rotate0', 0], *self.hex_vert_coord([0, 1], 5))

        self.add_vert(['rotate0', 1], *self.hex_vert_coord([1, 1], 3))
        self.add_vert(['rotate0', 2], *self.hex_vert_coord([1, 1], 4))

        self.add_vert(['rotate0', 3], *self.hex_vert_coord([0.5, 0.5], 0))
        self.add_vert(['rotate0', 4], *self.hex_vert_coord([0.5, 0.5], 1))
        self.add_vert(['rotate0', 5], *self.hex_vert_coord([0.5, 0.5], 2))

    def calculate_faces(self):
        # Hexagon
        self.add_face(['middle'],
                      [['rotate0', 3],
                       ['rotate0', 4],
                       ['rotate0', 5],
                       ['rotate180', 3],
                       ['rotate180', 4],
                       ['rotate180', 5]])

        # Top left Hexagon
        face = self.add_face(['rotate0', 0],
                             [['rotate0', 0],
                              top_tile(['rotate180', 1]),
                              top_tile(['rotate180', 2]),
                              top_left_tile(['rotate180', 0]),
                              left_tile(['rotate0', 1]),
                              left_tile(['rotate0', 2])],
                             equivalent=[left_tile(['rotate0', 3]),
                                         top_left_tile(['rotate180', 0]),
                                         top_tile(['rotate180', 3])])

        # Top right Hexagon
        face = self.add_face(['rotate0', 3],
                             [['rotate0', 2],
                              ['rotate0', 1],
                              top_tile(['rotate180', 0]),
                              top_right_tile(['rotate180', 2]),
                              top_right_tile(['rotate180', 1]),
                              right_tile(['rotate0', 0])],
                             equivalent=[top_tile(['rotate180', 0]),
                                         top_right_tile(['rotate180', 3]),
                                         right_tile(['rotate0', 0])])

        # Top left Triangle (mostly interior)
        face = self.add_face(['rotate0', 1],
                             [['rotate0', 0],
                              ['rotate0', 5],
                              ['rotate0', 4],
                              ['rotate0', 2],
                              ['rotate0', 1],
                              top_tile(['rotate180', 1])],
                             equivalent=[top_tile(['rotate180', 2])])
        
        # Top right Triangle (mostly exterior)
        face = self.add_face(['rotate0', 2],
                             [['rotate0', 1],
                              top_tile(['rotate180', 0]),
                              top_tile(['rotate180', 5]),
                              top_tile(['rotate180', 4]),
                              top_tile(['rotate180', 2]),
                              top_tile(['rotate180', 1])],
                             equivalent=[top_tile(['rotate180', 1])])

        # Left Triangle
        face = self.add_face(['rotate0', 4],
                             [['rotate180', 3],
                              ['rotate0', 5],
                              ['rotate0', 0],
                              left_tile(['rotate0', 2]),
                              left_tile(['rotate0', 4]),
                              left_tile(['rotate0', 3])],
                             equivalent=[left_tile(['rotate0', 5])])

        # Right Triangle
        face = self.add_face(['rotate0', 5],
                             [['rotate0', 2],
                              ['rotate0', 4],
                              ['rotate0', 3],
                              right_tile(['rotate180', 3]),
                              right_tile(['rotate0', 5]),
                              right_tile(['rotate0', 0])],
                             equivalent=[right_tile(['rotate0', 4])])
        
    def color_pattern1(self):
        self.color_face(['middle'], 1)
        self.color_face(['rotate0', 0], 1)
        self.color_face(['rotate0', 3], 1)
        self.color_face(['rotate180', 0], 1)
        self.color_face(['rotate180', 3], 1)

    def color_pattern2(self):
        self.color_face(['rotate0', 1], 1)
        self.color_face(['rotate180', 4], 1)
        self.color_face(['rotate180', 5], 1)
        self.color_face(['rotate180', 2], 1)

        self.color_face(['middle'], 2)
        self.color_face(['rotate0', 0], 2)
        self.color_face(['rotate0', 3], 2)
        self.color_face(['rotate180', 0], 2)
        self.color_face(['rotate180', 3], 2)


class HexBigTriTessagon(Tessagon):
    tile_class = HexBigTriTile
    metadata = metadata
