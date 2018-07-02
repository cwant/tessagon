from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Squares and Triangles',
                            classification='archimedean',
                            shapes=['squares', 'triangles'],
                            sides=[4, 3])


class SquareTriTile(Tile):
    # 12 verts, 16 faces (8 internal, 8 on boundary)
    # The angles make it hard to draw all edges, some excluded
    #
    #
    #  ^  ..o..|..o..    3.o.3|3.o.3
    #  |  ./...o...\.    ./...o...\.
    #  |  o.../.\...o    o.4./3\.4.o
    #  |  ...o---o...    .3.o---o.3.
    #     o...\./...o    o.4.\3/.4.o
    #  V  .\...o.../.    .\...o.../.
    #     ..o..|..o..    3.o.3|3.o.3
    #      U ----->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        # u_square means on the square that is on the U-boundary
        return {'top': {'left': {'u_boundary': None,
                                 'v_boundary': None},
                        'right': {'u_boundary': None,
                                  'v_boundary': None},
                        'center': None},
                'bottom': {'left': {'u_boundary': None,
                                    'v_boundary': None},
                           'right': {'u_boundary': None,
                                     'v_boundary': None},
                           'center': None},
                'middle': {'left': None,
                           'right': None}}

    def init_faces(self):
        return {'tri': {'top': {'left': {'u_boundary': None,
                                         'v_boundary': None},
                                'right': {'u_boundary': None,
                                          'v_boundary': None},
                                'center': None},
                        'bottom': {'left': {'u_boundary': None,
                                            'v_boundary': None},
                                   'right': {'u_boundary': None,
                                             'v_boundary': None},
                                   'center': None},
                        'middle': {'left': None,
                                   'right': None}},
                'square': {'top': {'left': None,
                                   'right': None},
                           'bottom': {'left': None,
                                      'right': None}}}

    def calculate_verts(self):
        # u_unit is the length of the edges expressed as a
        # proportion of the tile
        u_unit = 1.0 / (1.0 + sqrt(3))

        u0 = 0
        u1 = 0.5*u_unit
        u2 = 0.5*(1.0-u_unit)
        u3 = 0.5

        v_unit = 1.0 / (1.0 + sqrt(3))
        v0 = 0.5
        v1 = 0.5 * (1.0 + v_unit)
        v2 = 1.0 - 0.5*v_unit
        v3 = 1.0

        # Define top left square, other verts defined through symmetry
        self.add_vert(['top', 'left', 'u_boundary'], u0, v1, u_boundary=True)
        self.add_vert(['top', 'left', 'v_boundary'], u1, v3, v_boundary=True)
        self.add_vert(['top', 'center'], u3, v2)
        self.add_vert(['middle', 'left'], u2, v0)

    def calculate_faces(self):
        # 4 internal squares (others via symmetry)
        self.add_face(['square', 'top', 'left'],
                      [['top', 'left', 'u_boundary'],
                       ['top', 'left', 'v_boundary'],
                       ['top', 'center'],
                       ['middle', 'left']],
                      face_type='square')

        # 4 u-boundary triangles
        self.add_face(['tri', 'top', 'left', 'u_boundary'],
                      [['top', 'left', 'v_boundary'],
                       ['top', 'left', 'u_boundary'],
                       [['left'], ['top', 'right', 'v_boundary']]],
                      face_type='triangle', u_boundary=True)

        # 4 v-boundary triangles
        self.add_face(['tri', 'top', 'left', 'v_boundary'],
                      [['top', 'left', 'v_boundary'],
                       ['top', 'center'],
                       [['top'], ['bottom', 'center']]],
                      face_type='triangle', v_boundary=True)

        # 2 internal center triangles
        self.add_face(['tri', 'top', 'center'],
                      [['top', 'center'],
                       ['middle', 'right'],
                       ['middle', 'left']],
                      face_type='triangle')

        # 2 internal middle triangles
        self.add_face(['tri', 'middle', 'left'],
                      [['middle', 'left'],
                       ['bottom', 'left', 'u_boundary'],
                       ['top', 'left', 'u_boundary']],
                      face_type='triangle')


class SquareTriTessagon(Tessagon):
    tile_class = SquareTriTile
    metadata = metadata
