from tessagon.core.tile import Tile
from tessagon.core.tile_utils import bottom_tile, left_tile, \
    bottom_left_tile


# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/pythagorean.svg


class PythagoreanTile(Tile):
    uv_ratio = 1.0
    TOLERANCE = 0.0000001

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False
        self.square_ratio = kwargs.get('square_ratio', 0.5)

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None}

    def vert0(self):
        # Degenerate cases
        if self.square_ratio > 1 - self.TOLERANCE:
            return (0, 0.5)
        elif self.square_ratio < self.TOLERANCE:
            return (0.5, 0.5)

        # Basically intersecting some lines to figure this out
        # E.g., square_ratio == 1/2 --> slope = 2, solve for x, y:
        #   y = slope * (x - 0.5) + 1
        #   y = 0.5 - x / slope

        slope = 1 / self.square_ratio
        slope2 = slope ** 2
        x = 0.5 * (slope2 - slope) / (slope2 + 1)
        y = 0.5 - x / slope

        return (x, y)

    def calculate_verts(self):
        (u0, v0) = self.vert0()
        self.add_vert(0, u0, v0)
        self.add_vert(1, 1 - v0, u0)
        self.add_vert(2, 1 - u0, 1 - v0)
        self.add_vert(3, v0, 1 - u0)

    def calculate_faces(self):
        self.add_face('A', [1,
                            0,
                            left_tile(2),
                            left_tile(1),
                            bottom_left_tile(3),
                            bottom_left_tile(2),
                            bottom_tile(0),
                            bottom_tile(3)],
                      equivalent=[left_tile('B'),
                                  bottom_left_tile('D'),
                                  bottom_tile('C')])

        self.add_face('E', [0,
                            1,
                            2,
                            3])

    def color_pattern1(self):
        # Color the big ones
        self.color_face('A', 1)