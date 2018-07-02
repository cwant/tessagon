from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Other Squares and Triangles',
                            classification='archimedean',
                            shapes=['squares', 'triangles'],
                            sides=[4, 3])


class SquareTri2Tile(Tile):
    # 6 verts, 11 faces (3 internal, 8 on boundary)
    #
    #  ^  ..|..
    #  |  --O--
    #  |  ./.\.
    #  |  O---O
    #     |...|
    #  V  O---O
    #     .\./.
    #     --O--
    #     ..|..
    #
    #      U ----->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': {'u_boundary': None},
                         'bottom': {'u_boundary': None}},
                'right': {'top': {'u_boundary': None},
                          'bottom': {'u_boundary': None}},
                'center': {'top': None,
                           'bottom': None}}

    def init_faces(self):
        return {'left': {'top': {'corner': None,
                                 'u_boundary': None},
                         'bottom': {'corner': None,
                                    'u_boundary': None}},
                'right': {'top': {'corner': None,
                                  'u_boundary': None},
                          'bottom': {'corner': None,
                                     'u_boundary': None}},
                'center': {'top': None,
                           'middle': None,
                           'bottom': None}}

    def calculate_verts(self):
        v_unit = 1.0 / (2 + sqrt(3))
        v1 = v_unit * 0.5
        v2 = 0.5 - v1

        # Other verts defined through symmetry
        self.add_vert(['center', 'bottom'], 0.5, v1)
        self.add_vert(['left', 'bottom', 'u_boundary'], 0, v2, u_boundary=True)

    def calculate_faces(self):
        self.add_face(['left', 'bottom', 'corner'],
                      [['center', 'bottom'],
                       [['left'], ['center', 'bottom']],
                       [['left', 'bottom'], ['center', 'top']],
                       [['bottom'], ['center', 'top']]],
                      face_type='square', corner=True)

        self.add_face(['left', 'bottom', 'u_boundary'],
                      [['center', 'bottom'],
                       ['left', 'bottom', 'u_boundary'],
                       [['left'], ['center', 'bottom']]],
                      face_type='triangle', u_boundary=True)

        self.add_face(['center', 'bottom'],
                      [['left', 'bottom', 'u_boundary'],
                       ['center', 'bottom'],
                       ['right', 'bottom', 'u_boundary']],
                      face_type='triangle')

        self.add_face(['center', 'middle'],
                      [['left', 'bottom', 'u_boundary'],
                       ['right', 'bottom', 'u_boundary'],
                       ['right', 'top', 'u_boundary'],
                       ['left', 'top', 'u_boundary']],
                      face_type='square')


class SquareTri2Tessagon(Tessagon):
    tile_class = SquareTri2Tile
    metadata = metadata
