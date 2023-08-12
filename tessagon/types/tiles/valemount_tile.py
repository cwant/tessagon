from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    top_tile, top_left_tile, top_right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile

#    o--o--o--o    1,2,3,4
#    |..|.....|
#    o..o--o--o    5,6,7,8
# ^  |..|..|..|
# |  o--o--o..o    9,10,11,12
# |  |.....|..|
# |  o--o--o--o    13,14,15,16
# V
#   U --->


class ValemountTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def init_verts(self):
        # Naming stuff is hard ...
        return {1: None,
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
                16: None}

    def init_faces(self):
        return {'top_left': None,
                'top_right': None,
                'bottom_left': None,
                'bottom_right': None,
                'center': None}

    def calculate_verts(self):
        # Top row
        self.add_vert([1], 0, 1,
                      equivalent=[left_tile(4),
                                  top_tile(13),
                                  top_left_tile(16)])

        self.add_vert([2], 1/3.0, 1,
                      equivalent=[top_tile(14)])

        self.add_vert([3], 2/3.0, 1,
                      equivalent=[top_tile(15)])

        self.add_vert([4], 1, 1,
                      equivalent=[right_tile(1),
                                  top_tile(16),
                                  top_right_tile(13)])

        # Next row
        self.add_vert([5], 0, 2/3.0,
                      equivalent=[left_tile(8)])

        self.add_vert([6], 1/3.0, 2/3.0)
        self.add_vert([7], 2/3.0, 2/3.0)

        self.add_vert([8], 1, 2/3.0,
                      equivalent=[right_tile(5)])

        # Next row
        self.add_vert([9], 0, 1/3.0,
                      equivalent=[left_tile(12)])

        self.add_vert([10], 1/3.0, 1/3.0)
        self.add_vert([11], 2/3.0, 1/3.0)

        self.add_vert([12], 1, 1/3.0,
                      equivalent=[right_tile(9)])

        # Bottom row
        self.add_vert([13], 0, 0,
                      equivalent=[left_tile(16),
                                  bottom_tile(1),
                                  bottom_left_tile(4)])

        self.add_vert([14], 1/3.0, 0,
                      equivalent=[bottom_tile(2)])

        self.add_vert([15], 2/3.0, 0,
                      equivalent=[bottom_tile(3)])

        self.add_vert([16], 1, 0,
                      equivalent=[right_tile(13),
                                  bottom_tile(4),
                                  bottom_right_tile(1)])

    def calculate_faces(self):
        self.add_face('top_left',
                      [5, 9, 10, 6, 2, 1])
        self.add_face('top_right',
                      [6, 7, 8, 4, 3, 2])
        self.add_face('bottom_left',
                      [13, 14, 15, 11, 10, 9])
        self.add_face('bottom_right',
                      [11, 15, 16, 12, 8, 7])
        self.add_face('center',
                      [10, 11, 7, 6])

    def color_pattern1(self):
        self.color_paths([
            ['center']
        ], 1, 0)