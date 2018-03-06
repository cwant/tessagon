from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile


class HexTile(Tile):
    num_color_patterns = 2

    #    VERTS:
    #    ..|..
    #    ..a..  a = ['top', 'center']
    # ^  ./.\.  b = ['top', 'left']
    # |  b...c  c = ['top', 'right']
    # |  |...|  d = ['bottom', 'left']
    # |  d...e  e = ['bottom', 'right']
    # |  .\./.  f = ['bottom', 'center']
    #    ..f..
    # V  ..|..
    #
    #     U --->

    #    FACES:
    #    A.|.B
    #    ..o..  A = ['top', 'left']
    # ^  ./.\.  B = ['top', 'right']
    # |  o...o  C = ['middle']
    # |  |.C.|  D = ['bottom', 'left']
    # |  o...o  E = ['bottom', 'right']
    # |  .\./.
    #    ..o..
    # V  D.|.E
    #
    #     U --->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'top': {'left': None,
                        'center': None,
                        'right': None},
                'bottom': {'left': None,
                           'center': None,
                           'right': None}}

    def init_faces(self):
        return {'top': {'left': None,
                        'right': None},
                'middle': None,
                'bottom': {'left': None,
                           'right': None}}

    def calculate_verts(self):
        # Symmetry allow you to get six verts for the price of two.

        # Next line also defines the vert at ['bottom', 'center']
        self.add_vert(['top', 'center'], 0.5, 5.0/6.0)

        # Next line also defines the verts at: ['bottom', 'left']
        #                                      ['bottom', 'right']
        #                                      ['top', 'right']
        self.add_vert(['top', 'left'], 0, 2.0/3.0, u_boundary=True)

    def calculate_faces(self):
        # Symmetry allows you to create five faces for the price of two
        self.add_face('middle', [['top', 'center'],
                                 ['top', 'left'],
                                 ['bottom', 'left'],
                                 ['bottom', 'center'],
                                 ['bottom', 'right'],
                                 ['top', 'right']])

        # The next line also defines the faces at: ['top', 'right']
        #                                          ['bottom', 'right']
        #                                          ['bottom', 'left']
        self.add_face(['top', 'left'],
                      # The first two verts of the face are on this tile
                      [['top', 'left'],
                       ['top', 'center'],
                       # The other four verts are on neighboring tiles.
                       # E.g., the next one is the ['bottom', 'center']
                       # vert on the top neighbor tile.
                       [['top'], ['bottom', 'center']],
                       [['top'], ['bottom', 'left']],
                       [['top', 'left'], ['bottom', 'center']],
                       [['left'], ['top', 'center']]],
                      # Defining the face as a 'corner' also associates the
                      # created face as one that is shared with
                      # neighboring tiles.
                      corner=True)

    def color_pattern1(self):
        if self.fingerprint[0] % 3 == 0:
            self.color_paths([['top', 'left'],
                              ['bottom', 'left']], 1, 0)
        elif self.fingerprint[0] % 3 == 1:
            self.color_paths([['middle']], 1, 0)
        else:
            self.color_paths([['top', 'right'],
                              ['bottom', 'right']], 1, 0)

    def color_pattern2(self):
        if self.fingerprint[0] % 3 == 0:
            self.color_paths_hash({1: [['top', 'left'],
                                       ['bottom', 'left']],
                                   2: [['top', 'right'],
                                       ['bottom', 'right']]}, 0)
        elif self.fingerprint[0] % 3 == 1:
            self.color_paths_hash({1: [['middle']],
                                   2: [['top', 'left'],
                                       ['bottom', 'left']]}, 0)
        else:
            self.color_paths_hash({2: [['middle']],
                                   1: [['top', 'right'],
                                       ['bottom', 'right']]}, 0)


class HexTessagon(Tessagon):
    tile_class = HexTile
