from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import left_tile, top_tile

metadata = TessagonMetadata(name='Rhombuses',
                            num_color_patterns=2,
                            classification='laves',
                            shapes=['rhombuses'],
                            sides=[4],
                            uv_ratio=1.0/sqrt(3.0))


class RhombusTile(Tile):
    #    ..o..
    #    ./|\.
    #    o.|.o
    # ^  |.o.|
    # |  |/.\|
    # |  o...o
    # |  |\./|
    # |  |.o.|
    # |  o.|.o
    #    .\|/.
    # V  ..o..
    #
    #   U --->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': None, 'middle': None, 'bottom': None},
                'center': {'top': {'boundary': None, 'interior': None},
                           'bottom': {'boundary': None, 'interior': None}},
                'right': {'top': None, 'middle': None, 'bottom': None}}

    def init_faces(self):
        return {'middle': None,
                'left': {'top': {'interior': None, 'exterior': None},
                         'bottom': {'interior': None, 'exterior': None}},
                'right': {'top': {'interior': None, 'exterior': None},
                          'bottom': {'interior': None, 'exterior': None}}}

    def calculate_verts(self):
        # 10 verts, do top left quadrant, others via symmetry
        self.add_vert(['center', 'top', 'boundary'], 0.5, 1, v_boundary=True)
        self.add_vert(['left', 'top'], 0, 5.0/6.0, u_boundary=True)
        self.add_vert(['center', 'top', 'interior'], 0.5, 2.0/3.0)
        self.add_vert(['left', 'middle'], 0, 1.0/2.0, u_boundary=True)

    def calculate_faces(self):
        # One middle face
        self.add_face('middle',
                      [['center', 'top', 'interior'],
                       ['left', 'middle'],
                       ['center', 'bottom', 'interior'],
                       ['right', 'middle']], face_type='horizontal')
        # Eight others, define only left top, others by symmetry
        self.add_face(['left', 'top', 'interior'],
                      [['center', 'top', 'boundary'],
                       ['left', 'top'],
                       ['left', 'middle'],
                       ['center', 'top', 'interior']], face_type='upward')
        self.add_face(['left', 'top', 'exterior'],
                      [['center', 'top', 'boundary'],
                       ['left', 'top'],
                       # Verts on neighbor tile
                       left_tile(['center', 'top', 'boundary']),
                       top_tile(['left', 'bottom'])],
                      face_type='horizontal', corner=True)

    def color_pattern1(self):
        self.color_face(['middle'], 1)
        self.color_face(['left', 'top', 'exterior'], 1)

        self.color_face(['left', 'top', 'interior'], 2)
        self.color_face(['right', 'bottom', 'interior'], 2)

    def color_pattern2(self):
        self.color_face(['left', 'top', 'interior'], 1)
        self.color_face(['right', 'top', 'interior'], 1)

        self.color_face(['left', 'bottom', 'interior'], 2)
        self.color_face(['right', 'bottom', 'interior'], 2)


class RhombusTessagon(Tessagon):
    tile_class = RhombusTile
    metadata = metadata
