from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import left_tile, right_tile, \
    top_tile, top_left_tile, top_right_tile, \
    bottom_tile, bottom_left_tile, bottom_right_tile

metadata = TessagonMetadata(name='Valemount',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['rectangles', 'squares'],
                            sides=[4],
                            uv_ratio=1.0)


class ValemountTile(Tile):
    #    o--o--o--o    1,2,3,4
    #    |..|.....|
    #    o..o--o--o    5,6,7,8
    # ^  |..|..|..|
    # |  o--o--o..o    9,10,11,12
    # |  |.....|..|
    # |  o--o--o--o    13,14,15,16
    # V
    #   U --->

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
        vert = self.add_vert([1], 0, 1)
        self.set_equivalent_vert(*left_tile(4), vert)
        self.set_equivalent_vert(*top_tile(13), vert)
        self.set_equivalent_vert(*top_left_tile(16), vert)

        vert = self.add_vert([2], 1/3.0, 1)
        self.set_equivalent_vert(*top_tile(14), vert)

        vert = self.add_vert([3], 2/3.0, 1)
        self.set_equivalent_vert(*top_tile(15), vert)

        vert = self.add_vert([4], 1, 1)
        self.set_equivalent_vert(*right_tile(1), vert)
        self.set_equivalent_vert(*top_tile(16), vert)
        self.set_equivalent_vert(*top_right_tile(13), vert)

        # Next row
        vert = self.add_vert([5], 0, 2/3.0)
        self.set_equivalent_vert(*left_tile(8), vert)

        self.add_vert([6], 1/3.0, 2/3.0)
        self.add_vert([7], 2/3.0, 2/3.0)

        vert = self.add_vert([8], 1, 2/3.0)
        self.set_equivalent_vert(*right_tile(5), vert)

        # Next row
        vert = self.add_vert([9], 0, 1/3.0)
        self.set_equivalent_vert(*left_tile(12), vert)

        self.add_vert([10], 1/3.0, 1/3.0)
        self.add_vert([11], 2/3.0, 1/3.0)

        vert = self.add_vert([12], 1, 1/3.0)
        self.set_equivalent_vert(*right_tile(9), vert)

        # Bottom row
        vert = self.add_vert([13], 0, 0)
        self.set_equivalent_vert(*left_tile(16), vert)
        self.set_equivalent_vert(*bottom_tile(1), vert)
        self.set_equivalent_vert(*bottom_left_tile(4), vert)

        vert = self.add_vert([14], 1/3.0, 0)
        self.set_equivalent_vert(*bottom_tile(2), vert)

        vert = self.add_vert([15], 2/3.0, 0)
        self.set_equivalent_vert(*bottom_tile(3), vert)

        vert = self.add_vert([16], 1, 0)
        self.set_equivalent_vert(*right_tile(13), vert)
        self.set_equivalent_vert(*bottom_tile(4), vert)
        self.set_equivalent_vert(*bottom_right_tile(1), vert)

    def calculate_faces(self):
        self.add_face('top_left',
                      [1, 2, 6, 10, 9, 5])
        self.add_face('top_right',
                      [2, 3, 4, 8, 7, 6])
        self.add_face('bottom_left',
                      [9, 10, 11, 15, 14, 13])
        self.add_face('bottom_right',
                      [7, 8, 12, 16, 15, 11])
        self.add_face('center',
                      [6, 7, 11, 10])

    def color_pattern1(self):
        self.color_paths([
            ['center']
        ], 1, 0)


class ValemountTessagon(Tessagon):
    tile_class = ValemountTile
    metadata = metadata
