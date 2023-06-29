from math import atan2, sqrt, sin, cos, pi
from tessagon.core.tessagon import Tessagon
from tessagon.core.alternating_tile import AlternatingTile
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import right_tile, left_tile, \
    top_tile, top_left_tile, top_right_tile, \
    bottom_tile, bottom_right_tile

metadata = TessagonMetadata(name='Florets',
                            num_color_patterns=3,
                            classification='laves',
                            shapes=['pentagons'],
                            sides=[5],
                            uv_ratio=1.0/sqrt(3))


class FloretTile(AlternatingTile):
    #  See the SVG for decomposition:
    # https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/floret.svg

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

        # multiplier to get v units ...
        self.uv_ratio = self.tessagon.metadata.uv_ratio

        # Tilt
        theta_offset1 = pi/3 - atan2(sqrt(3), 9)
        theta_offset2 = pi/6

        # No hexagons in this pattern, but verts lie of hexagons
        # radius is in u inits
        self.hexagons = [
            {'radius': 4 / sqrt(21),
             'hex_theta': [(theta_offset1 + number * pi / 3.0)
                           for number in range(6)]},
            # Just guessing ...
            {'radius': 2 / (3 * self.uv_ratio),
             'hex_theta': [(theta_offset2 + number * pi / 3.0)
                           for number in range(6)]},
        ]

    def hex_vert_coord(self, hexagon_num, center, number):
        # hexagon_num in range(2)
        # number in range(6)
        hexagon = self.hexagons[hexagon_num]
        return [center[0] +
                hexagon['radius'] * cos(hexagon['hex_theta'][number]),
                center[1] +
                hexagon['radius'] * sin(hexagon['hex_theta'][number]) *
                self.uv_ratio]

    def init_verts(self):
        if self.tile_type == 0:
            verts = {i: None for i in range(6)}
        else:
            verts = {i: None for i in range(6, 14)}

        return verts

    def init_faces(self):
        if self.tile_type == 0:
            faces = {c: None for c in ['A', 'B', 'C', 'D']}
        else:
            faces = {c: None for c in ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']}

        return faces

    def calculate_verts(self):
        if self.tile_type == 0:
            self.add_vert([2], *self.hex_vert_coord(0, [0, 0], 0))
            self.add_vert([3], *self.hex_vert_coord(0, [1, 1], 3))
        else:
            self.add_vert([6], 1, 0,
                          equivalent=[right_tile(0),
                                      bottom_right_tile(13),
                                      bottom_tile(5)])
            self.add_vert([7], *self.hex_vert_coord(0, [1, 0], 2))
            self.add_vert([8], *self.hex_vert_coord(1, [0, 1], 4),
                          equivalent=[left_tile(1)])
            self.add_vert([9], *self.hex_vert_coord(0, [0, 1], 4))
            self.add_vert([10], *self.hex_vert_coord(0, [1, 0], 1))
            self.add_vert([11], *self.hex_vert_coord(1, [0, 1], 5),
                          equivalent=[right_tile(4)])
            self.add_vert([12], *self.hex_vert_coord(0, [0, 1], 5))
            self.add_vert([13], 0, 1,
                          equivalent=[left_tile(5),
                                      top_left_tile(6),
                                      top_tile(0)])

    def calculate_faces(self):
        # All of tile type 0 faces overlap tiles of type 1
        if self.tile_type == 0:
            return

        # Tile 'E' is handled as Tile 'K' on another tile
        # Tile 'F' is handled as Tile 'L' on another tile
        self.add_face('G', [6,
                            10,
                            9,
                            8,
                            7])

        self.add_face('H', [11,
                            10,
                            6,
                            right_tile(2),
                            right_tile(3)],
                      equivalent=[right_tile('B')])

        self.add_face('I', [8,
                            9,
                            13,
                            left_tile(3),
                            left_tile(2)],
                      equivalent=[left_tile('C')])

        self.add_face('J', [13,
                            9,
                            10,
                            11,
                            12])

        self.add_face('K', [12,
                            11,
                            right_tile(3),
                            right_tile(5),
                            top_right_tile(7)],
                      equivalent=[right_tile('D'),
                                  top_right_tile('E')])

        self.add_face('L', [13,
                            12,
                            top_right_tile(7),
                            top_tile(1),
                            top_tile(2)],
                      equivalent=[top_right_tile('F'),
                                  top_tile('A')])

    def floret_fingerprint(self, face):
        fingerprint = list(self.fingerprint.copy())

        fingerprint[0] = fingerprint[0] // 2 + fingerprint[1] // 2

        if face in ['F']:
            fingerprint[0] -= 1
        elif face in ['K']:
            fingerprint[0] += 1

        if self.fingerprint[0] % 2 == 0:
            if face in ['A', 'B']:
                fingerprint[0] -= 1
        else:
            if face in ['C', 'D']:
                fingerprint[0] += 1

        if face in ['A', 'B', 'E', 'F', 'G', 'H']:
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
