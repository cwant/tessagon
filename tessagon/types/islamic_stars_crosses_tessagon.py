from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import left_tile, top_left_tile, top_tile

metadata = TessagonMetadata(name='Islamic Stars and Crosses',
                            num_color_patterns=1,
                            classification='non_convex',
                            shapes=['stars', 'crosses'],
                            sides=[16],
                            uv_ratio=1.0)


class IslamicStarsCrossesTile(Tile):
    # See page 9 of "Islamic Design" by Daud Sutton
    #
    # ......o......
    # ...../.\.....
    # ..o-o...o-o..
    # ..|.......|..
    # ..o.......o..
    # ./.........\.
    # o...........o
    # .\........./.
    # ..o.......o..
    # ..|.......|..
    # ..o-o...o-o..
    # .....\./.....
    # ......o......

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': {'v_dominant': None,
                                 'point': None,
                                 'u_dominant': None},
                         'middle': None,
                         'bottom': {'v_dominant': None,
                                    'point': None,
                                    'u_dominant': None}},
                'center': {'top': None,
                           'bottom': None},
                'right': {'top': {'v_dominant': None,
                                  'point': None,
                                  'u_dominant': None},
                          'middle': None,
                          'bottom': {'v_dominant': None,
                                     'point': None,
                                     'u_dominant': None}}}

    def init_faces(self):
        return {'left': {'top': None,
                         'bottom': None},
                'center': None,
                'right': {'top': None,
                          'bottom': None}}

    def calculate_verts(self):
        c = 1.0 / (2 * (sqrt(2) + 1))
        a = c / sqrt(2)

        # left top corner
        self.add_vert(['left', 'middle'], 0.0, 0.5, u_boundary=True)
        self.add_vert(['left', 'top', 'u_dominant'], a, 0.5 + a)
        self.add_vert(['left', 'top', 'point'], a, 1.0 - a)
        self.add_vert(['left', 'top', 'v_dominant'], 0.5 - a, 1.0 - a)
        self.add_vert(['center', 'top'], 0.5, 1.0, v_boundary=True)

    def calculate_faces(self):
        # Middle star
        self.add_face(['center'],
                      [['left', 'middle'],
                       ['left', 'top', 'u_dominant'],
                       ['left', 'top', 'point'],
                       ['left', 'top', 'v_dominant'],
                       ['center', 'top'],
                       ['right', 'top', 'v_dominant'],
                       ['right', 'top', 'point'],
                       ['right', 'top', 'u_dominant'],
                       ['right', 'middle'],
                       ['right', 'bottom', 'u_dominant'],
                       ['right', 'bottom', 'point'],
                       ['right', 'bottom', 'v_dominant'],
                       ['center', 'bottom'],
                       ['left', 'bottom', 'v_dominant'],
                       ['left', 'bottom', 'point'],
                       ['left', 'bottom', 'u_dominant']],
                      face_type='star')

        # Top left cross
        self.add_face(['left', 'top'],
                      [['center', 'top'],
                       ['left', 'top', 'v_dominant'],
                       ['left', 'top', 'point'],
                       ['left', 'top', 'u_dominant'],
                       ['left', 'middle'],
                       left_tile(['right', 'top', 'u_dominant']),
                       left_tile(['right', 'top', 'point']),
                       left_tile(['right', 'top', 'v_dominant']),
                       left_tile(['center', 'top']),
                       top_left_tile(['right', 'bottom', 'v_dominant']),
                       top_left_tile(['right', 'bottom', 'point']),
                       top_left_tile(['right', 'bottom', 'u_dominant']),
                       top_left_tile(['right', 'middle']),
                       top_tile(['left', 'bottom', 'u_dominant']),
                       top_tile(['left', 'bottom', 'point']),
                       top_tile(['left', 'bottom', 'v_dominant'])],
                      face_type='cross', corner=True)

    def color_pattern1(self):
        self.color_face(['left', 'top'], 1)
        self.color_face(['center'], 0)


class IslamicStarsCrossesTessagon(Tessagon):
    tile_class = IslamicStarsCrossesTile
    metadata = metadata
