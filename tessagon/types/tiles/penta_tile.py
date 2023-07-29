from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, bottom_tile

# 16 verts, 12 faces (4 internal, 8 on boundaries)
#
#  +              O+++++++++O              +
#  +             +           +             +
#  O            +             +            O
#     ++       +               +       ++
#        ++   +                 +   ++
#            O+                 +O
#          ++   ++           ++   ++
#         +         +     +         +
#        +             O             +
#       +              +              +
#  ++++O               +               O++++
#       +              +              +
#        +             O             +
#         +         +     +         +
#          ++   ++           ++   ++
#            O+                 +O
#        ++   +                 +   ++
#     ++       +               +       ++
#  O            +             +            O
#  +             +           +             +
#  +              O+++++++++O              +


class PentaTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': {'u_boundary': None,
                                 'v_boundary': None,
                                 'interior': None},
                         'middle': None,
                         'bottom': {'u_boundary': None,
                                    'v_boundary': None,
                                    'interior': None}},
                'center': {'top': None,
                           'bottom': None},
                'right': {'top': {'u_boundary': None,
                                  'v_boundary': None,
                                  'interior': None},
                          'middle': None,
                          'bottom': {'u_boundary': None,
                                     'v_boundary': None,
                                     'interior': None}}}

    def init_faces(self):
        return {'left': {'top': {'u_boundary': None,
                                 'v_boundary': None},
                         'middle': None,
                         'bottom': {'u_boundary': None,
                                    'v_boundary': None}},
                'center': {'top': None,
                           'bottom': None},
                'right': {'top': {'u_boundary': None,
                                  'v_boundary': None},
                          'middle': None,
                          'bottom': {'u_boundary': None,
                                     'v_boundary': None}}}

    def calculate_verts(self):
        # u_unit is the length of the edges expressed as a
        # proportion of the tile
        u_unit = 1.0 / (1.0 + sqrt(3))
        u0 = v0 = 0
        u1 = v1 = u_unit/(2*sqrt(3))
        u3 = v3 = (0.5 + 1/sqrt(3)) * u_unit
        u2 = v2 = 0.5*(u1 + u3)
        u4 = v4 = 0.5

        self.add_vert(['left', 'bottom', 'u_boundary'], u0, v1,
                      u_boundary=True)
        self.add_vert(['left', 'bottom', 'v_boundary'], u3, v0,
                      v_boundary=True)
        self.add_vert(['left', 'bottom', 'interior'], u2, v2)
        self.add_vert(['left', 'middle'], u1, v4)
        self.add_vert(['center', 'bottom'], u4, v3)

    def calculate_faces(self):
        self.add_face(['left', 'bottom', 'u_boundary'],
                      [['left', 'bottom', 'u_boundary'],
                       ['left', 'bottom', 'interior'],
                       ['left', 'middle'],
                       left_tile(['right', 'middle']),
                       left_tile(['right', 'bottom', 'interior'])],
                      u_boundary=True)

        self.add_face(['left', 'bottom', 'v_boundary'],
                      [['left', 'bottom', 'v_boundary'],
                       ['left', 'bottom', 'interior'],
                       ['left', 'bottom', 'u_boundary'],
                       bottom_tile(['left', 'top', 'u_boundary']),
                       bottom_tile(['left', 'top', 'interior'])],
                      v_boundary=True)

        self.add_face(['left', 'middle'],
                      [['left', 'middle'],
                       ['left', 'bottom', 'interior'],
                       ['center', 'bottom'],
                       ['center', 'top'],
                       ['left', 'top', 'interior']])

        self.add_face(['center', 'bottom'],
                      [['left', 'bottom', 'v_boundary'],
                       ['right', 'bottom', 'v_boundary'],
                       ['right', 'bottom', 'interior'],
                       ['center', 'bottom'],
                       ['left', 'bottom', 'interior']])

    def color_pattern1(self):
        self.color_paths([
            ['right', 'middle'],
            ['center', 'bottom'],
            ['right', 'bottom', 'v_boundary'],
            ['right', 'bottom', 'u_boundary'],
        ], 1, 0)
