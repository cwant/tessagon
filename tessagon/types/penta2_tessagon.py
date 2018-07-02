from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Other Pentagons',
                            classification='laves',
                            shapes=['pentagons'],
                            sides=[5])


class Penta2Tile(Tile):
    # 11 verts, 6 faces (2 internal, 4 on boundary)
    #
    #     O---O
    #     |...|
    #     O...O
    #     .\./.
    #  ^  ..O..
    #  |  ..|..
    #  |  --O--
    #  |  ..|..
    #     ..O..
    #  V  ./.\.
    #     O...O
    #     |...|
    #     O---O
    #
    #    U ----->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
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

    def init_faces(self):
        return {'left': {'top': None,
                         'bottom': None},
                'right': {'top': None,
                          'bottom': None},
                'center': {'top': None,
                           'bottom': None}}

    def calculate_verts(self):
        v_unit = 1.0 / (2.0 + sqrt(3.0))
        v0 = 0
        v1 = v_unit * 0.5 * (1.0 + 1.0 / sqrt(3.0))
        v2 = 0.5 - v1

        self.add_vert(['left', 'bottom', 'corner'], 0, v0, corner=True)
        self.add_vert(['left', 'bottom', 'u_boundary'], 0, v1,
                      u_boundary=True)
        self.add_vert(['center', 'bottom'], 0.5, v2)
        self.add_vert(['center', 'middle'], 0.5, 0.5)

    def calculate_faces(self):
        self.add_face(['center', 'bottom'],
                      [['left', 'bottom', 'corner'],
                       ['left', 'bottom', 'u_boundary'],
                       ['center', 'bottom'],
                       ['right', 'bottom', 'u_boundary'],
                       ['right', 'bottom', 'corner']])
        self.add_face(['left', 'bottom'],
                      [['center', 'middle'],
                       ['center', 'bottom'],
                       ['left', 'bottom', 'u_boundary'],
                       [['left'], ['center', 'bottom']],
                       [['left'], ['center', 'middle']]], u_boundary=True)


class Penta2Tessagon(Tessagon):
    tile_class = Penta2Tile
    metadata = metadata
