from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

# Will my brain survive this one?

metadata = TessagonMetadata(name='Dodecagons, Hexagons, and Squares',
                            classification='archimedean',
                            shapes=['dodecagons', 'hexagons', 'squares'],
                            sides=[12, 6, 4])


class DodecaTile(Tile):
    # 24 verts, 19 faces (7 internal, 12 on boundary)
    # The angles make it hard to draw all edges, some excluded

    #     .......|.4.|.......
    #     .      o---o      .
    #     .  12 /     \  12 .
    #     .    o   6   o    .
    #     --o ..\     /.. o--
    #     .  \.4.o---o.4./  .
    #  ^  . 6 o         o 6 .
    #  |  .  /           \  .
    #  |  --o             o--
    #  |  .4|      12     |4. Number is verts in face
    #  |  --o             o--
    #     .  \           /  .
    #  V  . 6 o         o 6 .
    #     .  /...o---o...\  .
    #     --o.4./     \.4.o--
    #     .    o   6   o    .
    #     .     \     /     .
    #     .  12  o---o  12  .
    #     .......|.4.|.......
    #
    #            U ---->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        # u_square means on the square that is on the U-boundary
        return {'top': {'left': {'u_square': None,
                                 'v_square': None,
                                 # Inner square, sort v-distance from middle
                                 'sq1': None,
                                 'sq2': None,
                                 'sq3': None,
                                 'sq4': None},
                        'right': {'u_square': None,
                                  'v_square': None,
                                  'sq1': None,
                                  'sq2': None,
                                  'sq3': None,
                                  'sq4': None}},
                'bottom': {'left': {'u_square': None,
                                    'v_square': None,
                                    'sq1': None,
                                    'sq2': None,
                                    'sq3': None,
                                    'sq4': None},
                           'right': {'u_square': None,
                                     'v_square': None,
                                     'sq1': None,
                                     'sq2': None,
                                     'sq3': None,
                                     'sq4': None}}}

    def init_faces(self):
        return {'dodec': {'top': {'left': None,
                                  'right': None},
                          'bottom': {'left': None,
                                     'right': None},
                          'middle': None},
                'hex': {'top': {'left': None,
                                'center': None,
                                'right': None},
                        'bottom': {'left': None,
                                   'center': None,
                                   'right': None}},
                'square': {'top': {'left': None,
                                   'center': None,
                                   'right': None},
                           'bottom': {'left': None,
                                      'center': None,
                                      'right': None},
                           'middle': {'left': None,
                                      'right': None}}}

    def calculate_verts(self):
        # u_unit is the length of the edges expressed as a
        # proportion of the tile
        u_unit = 1.0 / (3.0 + sqrt(3))
        u_h = 0.5*sqrt(3)*u_unit  # height of triangle of side u_unit

        u1 = 0.5*u_unit
        u2 = 0.5 - u1 - u_h
        u3 = 0.5 - u_unit
        u4 = 0.5 - u1

        v_unit = 1.0 / (3.0*(1.0 + sqrt(3)))
        v_h = 0.5*sqrt(3)*v_unit  # height of triangle of side v_unit
        v1 = 1.0 - 0.5*v_unit
        v2 = v1 - v_h
        v3 = 0.5 + 2*v_h + 0.5*v_unit
        v4 = 0.5 + v_h + v_unit
        v5 = 0.5 + v_h + 0.5*v_unit
        v6 = 0.5 + 0.5*v_unit

        # Define top left region, other verts defined through symmetry
        self.add_vert(['top', 'left', 'v_square'], u4, v1)
        self.add_vert(['top', 'left', 'u_square'], u1, v6)
        self.add_vert(['top', 'left', 'sq1'], u2, v5)
        self.add_vert(['top', 'left', 'sq2'], u4, v4)
        self.add_vert(['top', 'left', 'sq3'], u1, v3)
        self.add_vert(['top', 'left', 'sq4'], u3, v2)

    def calculate_faces(self):
        # Top left Dodecagon
        self.add_face(['dodec', 'top', 'left'],
                      [['top', 'left', 'v_square'],
                       ['top', 'left', 'sq4'],
                       ['top', 'left', 'sq3'],
                       [['left'], ['top', 'right', 'sq3']],
                       [['left'], ['top', 'right', 'sq4']],
                       [['left'], ['top', 'right', 'v_square']],
                       [['left', 'top'], ['bottom', 'right', 'v_square']],
                       [['left', 'top'], ['bottom', 'right', 'sq4']],
                       [['left', 'top'], ['bottom', 'right', 'sq3']],
                       [['top'], ['bottom', 'left', 'sq3']],
                       [['top'], ['bottom', 'left', 'sq4']],
                       [['top'], ['bottom', 'left', 'v_square']]],
                      face_type='dodecagon', corner=True)
        # Middle Dodecagon
        self.add_face(['dodec', 'middle'],
                      [['top', 'left', 'u_square'],
                       ['top', 'left', 'sq1'],
                       ['top', 'left', 'sq2'],
                       ['top', 'right', 'sq2'],
                       ['top', 'right', 'sq1'],
                       ['top', 'right', 'u_square'],
                       ['bottom', 'right', 'u_square'],
                       ['bottom', 'right', 'sq1'],
                       ['bottom', 'right', 'sq2'],
                       ['bottom', 'left', 'sq2'],
                       ['bottom', 'left', 'sq1'],
                       ['bottom', 'left', 'u_square']],
                      face_type='dodecagon')
        # Upper square
        self.add_face(['square', 'top', 'center'],
                      [['top', 'left', 'v_square'],
                       ['top', 'right', 'v_square'],
                       [['top'], ['bottom', 'right', 'v_square']],
                       [['top'], ['bottom', 'left', 'v_square']]],
                      face_type='square', v_boundary=True)
        # Left square
        self.add_face(['square', 'middle', 'left'],
                      [['top', 'left', 'u_square'],
                       ['bottom', 'left', 'u_square'],
                       [['left'], ['bottom', 'right', 'u_square']],
                       [['left'], ['top', 'right', 'u_square']]],
                      face_type='square', u_boundary=True)
        # Interior square
        self.add_face(['square', 'top', 'left'],
                      [['top', 'left', 'sq1'],
                       ['top', 'left', 'sq2'],
                       ['top', 'left', 'sq4'],
                       ['top', 'left', 'sq3']],
                      face_type='square')
        # Top Hex
        self.add_face(['hex', 'top', 'center'],
                      [['top', 'left', 'sq2'],
                       ['top', 'left', 'sq4'],
                       ['top', 'left', 'v_square'],
                       ['top', 'right', 'v_square'],
                       ['top', 'right', 'sq4'],
                       ['top', 'right', 'sq2']],
                      face_type='hexagon')
        # Left Hex
        self.add_face(['hex', 'top', 'left'],
                      [['top', 'left', 'sq3'],
                       ['top', 'left', 'sq1'],
                       ['top', 'left', 'u_square'],
                       [['left'], ['top', 'right', 'u_square']],
                       [['left'], ['top', 'right', 'sq1']],
                       [['left'], ['top', 'right', 'sq3']]],
                      face_type='hexagon', u_boundary=True)


class DodecaTessagon(Tessagon):
    tile_class = DodecaTile
    metadata = metadata
