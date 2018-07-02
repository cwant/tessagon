from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Hexagons, Squares, and Triangles',
                            classification='archimedean',
                            shapes=['hexagons', 'squares', 'triangles'],
                            sides=[6, 4, 3])


class HexSquareTriTile(Tile):
    # 14 verts, 19 faces (7 internal, 12 on boundary)
    # The angles make it hard to draw all edges, some excluded
    #
    #     ...|...|...  6..|.4.|..6
    #     ...o---o...  ...o---o...
    #  ^  o ..\./...o  o.4.\3/.4.o
    #  |  .\...o.../.  3\...o.../3 Numbers are faces with # sides
    #  |  --o.....o--  --o.....o--
    #  |  ..|.....|..  4.|..6..|.4
    #  |  --o.... o--  --o.... o--
    #     ./.. o...\.  3/.. o...\3
    #  V  o.../.\...o  o.4./3\.4.o
    #     ...o---o...  ...o---o...
    #     ...|...|...  6..|.4.|..6
    #
    #       U ---->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        # u_square means on the square that is on the U-boundary
        return {'top': {'left': {'u_boundary': None,
                                 'u_square': None,
                                 'v_square': None},
                        'right': {'u_boundary': None,
                                  'u_square': None,
                                  'v_square': None},
                        'center': None},
                'bottom': {'left': {'u_boundary': None,
                                    'u_square': None,
                                    'v_square': None},
                           'right': {'u_boundary': None,
                                     'u_square': None,
                                     'v_square': None},
                           'center': None}}

    def init_faces(self):
        # Whelp!
        return {'hex': {'top': {'left': None,
                                'right': None},
                        'bottom': {'left': None,
                                   'right': None},
                        'middle': None},
                'tri': {'top': {'left': None,
                                'center': None,
                                'right': None},
                        'bottom': {'left': None,
                                   'center': None,
                                   'right': None}},
                'square': {'top': {'left': None,
                                   'center': None,
                                   'right': None},
                           'bottom': {'left': None,
                                      'center': None,
                                      'right': None},
                           'middle': {'left': None,
                                      'right': None}}}

    def calculate_verts(self):
        # u_unit is the length of the edges expressed as a
        # proportion of the tile
        u_unit = 1.0 / (1.0 + sqrt(3))
        u0 = 0
        u1 = 0.5*u_unit
        u2 = 0.5*(1.0-u_unit)
        u3 = 0.5

        v_unit = 1.0 / (3.0 + sqrt(3))
        v0 = 1.0 - 0.5*v_unit
        v1 = 1.0 - v_unit
        v2 = 0.5 + v_unit
        v3 = 1.0 - 2.0*v_unit

        # Define top left square, other verts defined through symmetry
        self.add_vert(['top', 'left', 'v_square'], u2, v0)
        self.add_vert(['top', 'center'], u3, v2)
        self.add_vert(['top', 'left', 'u_square'], u1, v3)
        self.add_vert(['top', 'left', 'u_boundary'], u0, v1, u_boundary=True)

    def calculate_faces(self):
        # Middle hexagon
        self.add_face(['hex', 'middle'],
                      [['top', 'center'],
                       ['top', 'left', 'u_square'],
                       ['bottom', 'left', 'u_square'],
                       ['bottom', 'center'],
                       ['bottom', 'right', 'u_square'],
                       ['top', 'right', 'u_square']],
                      face_type='hexagon')

        # Six top-left faces, rest defined via symmetry
        # Top square
        self.add_face(['square', 'top', 'center'],
                      [['top', 'left', 'v_square'],
                       ['top', 'right', 'v_square'],
                       [['top'], ['bottom', 'right', 'v_square']],
                       [['top'], ['bottom', 'left', 'v_square']]],
                      face_type='square', v_boundary=True)
        # Left square
        self.add_face(['square', 'middle', 'left'],
                      [['top', 'left', 'u_square'],
                       ['bottom', 'left', 'u_square'],
                       [['left'], ['bottom', 'right', 'u_square']],
                       [['left'], ['top', 'right', 'u_square']]],
                      face_type='square', u_boundary=True)
        # Interior square
        self.add_face(['square', 'top', 'left'],
                      [['top', 'left', 'v_square'],
                       ['top', 'center'],
                       ['top', 'left', 'u_square'],
                       ['top', 'left', 'u_boundary']],
                      face_type='square')
        # Upper triangle
        self.add_face(['tri', 'top', 'center'],
                      [['top', 'center'],
                       ['top', 'left', 'v_square'],
                       ['top', 'right', 'v_square']],
                      face_type='triangle')
        # Left triangle
        self.add_face(['tri', 'top', 'left'],
                      [['top', 'left', 'u_square'],
                       ['top', 'left', 'u_boundary'],
                       [['left'], ['top', 'right', 'u_square']]],
                      face_type='triangle', u_boundary=True)
        # Corner hexagon
        self.add_face(['hex', 'top', 'left'],
                      [['top', 'left', 'v_square'],
                       ['top', 'left', 'u_boundary'],
                       [['left'], ['top', 'right', 'v_square']],
                       [['left', 'top'], ['bottom', 'right', 'v_square']],
                       [['top'], ['bottom', 'left', 'u_boundary']],
                       [['top'], ['bottom', 'left', 'v_square']]],
                      face_type='hexagon', corner=True)


class HexSquareTriTessagon(Tessagon):
    tile_class = HexSquareTriTile
    metadata = metadata
