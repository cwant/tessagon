from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import left_tile, top_tile, left_top_tile

metadata = TessagonMetadata(name='Weave',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['quads', 'rectangles'],
                            sides=[4],
                            uv_ratio=1.0,
                            extra_parameters={
                                'square_ratio': {
                                    'type': 'float',
                                    'min': 0.0,
                                    'max': 1.0,
                                    'default': 0.5,
                                    'description':
                                    'Control the size of the squares'
                                }
                            })


class WeaveTile(Tile):
    # 16 verts, 13 faces (5 internal, 8 on boundary)
    #
    #      ....|..|....  .8..|.8|.8..
    #      -o--o..o--o-  -o--o..o--o-
    #   ^  .|..|..|..|.  .|4.|..|4.|.
    #   |  .o--o--o--o.  .o--o--o--o.
    #   |  .|........|.  8|...8....|8
    #   |  .o--o--o--o.  .o--o--o--o.
    #      .|..|..|..|.  .|4.|..|4.|.
    #   V  -o--o..o--o.  -o--o..o--o.
    #      ....|..|....  8...|8.|...8
    #
    #        U ----->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True
        self.square_ratio = kwargs.get('square_ratio', 0.5)

    def init_verts(self):
        # u_square means on the square that is on the U-boundary
        return {'top': {'left': {'u_inner': {'v_inner': None,
                                             'v_outer': None},
                                 'u_outer': {'v_inner': None,
                                             'v_outer': None}},
                        'right': {'u_inner': {'v_inner': None,
                                              'v_outer': None},
                                  'u_outer': {'v_inner': None,
                                              'v_outer': None}}},
                'bottom': {'left': {'u_inner': {'v_inner': None,
                                                'v_outer': None},
                                    'u_outer': {'v_inner': None,
                                                'v_outer': None}},
                           'right': {'u_inner': {'v_inner': None,
                                                 'v_outer': None},
                                     'u_outer': {'v_inner': None,
                                                 'v_outer': None}}}}

    def init_faces(self):
        return {'square': {'top': {'left': None,
                                   'right': None},
                           'bottom': {'left': None,
                                      'right': None}},
                'oct': {'top': {'left': None,
                                'center': None,
                                'right': None},
                        'middle': {'left': None,
                                   'center': None,
                                   'right': None},
                        'bottom': {'left': None,
                                   'center': None,
                                   'right': None}}}

    def calculate_verts(self):
        half_square_size = 0.25 * self.square_ratio
        u0 = 0.25 - half_square_size
        u1 = 0.25 + half_square_size

        v0 = 0.75 - half_square_size
        v1 = 0.75 + half_square_size

        # Define top left square, other verts defined through symmetry
        self.add_vert(['top', 'left', 'u_inner', 'v_inner'], u1, v0)
        self.add_vert(['top', 'left', 'u_inner', 'v_outer'], u1, v1)
        self.add_vert(['top', 'left', 'u_outer', 'v_inner'], u0, v0)
        self.add_vert(['top', 'left', 'u_outer', 'v_outer'], u0, v1)

    def calculate_faces(self):
        # 4 internal squares (via symmetry)
        self.add_face(['square', 'top', 'left'],
                      [['top', 'left', 'u_outer', 'v_outer'],
                       ['top', 'left', 'u_inner', 'v_outer'],
                       ['top', 'left', 'u_inner', 'v_inner'],
                       ['top', 'left', 'u_outer', 'v_inner']],
                      face_type='square')

        # 1 interior strip
        self.add_face(['oct', 'middle', 'center'],
                      [['top', 'left', 'u_outer', 'v_inner'],
                       ['top', 'left', 'u_inner', 'v_inner'],
                       ['top', 'right', 'u_inner', 'v_inner'],
                       ['top', 'right', 'u_outer', 'v_inner'],
                       ['bottom', 'right', 'u_outer', 'v_inner'],
                       ['bottom', 'right', 'u_inner', 'v_inner'],
                       ['bottom', 'left', 'u_inner', 'v_inner'],
                       ['bottom', 'left', 'u_outer', 'v_inner']],
                      face_type='oct')

        # 4 corner strips
        self.add_face(['oct', 'top', 'left'],
                      [['top', 'left', 'u_inner', 'v_outer'],
                       ['top', 'left', 'u_outer', 'v_outer'],
                       left_tile(['top', 'right', 'u_outer', 'v_outer']),
                       left_tile(['top', 'right', 'u_inner', 'v_outer']),
                       left_top_tile(['bottom', 'right',
                                      'u_inner', 'v_outer']),
                       left_top_tile(['bottom', 'right',
                                      'u_outer', 'v_outer']),
                       top_tile(['bottom', 'left', 'u_outer', 'v_outer']),
                       top_tile(['bottom', 'left', 'u_inner', 'v_outer'])],
                      face_type='oct', corner=True)

        # 2 side strips
        self.add_face(['oct', 'middle', 'left'],
                      [['top', 'left', 'u_outer', 'v_outer'],
                       ['top', 'left', 'u_outer', 'v_inner'],
                       ['bottom', 'left', 'u_outer', 'v_inner'],
                       ['bottom', 'left', 'u_outer', 'v_outer'],
                       left_tile(['bottom', 'right', 'u_outer', 'v_outer']),
                       left_tile(['bottom', 'right', 'u_outer', 'v_inner']),
                       left_tile(['top', 'right', 'u_outer', 'v_inner']),
                       left_tile(['top', 'right', 'u_outer', 'v_outer'])],
                      face_type='oct', u_boundary=True)

        # 2 top/bottom strips
        self.add_face(['oct', 'top', 'center'],
                      [['top', 'left', 'u_inner', 'v_outer'],
                       ['top', 'left', 'u_inner', 'v_inner'],
                       ['top', 'right', 'u_inner', 'v_inner'],
                       ['top', 'right', 'u_inner', 'v_outer'],
                       top_tile(['bottom', 'right', 'u_inner', 'v_outer']),
                       top_tile(['bottom', 'right', 'u_inner', 'v_inner']),
                       top_tile(['bottom', 'left', 'u_inner', 'v_inner']),
                       top_tile(['bottom', 'left', 'u_inner', 'v_outer'])],
                      face_type='oct', v_boundary=True)

    def color_pattern1(self):
        self.color_face(['oct', 'top', 'center'], 1)
        self.color_face(['oct', 'middle', 'left'], 1)

        self.color_face(['oct', 'top', 'left'], 2)
        self.color_face(['oct', 'middle', 'center'], 2)


class WeaveTessagon(Tessagon):
    tile_class = WeaveTile
    metadata = metadata
