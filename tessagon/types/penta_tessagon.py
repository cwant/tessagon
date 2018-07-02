from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Pentagons',
                            classification='laves',
                            shapes=['pentagons'],
                            sides=[5])


class PentaTile(Tile):
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
                       [['left'], ['right', 'middle']],
                       [['left'], ['right', 'bottom', 'interior']]],
                      u_boundary=True)

        self.add_face(['left', 'bottom', 'v_boundary'],
                      [['left', 'bottom', 'u_boundary'],
                       ['left', 'bottom', 'interior'],
                       ['left', 'bottom', 'v_boundary'],
                       [['bottom'], ['left', 'top', 'interior']],
                       [['bottom'], ['left', 'top', 'u_boundary']]],
                      v_boundary=True)

        self.add_face(['left', 'middle'],
                      [['left', 'middle'],
                       ['left', 'bottom', 'interior'],
                       ['center', 'bottom'],
                       ['center', 'top'],
                       ['left', 'top', 'interior']])

        self.add_face(['center', 'bottom'],
                      [['left', 'bottom', 'interior'],
                       ['center', 'bottom'],
                       ['right', 'bottom', 'interior'],
                       ['right', 'bottom', 'v_boundary'],
                       ['left', 'bottom', 'v_boundary']])


class PentaTessagon(Tessagon):
    tile_class = PentaTile
    metadata = metadata
