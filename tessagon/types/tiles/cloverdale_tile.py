from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, top_left_tile, top_tile

# See the SVG for decomposition:
# https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/cloverdale.svg


class CloverdaleTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': {'inner': None,
                                 'outer': None,
                                 'u_border': None,
                                 'v_border': None},
                         'middle': {'inner': None,
                                    'outer': None},
                         'bottom': {'inner': None,
                                    'outer': None,
                                    'u_border': None,
                                    'v_border': None}},
                'center': {'top': {'inner': None,
                                   'outer': None},
                           'middle': None,
                           'bottom': {'inner': None,
                                      'outer': None}},
                'right': {'top': {'inner': None,
                                  'outer': None,
                                  'u_border': None,
                                  'v_border': None},
                          'middle': {'inner': None,
                                     'outer': None},
                          'bottom': {'inner': None,
                                     'outer': None,
                                     'u_border': None,
                                     'v_border': None}}}

    def init_faces(self):
        return {'left': {'top': {'square': None,
                                 'u_pentagon': None,
                                 'v_pentagon': None},
                         'bottom': {'square': None,
                                    'u_pentagon': None,
                                    'v_pentagon': None},
                         'middle': {'square': None}},
                'center': {'top': {'square': None},
                           'bottom': {'square': None}},
                'right': {'top': {'square': None,
                                  'u_pentagon': None,
                                  'v_pentagon': None},
                          'bottom': {'square': None,
                                     'u_pentagon': None,
                                     'v_pentagon': None},
                          'middle': {'square': None}}}

    def calculate_verts(self):
        # a is the side length of square
        # c is half diagonal of square
        c = 1.0 / (sqrt(2.0) + 4.0)
        a = sqrt(2.0) * c

        # left top corner
        self.add_vert(['left', 'top', 'inner'],
                      a / 2.0 + c, 1.0 - (a / 2.0 + c))
        self.add_vert(['left', 'top', 'outer'], a / 2.0, 1.0 - a / 2.0)
        self.add_vert(['left', 'top', 'u_border'],
                      0.0, 1.0 - a / 2.0, u_boundary=True)
        self.add_vert(['left', 'top', 'v_border'],
                      a / 2.0, 1.0, v_boundary=True)

        self.add_vert(['left', 'middle', 'inner'], a / 2.0, 0.5)
        self.add_vert(['left', 'middle', 'outer'], 0.0, 0.5, u_boundary=True)

        self.add_vert(['center', 'top', 'inner'], 0.5, 1.0 - a / 2.0)
        self.add_vert(['center', 'top', 'outer'], 0.5, 1.0, v_boundary=True)
        self.add_vert(['center', 'middle'], 0.5, 0.5)

    def calculate_faces(self):
        self.add_face(['left', 'top', 'square'],
                      [['left', 'top', 'u_border'],
                       ['left', 'top', 'outer'],
                       ['left', 'top', 'v_border'],
                       top_tile(['left', 'bottom', 'outer']),
                       top_tile(['left', 'bottom', 'u_border']),
                       top_left_tile(['right', 'bottom', 'outer']),
                       left_tile(['right', 'top', 'v_border']),
                       left_tile(['right', 'top', 'outer'])],
                      corner=True)

        self.add_face(['left', 'top', 'u_pentagon'],
                      [['left', 'middle', 'outer'],
                       ['left', 'middle', 'inner'],
                       ['left', 'top', 'inner'],
                       ['left', 'top', 'outer'],
                       ['left', 'top', 'u_border']])

        self.add_face(['left', 'top', 'v_pentagon'],
                      [['left', 'top', 'outer'],
                       ['left', 'top', 'inner'],
                       ['center', 'top', 'inner'],
                       ['center', 'top', 'outer'],
                       ['left', 'top', 'v_border']])

        self.add_face(['center', 'top', 'square'],
                      [['right', 'top', 'inner'],
                       ['center', 'top', 'inner'],
                       ['left', 'top', 'inner'],
                       ['center', 'middle']])

        self.add_face(['left', 'middle', 'square'],
                      [['left', 'top', 'inner'],
                       ['left', 'middle', 'inner'],
                       ['left', 'bottom', 'inner'],
                       ['center', 'middle']])

    def color_pattern1(self):
        self.color_face(['left', 'top', 'square'], 1)
        self.color_face(['left', 'middle', 'square'], 1)
        self.color_face(['center', 'top', 'square'], 1)
        self.color_face(['right', 'middle', 'square'], 1)
        self.color_face(['center', 'bottom', 'square'], 1)
        self.color_face(['left', 'top', 'u_pentagon'], 0)
        self.color_face(['left', 'top', 'v_pentagon'], 0)
