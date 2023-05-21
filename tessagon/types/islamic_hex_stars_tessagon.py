from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import left_tile, top_left_tile, top_tile

metadata = TessagonMetadata(name='Islamic Hexagons and Stars',
                            num_color_patterns=1,
                            classification='non_convex',
                            shapes=['hexagons', 'stars'],
                            sides=[6, 12],
                            uv_ratio=sqrt(3.0))


class IslamicHexStarsTile(Tile):
    # See page 3 of "Islamic Design" by Daud Sutton
    # See the SVG for decomposition:
    # https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/islamic_hex_stars.svg

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': {'boundary': None,
                                 'mid': {'outer': None,
                                         'mid': None,
                                         'inner': None}},
                         'middle': {'inner': None,
                                    'outer': None},
                         'bottom': {'boundary': None,
                                    'mid': {'outer': None,
                                            'mid': None,
                                            'inner': None}}},
                'center': {'top': None,
                           'bottom': None},
                'right': {'top': {'boundary': None,
                                  'mid': {'outer': None,
                                          'mid': None,
                                          'inner': None}},
                          'middle': {'inner': None,
                                     'outer': None},
                          'bottom': {'boundary': None,
                                     'mid': {'outer': None,
                                             'mid': None,
                                             'inner': None}}},
                }

    def init_faces(self):
        return {'left': {'top': {'star': None, 'hexagon': None},
                         'middle': {'hexagon': None},
                         'bottom': {'star': None, 'hexagon': None}},
                'center': {'star': None},
                'right': {'top': {'star': None, 'hexagon': None},
                          'middle': {'hexagon': None},
                          'bottom': {'star': None, 'hexagon': None}}}

    def calculate_verts(self):
        # left verts
        self.add_vert(['left', 'top', 'boundary'], 2/12.0, 1, v_boundary=True)
        self.add_vert(['left', 'top', 'mid', 'outer'], 1/12.0, 0.75)
        self.add_vert(['left', 'top', 'mid', 'mid'], 3/12.0, 0.75)
        self.add_vert(['left', 'top', 'mid', 'inner'], 5/12.0, 0.75)
        self.add_vert(['left', 'middle', 'outer'], 0, 0.5, u_boundary=True)
        self.add_vert(['left', 'middle', 'inner'], 4/12, 0.5)

        # center vert
        self.add_vert(['center', 'top'], 0.5, 1, v_boundary=True)

    def calculate_faces(self):
        self.add_face(['left', 'top', 'star'],
                      [['left', 'top', 'boundary'],
                       ['left', 'top', 'mid', 'mid'],
                       ['left', 'top', 'mid', 'outer'],
                       ['left', 'middle', 'outer'],
                       left_tile(['right', 'top', 'mid', 'outer']),
                       left_tile(['right', 'top', 'mid', 'mid']),
                       left_tile(['right', 'top', 'boundary']),
                       top_left_tile(['right', 'bottom', 'mid', 'mid']),
                       top_left_tile(['right', 'bottom', 'mid', 'outer']),
                       top_tile(['left', 'middle', 'outer']),
                       top_tile(['left', 'bottom', 'mid', 'outer']),
                       top_tile(['left', 'bottom', 'mid', 'mid'])],
                      face_type='star', corner=True)

        self.add_face(['left', 'top', 'hexagon'],
                      [['center', 'top'],
                       ['left', 'top', 'mid', 'inner'],
                       ['left', 'top', 'mid', 'mid'],
                       ['left', 'top', 'boundary'],
                       top_tile(['left', 'bottom', 'mid', 'mid']),
                       top_tile(['left', 'bottom', 'mid', 'inner'])],
                      face_type='hexagon', v_boundary=True)

        self.add_face(['left', 'middle', 'hexagon'],
                      [['left', 'middle', 'outer'],
                       ['left', 'top', 'mid', 'outer'],
                       ['left', 'top', 'mid', 'mid'],
                       ['left', 'middle', 'inner'],
                       ['left', 'bottom', 'mid', 'mid'],
                       ['left', 'bottom', 'mid', 'outer']],
                      face_type='hexagon')

        self.add_face(['center', 'star'],
                      [['center', 'top'],
                       ['right', 'top', 'mid', 'inner'],
                       ['right', 'top', 'mid', 'mid'],
                       ['right', 'middle', 'inner'],
                       ['right', 'bottom', 'mid', 'mid'],
                       ['right', 'bottom', 'mid', 'inner'],
                       ['center', 'bottom'],
                       ['left', 'bottom', 'mid', 'inner'],
                       ['left', 'bottom', 'mid', 'mid'],
                       ['left', 'middle', 'inner'],
                       ['left', 'top', 'mid', 'mid'],
                       ['left', 'top', 'mid', 'inner']],
                      face_type='star')

    def color_pattern1(self):
        self.color_face(['left', 'top', 'star'], 1)
        self.color_face(['center', 'star'], 1)


class IslamicHexStarsTessagon(Tessagon):
    tile_class = IslamicHexStarsTile
    metadata = metadata
