from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import left_tile, left_top_tile, top_tile
metadata = TessagonMetadata(name='Hexagons and Triangles',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['hexagons', 'triangles'],
                            sides=[6, 3],
                            uv_ratio=1.0/sqrt(3.0))


class HexTriTile(Tile):
    #    ....o....
    #    .../.\...
    #  ^ --o---o--
    #  | ./.....\.
    #  | o.......o
    #  | .\...../.
    #  | --o---o--
    #    ...\./...
    #  V ....o ...
    #
    #     U ------>

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'top': None,
                'left': {'top': None,
                         'middle': None,
                         'bottom': None},
                'right':  {'top': None,
                           'middle': None,
                           'bottom': None},
                'bottom': None}

    def init_faces(self):
        return {'center': {'top': None,
                           'middle': None,
                           'bottom': None},
                'left': {'top': {'triangle': None, 'hexagon': None},
                         'bottom': {'triangle': None, 'hexagon': None}},
                'right': {'top': {'triangle': None, 'hexagon': None},
                          'bottom': {'triangle': None, 'hexagon': None}}}

    def calculate_verts(self):
        # top left verts
        self.add_vert('top', 0.5, 1, v_boundary=True)
        self.add_vert(['left', 'top'], 0.25, 0.75)
        self.add_vert(['left', 'middle'], 0, 0.5, u_boundary=True)

    def calculate_faces(self):
        # Middle hexagon
        self.add_face(['center', 'middle'],
                      [['left', 'top'],
                       ['left', 'middle'],
                       ['left', 'bottom'],
                       ['right', 'bottom'],
                       ['right', 'middle'],
                       ['right', 'top']],
                      face_type='hexagon')
        # Interior top triangle
        self.add_face(['center', 'top'],
                      [['top'],
                       ['left', 'top'],
                       ['right', 'top']],
                      face_type='triangle')

        # Exterior left triangle
        self.add_face(['left', 'top', 'triangle'],
                      [['left', 'top'],
                       ['left', 'middle'],
                       # Verts on neighbor tiles
                       left_tile(['right', 'top'])],
                      face_type='triangle', u_boundary=True)

        # Exterior top-left hexagon
        self.add_face(['left', 'top', 'hexagon'],
                      [['top'],
                       ['left', 'top'],
                       # Verts on neighbor tiles
                       left_tile(['right', 'top']),
                       left_tile('top'),
                       left_top_tile(['right', 'bottom']),
                       top_tile(['left', 'bottom'])],
                      face_type='hexagon', corner=True)

    def color_pattern1(self):
        # Color the hexagons
        self.color_face(['center', 'middle'], 1)
        self.color_face(['left', 'top', 'hexagon'], 1)


class HexTriTessagon(Tessagon):
    tile_class = HexTriTile
    metadata = metadata
