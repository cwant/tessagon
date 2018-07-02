from math import sqrt
from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Dodecagons and Triangles',
                            classification='archimedean',
                            shapes=['dodecagons', 'triangles'],
                            sides=[12, 3])


class DodecaTriTile(Tile):
    # 14 verts, 11 faces (3 internal, 8 on boundary)
    # The angles make it hard to draw all edges, some excluded

    #     . ....|3.o---o.3|......
    #  ^  .     o         o     .
    #  |  . 12 /           \ 12 .
    #  |  .   o             o   .
    #  |  .-o3|      12     |3o-. Number is verts in face
    #  |  .   o             o   .
    #     .    \           /    .
    #  V  . 12  o         o 12  .
    #     . ....|3.o---o.3|......
    #
    #            U ---->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        # u_square means on the square that is on the U-boundary
        return {'left': {'top': {'v_boundary': None,
                                 'diag': None,
                                 'tri': None},  # on the triangle
                         'middle': None,
                         'bottom': {'v_boundary': None,
                                    'diag': None,
                                    'tri': None}},
                'right': {'top': {'v_boundary': None,
                                  'diag': None,
                                  'tri': None},  # on the triangle
                          'middle': None,
                          'bottom': {'v_boundary': None,
                                     'diag': None,
                                     'tri': None}}}

    def init_faces(self):
        return {'dodec': {'left': {'top': None,
                                   'bottom': None},
                          'right': {'top': None,
                                    'bottom': None},
                          'center': None},
                'tri': {'left': {'top': None,
                                 'middle': None,
                                 'bottom': None},
                        'right': {'top': None,
                                  'middle': None,
                                  'bottom': None}}}

    def calculate_verts(self):
        # u_unit is the length of the edges expressed as a
        # proportion of the tile
        u_unit = 1.0 / (3.0 + 2.0 * sqrt(3))
        u_h = 0.5*sqrt(3)*u_unit  # height of triangle of side u_unit

        u1 = 0.5*u_unit
        u2 = u1 + u_h
        u3 = u2 + u1
        u4 = u3 + u_h

        v_unit = 1.0 / (2.0 + sqrt(3))
        v_h = 0.5*sqrt(3)*v_unit  # height of triangle of side v_unit
        v1 = 0
        v2 = 0.5 * v_unit
        v3 = v2 + v_h
        v4 = 0.5

        # Sweet symmetry makes this easy work
        self.add_vert(['left', 'middle'], u1, v4)  # 2 verts added
        self.add_vert(['left', 'bottom', 'v_boundary'], u4, v1,
                      v_boundary=True)  # 4 verts
        self.add_vert(['left', 'bottom', 'diag'], u3, v2)  # 4 verts
        self.add_vert(['left', 'bottom', 'tri'], u2, v3)  # 4 verts

    def calculate_faces(self):
        # Top left Dodecagon
        self.add_face(['dodec', 'left', 'bottom'],
                      [['left', 'middle'],
                       ['left', 'bottom', 'tri'],
                       ['left', 'bottom', 'diag'],
                       [['bottom'], ['left', 'top', 'diag']],
                       [['bottom'], ['left', 'top', 'tri']],
                       [['bottom'], ['left', 'middle']],
                       [['bottom', 'left'], ['right', 'middle']],
                       [['bottom', 'left'], ['right', 'top', 'tri']],
                       [['bottom', 'left'], ['right', 'top', 'diag']],
                       [['left'], ['right', 'bottom', 'diag']],
                       [['left'], ['right', 'bottom', 'tri']],
                       [['left'], ['right', 'middle']]],
                      face_type='dodecagon', corner=True)

        # Middle Dodecagon
        self.add_face(['dodec', 'center'],
                      [['left', 'bottom', 'tri'],
                       ['left', 'bottom', 'diag'],
                       ['left', 'bottom', 'v_boundary'],
                       ['right', 'bottom', 'v_boundary'],
                       ['right', 'bottom', 'diag'],
                       ['right', 'bottom', 'tri'],
                       ['right', 'top', 'tri'],
                       ['right', 'top', 'diag'],
                       ['right', 'top', 'v_boundary'],
                       ['left', 'top', 'v_boundary'],
                       ['left', 'top', 'diag'],
                       ['left', 'top', 'tri']],
                      face_type='dodecagon')

        # Left triangle
        self.add_face(['tri', 'left', 'middle'],
                      [['left', 'top', 'tri'],
                       ['left', 'bottom', 'tri'],
                       ['left', 'middle']],
                      face_type='triangle')

        # bottom-left triangle
        self.add_face(['tri', 'left', 'bottom'],
                      [['left', 'bottom', 'diag'],
                       ['left', 'bottom', 'v_boundary'],
                       [['bottom'], ['left', 'top', 'diag']]],
                      face_type='triangle', v_boundary=True)


class DodecaTriTessagon(Tessagon):
    tile_class = DodecaTriTile
    metadata = metadata
