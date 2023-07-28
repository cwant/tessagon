from math import sqrt
from tessagon.core.tile import Tile
from tessagon.types.tiles.dissected_hex_quad_tiles import \
    DissectedHexQuadTile1Verts, DissectedHexQuadTile2Verts

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/dissected_hex_tri.svg


class DissectedHexTriTile(Tile):
    uv_ratio = 1.0 / sqrt(3.0)

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False


# Uses the same configuration of vertices as DissectedHexQuadTile1
class DissectedHexTriTile1(DissectedHexTriTile,
                           DissectedHexQuadTile1Verts):

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None,
                'F': None}

    def calculate_faces(self):
        self.add_face('A', [0, 3, 2])
        self.add_face('B', [0, 4, 3])
        self.add_face('C', [0, 1, 4])
        self.add_face('D', [2, 6, 5])
        self.add_face('E', [2, 3, 6])
        self.add_face('F', [3, 4, 6])

    def color_pattern1(self):
        self.color_face('B', 1)
        self.color_face('E', 1)


class DissectedHexTriTile2(DissectedHexTriTile,
                           DissectedHexQuadTile2Verts):

    def init_faces(self):
        return {'G': None,
                'H': None,
                'I': None,
                'J': None,
                'K': None,
                'L': None}

    def calculate_faces(self):
        self.add_face('G', [7, 8, 9])
        self.add_face('H', [9, 8, 10])
        self.add_face('I', [8, 11, 10])
        self.add_face('J', [9, 10, 12])
        self.add_face('K', [10, 11, 12])
        self.add_face('L', [11, 13, 12])

    def color_pattern1(self):
        self.color_face('G', 1)
        self.color_face('J', 1)
        self.color_face('I', 1)
        self.color_face('L', 1)
