from math import atan2, sqrt, sin, cos, pi
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_boundary, right_boundary, \
    top_boundary, bottom_boundary

#  See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/floret.svg


class FloretTile(Tile):
    uv_ratio = 1.0 / sqrt(3)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

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


class FloretTile1(FloretTile):
    BOUNDARY = dict(
        top=['vert', 'face', 'tangent-split'],
        left=['tangent-split', 'face-1', 'vert-1', 'face-2', 'vert-2'],
        bottom=['vert', 'face', 'tangent-split'],
        right=['tangent-split', 'face-1', 'vert-1', 'face-2', 'vert-2']
    )

    def init_verts(self):
        return {i: None for i in range(6)}

    def init_faces(self):
        return {c: None for c in ['A', 'B', 'C', 'D']}

    def calculate_verts(self):
        self.add_vert(0,
                      0, 0,
                      left_boundary='vert-2')

        self.add_vert(1,
                      *self.hex_vert_coord(1, [1, 1], 4),
                      right_boundary='vert-1')

        self.add_vert(2,
                      *self.hex_vert_coord(0, [0, 0], 0))

        self.add_vert(3,
                      *self.hex_vert_coord(0, [1, 1], 3))

        self.add_vert(4,
                      *self.hex_vert_coord(1, [0, 0], 1),
                      left_boundary='vert-1')

        self.add_vert(5,
                      1, 1,
                      right_boundary='vert-2')

    def calculate_faces(self):
        self.add_face('A', [1,
                            2,
                            0,
                            bottom_boundary('face')])

        self.add_face('B', [0,
                            2,
                            3,
                            4,
                            left_boundary('face-2')])

        self.add_face('C', [5,
                            3,
                            2,
                            1,
                            right_boundary('face-2')])

        self.add_face('D', [4,
                            3,
                            5,
                            top_boundary('face')])

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


class FloretTile2(FloretTile):
    BOUNDARY = dict(
        top=['split', 'face', 'vert'],
        left=['vert-1', 'face-1', 'vert-2', 'face-2', 'split'],
        bottom=['split', 'face', 'vert'],
        right=['vert-1', 'face-1', 'vert-2', 'face-2', 'split']
    )

    def init_verts(self):
        return {i: None for i in range(6, 14)}

    def init_faces(self):
        return {c: None for c in ['E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']}

    def calculate_verts(self):
        self.add_vert(6,
                      1, 0,
                      bottom_boundary='vert')

        self.add_vert(7,
                      *self.hex_vert_coord(0, [1, 0], 2))

        self.add_vert(8,
                      *self.hex_vert_coord(1, [0, 1], 4),
                      left_boundary='vert-2')

        self.add_vert(9,
                      *self.hex_vert_coord(0, [0, 1], 4))

        self.add_vert(10,
                      *self.hex_vert_coord(0, [1, 0], 1))

        self.add_vert(11,
                      *self.hex_vert_coord(1, [0, 1], 5),
                      right_boundary='vert-2')

        self.add_vert(12,
                      *self.hex_vert_coord(0, [0, 1], 5))

        self.add_vert(13,
                      0, 1,
                      top_boundary='vert')

    def calculate_faces(self):
        self.add_face('E', [6,
                            7,
                            bottom_boundary('face')])

        self.add_face('F', [7,
                            8,
                            left_boundary('face-2')])

        self.add_face('G', [6,
                            10,
                            9,
                            8,
                            7])

        self.add_face('H', [11,
                            10,
                            6,
                            right_boundary('face-1')])

        self.add_face('I', [8,
                            9,
                            13,
                            left_boundary('face-1')])

        self.add_face('J', [13,
                            9,
                            10,
                            11,
                            12])

        self.add_face('K', [12,
                            11,
                            right_boundary('face-2')])

        self.add_face('L', [13,
                            12,
                            top_boundary('face')])

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
