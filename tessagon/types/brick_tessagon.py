from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import left_tile, bottom_tile

metadata = TessagonMetadata(name='Bricks',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['rectangles'],
                            sides=[4],
                            uv_ratio=1.0)


class BrickTile(Tile):
    #                 top
    #
    #    -o..o-      -o..o- r
    # ^  .|..|.    l .|..|. i
    # |  .o--o.    e .o--o. g
    # |  .|..|.    f .|..|. h
    # |  -o..o-    t -o..o- t
    # V
    #   U --->       bottom

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': None, 'middle': None, 'bottom': None},
                'right': {'top': None, 'middle': None, 'bottom': None}}

    def init_faces(self):
        return {'left': None, 'right': None, 'top': None, 'bottom': None}

    def calculate_verts(self):
        # corners: set bottom-left ... symmetry takes care of other 3 corners
        self.add_vert(['left', 'bottom'], 0.25, 0.0, v_boundary=True)

        # left middle, symmetry also creates right middle
        self.add_vert(['left', 'middle'], 0.25, 0.5)

    def calculate_faces(self):
        # Add left, symmetry gives the right side face
        self.add_face('left',
                      [['left', 'top'],
                       ['left', 'middle'],
                       ['left', 'bottom'],
                       # Verts on neighbor tiles:
                       left_tile(['right', 'bottom']),
                       left_tile(['right', 'middle']),
                       left_tile(['right', 'top'])],
                      u_boundary=True)

        # Add bottom, symmetry gives the top face
        self.add_face('bottom',
                      [['right', 'bottom'],
                       ['right', 'middle'],
                       ['left', 'middle'],
                       ['left', 'bottom'],
                       # Verts on neighbor tiles:
                       bottom_tile(['left', 'middle']),
                       bottom_tile(['right', 'middle'])],
                      v_boundary=True)

    def color_pattern1(self):
        self.color_paths([
            ['left'],
            ['right']
        ], 1, 0)


class BrickTessagon(Tessagon):
    tile_class = BrickTile
    metadata = metadata
