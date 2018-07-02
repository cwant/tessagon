from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

# TODO: gulp, 'octagon' does not begin with 'octo'

metadata = TessagonMetadata(name='Octagons and Squares',
                            classification='archimedean',
                            shapes=['octagons', 'squares'],
                            sides=[8, 4])


class OctoTile(Tile):
    # ^  ..o-o..
    # |  ./...\.
    # |  o.....o
    # |  |.....|
    # |  o.....o
    # |  .\.../.
    #    ..o-o..
    # V
    #    U ---->

    CORNER_TO_VERT_RATIO = 1.0 / (2.0 + sqrt(2))

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': {'u_boundary': None,
                                 'v_boundary': None},
                         'bottom': {'u_boundary': None,
                                    'v_boundary': None}},
                'right': {'top': {'u_boundary': None,
                                  'v_boundary': None},
                          'bottom': {'u_boundary': None,
                                     'v_boundary': None}}}

    def init_faces(self):
        return {'middle': None,
                'left': {'top': None,
                         'bottom': None},
                'right': {'top': None,
                          'bottom': None}}

    def calculate_verts(self):
        self.add_vert(['left', 'top', 'v_boundary'],
                      self.CORNER_TO_VERT_RATIO, 1, v_boundary=True)
        self.add_vert(['left', 'top', 'u_boundary'],
                      0, 1.0 - self.CORNER_TO_VERT_RATIO, u_boundary=True)

    def calculate_faces(self):
        # Middle interior face
        self.add_face('middle', [['left', 'top', 'v_boundary'],
                                 ['left', 'top', 'u_boundary'],
                                 ['left', 'bottom', 'u_boundary'],
                                 ['left', 'bottom', 'v_boundary'],
                                 ['right', 'bottom', 'v_boundary'],
                                 ['right', 'bottom', 'u_boundary'],
                                 ['right', 'top', 'u_boundary'],
                                 ['right', 'top', 'v_boundary']])

        # Four faces, define top left corner, others via symmetry
        self.add_face(['left', 'top'],
                      [['left', 'top', 'v_boundary'],
                       ['left', 'top', 'u_boundary'],
                       # Verts on neighbor tiles
                       [['left'], ['right', 'top', 'v_boundary']],
                       [['top'], ['left', 'bottom', 'u_boundary']]],
                      corner=True)


class OctoTessagon(Tessagon):
    tile_class = OctoTile
    metadata = metadata
