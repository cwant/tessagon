from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Dissected Square',
                            num_color_patterns=2,
                            classification='laves',
                            shapes=['triangles'],
                            sides=[3])


class DissectedSquareTile(Tile):

    #    VERTS:     a = ['top', 'left']
    #    a---b---c  b = ['top', 'center']
    # ^  |\..|../|  c = ['top', 'right']
    # |  |.\.|./.|  d = ['middle', 'left']
    # |  d---e---f  e = ['middle', 'center']
    # |  |../|\..|  f = ['middle', 'right']
    #    |./.|.\.|  g = ['bottom', 'left']
    # V  g---h---i  h = ['bottom', 'center']
    #               i = ['bottom', 'right']
    #     U --->

    #    FACES:
    #    o---o---o  A = ['top', 'left', 'middle']
    # ^  |\.B|C./|  B = ['top', 'left', 'center']
    # |  |A\.|./D|  C = ['top', 'right', 'center']
    # |  o---o---o  D = ['top', 'right', 'middle']
    # |  |E./|\.H|  E = ['bottom', 'left', 'middle']
    #    |./F|G\.|  F = ['bottom', 'left', 'center']
    # V  o-------o  G = ['bottom', 'right', 'center']
    #               H = ['bottom', 'right', 'middle']
    #     U --->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'top': {'left': None,
                        'center': None,
                        'right': None},
                'middle': {'left': None,
                           'center': None,
                           'right': None},
                'bottom': {'left': None,
                           'center': None,
                           'right': None}}

    def init_faces(self):
        return {'top': {'left': {'middle': None, 'center': None},
                        'right': {'middle': None, 'center': None}},
                'bottom': {'left': {'middle': None, 'center': None},
                           'right': {'middle': None, 'center': None}}}

    def calculate_verts(self):
        # Symmetry allow you to get nine verts for the price of four.
        self.add_vert(['top', 'left'], 0, 1.0, corner=True)
        self.add_vert(['middle', 'left'], 0, 0.5, u_boundary=True)
        self.add_vert(['top', 'center'], 0.5, 1.0, v_boundary=True)
        self.add_vert(['middle', 'center'], 0.5, 0.5)

    def calculate_faces(self):
        # Symmetry allows you to create eight faces for the price of two
        self.add_face(['top', 'left', 'middle'],
                      [['top', 'left'],
                       ['middle', 'left'],
                       ['middle', 'center']])
        self.add_face(['top', 'left', 'center'],
                      [['top', 'left'],
                       ['middle', 'center'],
                       ['top', 'center']])

    def color_pattern1(self):
        self.color_paths([['top', 'left', 'center'],
                          ['top', 'right', 'middle'],
                          ['bottom', 'right', 'center'],
                          ['bottom', 'left', 'middle']], 1, 0)

    def color_pattern2(self):
        if (self.fingerprint[0] // 2 + self.fingerprint[1] // 2) % 2 == 0:
            self.color_tiles(1, 0)
        else:
            self.color_tiles(0, 1)

    def color_tiles(self, color1, color2):
        if self.fingerprint[0] % 2 == 0:
            if self.fingerprint[1] % 2 == 0:
                self.color_paths([['top', 'left', 'center'],
                                  ['bottom', 'right', 'middle']],
                                 color2, color1)
            else:
                self.color_paths([['bottom', 'left', 'center'],
                                  ['top', 'right', 'middle']],
                                 color2, color1)
        else:
            if self.fingerprint[1] % 2 == 0:
                self.color_paths([['top', 'right', 'center'],
                                  ['bottom', 'left', 'middle']],
                                 color2, color1)
            else:
                self.color_paths([['bottom', 'right', 'center'],
                                  ['top', 'left', 'middle']],
                                 color2, color1)


class DissectedSquareTessagon(Tessagon):
    tile_class = DissectedSquareTile
    metadata = metadata
