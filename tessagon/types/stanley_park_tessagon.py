from math import sqrt
from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import top_tile, bottom_tile, \
    top_left_tile, left_tile

metadata = TessagonMetadata(name='Stanley Park',
                            num_color_patterns=2,
                            classification='non_convex',
                            sides=[12],
                            uv_ratio=sqrt(3.0))

# Non-convex pattern. Might work better for 2D than 3D
# Also, the ASCII art below is a bit hard to visualize,
# so check out preview images linked from README.md


class StanleyParkTile(Tile):
    #    VERTS:
    #   ....a...b....  a = ['top', 'left']
    # ^ .../.....\...  b = ['top', 'right']
    # | ..c.......d..  c = ['mid1', 'left']
    # | ..|.......|..  d = ['mid1', 'right']
    # | ..e...f...g .  e = ['mid2', 'left']
    # | ./.\./.\./.\.  f = ['mid2', 'center']
    #   h...i...j...k  g = ['mid2', 'right']
    # V ....|...|....  h = ['mid3', 'left', 'outer']
    #   ....l...m....  i = ['mid3', 'left', 'inner']
    #                  j = ['mid3', 'right', 'inner']
    #     U --->       k = ['mid3', 'right', 'outer']
    #                  l = ['bottom', 'left']
    #                  m = ['bottom', 'right']

    #    FACES:
    #   ....o...o....
    # ^ .A./.....\.C.  A = ['top', 'left']
    # | ..o...B...o..  B = ['top', 'middle']
    # | ..|.......|..  C = ['top', 'right']
    # | ..o...o...o .  D = ['bottom', 'left']
    # | ./.\./.\./.\.  E = ['bottom', 'middle']
    #   o...o...o...o  F = ['bottom', 'right']
    # V ..D.|.E.|.F..
    #   ....o...o....
    #
    #     U --->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = False

    def init_verts(self):
        return {'top': {'left': None,
                        'right': None},
                'mid1': {'left': None,
                         'right': None},
                'mid2': {'left': None,
                         'center': None,
                         'right': None},
                'mid3': {'left': {'outer': None,
                                  'inner': None},
                         'right': {'inner': None,
                                   'outer': None}},
                'bottom': {'left': None,
                           'right': None}}

    def init_faces(self):
        return {'top': {'left': None,
                        'center': None,
                        'right': None},
                'bottom': {'left': None,
                           'center': None,
                           'right': None}}

    def calculate_verts(self):
        vert = self.add_vert(['top', 'left'], 2.0/6.0, 1.0)
        self.set_equivalent_vert(*top_tile(['bottom', 'left']), vert)
        # Reflection doesn't handle 'set_equivalent_vert' so ...
        vert = self.add_vert(['top', 'right'], 4.0/6.0, 1.0)
        self.set_equivalent_vert(*top_tile(['bottom', 'right']), vert)

        self.add_vert(['mid1', 'left'], 1.0/6.0, 5.0/6.0)
        self.add_vert(['mid2', 'left'], 1.0/6.0, 3.0/6.0)
        self.add_vert(['mid2', 'center'], 3.0/6.0, 3.0/6.0)
        self.add_vert(['mid3', 'left', 'outer'], 0.0, 2.0/6.0,
                      u_boundary=True)
        self.add_vert(['mid3', 'left', 'inner'], 2.0/6.0, 2.0/6.0)

        vert = self.add_vert(['bottom', 'left'], 2.0/6.0, 0.0)
        self.set_equivalent_vert(*bottom_tile(['top', 'left']), vert)
        vert = self.add_vert(['bottom', 'right'], 4.0/6.0, 0.0)
        self.set_equivalent_vert(*bottom_tile(['top', 'right']), vert)

    def calculate_faces(self):
        face = self.add_face(['top', 'left'],
                             [['mid3', 'left', 'outer'],
                              ['mid2', 'left'],
                              ['mid1', 'left'],
                              ['top', 'left'],
                              top_tile(['mid3', 'left', 'inner']),
                              top_tile(['mid2', 'left']),
                              top_tile(['mid3', 'left', 'outer']),
                              top_left_tile(['mid2', 'right']),
                              top_left_tile(['mid3', 'right', 'inner']),
                              left_tile(['top', 'right']),
                              left_tile(['mid1', 'right']),
                              left_tile(['mid2', 'right'])],
                             u_boundary=True)
        self.set_equivalent_face(*top_tile(['bottom', 'left']), face)
        self.set_equivalent_face(*top_left_tile(['bottom', 'right']), face)
        self.set_equivalent_face(*left_tile(['top', 'right']), face)

        face = self.add_face(['top', 'center'],
                             [['top', 'left'],
                              ['mid1', 'left'],
                              ['mid2', 'left'],
                              ['mid3', 'left', 'inner'],
                              ['mid2', 'center'],
                              ['mid3', 'right', 'inner'],
                              ['mid2', 'right'],
                              ['mid1', 'right'],
                              ['top', 'right'],
                              top_tile(['mid3', 'right', 'inner']),
                              top_tile(['mid2', 'center']),
                              top_tile(['mid3', 'left', 'inner'])])
        self.set_equivalent_face(*top_tile(['bottom', 'center']), face)

    def color_pattern1(self):
        self.color_face(['top', 'center'], 1)
        self.color_face(['bottom', 'center'], 1)

    def color_pattern2(self):
        if self.fingerprint[1] % 2 == 0:
            self.color_face(['top', 'left'], 1)
            self.color_face(['top', 'center'], 1)
            self.color_face(['top', 'right'], 1)


class StanleyParkTessagon(Tessagon):
    tile_class = StanleyParkTile
    metadata = metadata
