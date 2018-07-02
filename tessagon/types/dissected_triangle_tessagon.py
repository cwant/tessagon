from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Dissected Triangle',
                            classification='laves',
                            shapes=['triangles'],
                            sides=[3])


class DissectedTriangleTile(Tile):
    #     11 verts:
    #
    #     O++++++++++++O      +      O++++++++++++O
    #     ++ ++         ++    +    ++         ++ ++
    #     + +   +++       +   +   +       +++   + +
    #     +  +      ++     +  +  +     ++      +  +
    #     +   +        ++   + + +   ++        +   +
    #     +    O++++++++++++++O++++++++++++++O    +
    #     +   +        ++   + + +   ++        +   +
    #     +  +      ++     +  +  +     ++      +  +
    #     + +   +++       +   +   +       +++   + +
    #     ++ ++         ++    +    ++         ++ ++
    #     O++++++++++++O      +      O++++++++++++O
    #
    #     14 faces (10 internal, 4 on boundary)
    #
    #     O++++++++++++O      +      O++++++++++++O
    #     ++ ++         ++    +    ++         ++ ++
    #     + +   +++  3    + 4 + 5 +  6    +++   + +
    #     +  +  2   ++     +  +  +     ++   7  +  +
    #     +   +        ++   + + +   ++        +   +
    #     + 1  O++++++++++++++O++++++++++++++O  8 +
    #     +   +        ++   + + +   ++        +   +
    #     +  +   9  ++     +  +  +     ++  14  +  +
    #     + +   +++  10   +   +   +  13   +++   + +
    #     ++ ++         ++    +    ++         ++ ++
    #     O++++++++++++O   11 + 12   O++++++++++++O

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': {'corner': None,
                                 'v_boundary': None},
                         'middle': None,
                         'bottom': {'corner': None,
                                    'v_boundary': None}},
                'right': {'top': {'corner': None,
                                  'v_boundary': None},
                          'middle': None,
                          'bottom': {'corner': None,
                                     'v_boundary': None}},
                'center': None}

    def init_faces(self):
        return {'left': {'top': {'center': None,
                                 'interior1': None,  # closest to center
                                 'interior2': None},
                         'middle': None,
                         'bottom': {'center': None,
                                    'interior1': None,  # closest to center
                                    'interior2': None}},
                'right': {'top': {'center': None,
                                  'interior1': None,  # closest to center
                                  'interior2': None},
                          'middle': None,
                          'bottom': {'center': None,
                                     'interior1': None,  # closest to center
                                     'interior2': None}}}

    def calculate_verts(self):
        # Four corners, via symmetry
        self.add_vert(['left', 'top', 'corner'], 0, 1, corner=True)
        # The center vert
        self.add_vert('center', 0.5, 0.5)
        # Vert on boundary
        self.add_vert(['left', 'top', 'v_boundary'], 1.0/3.0, 1,
                      v_boundary=True)
        # Interior vert
        self.add_vert(['left', 'middle'], 1.0/6.0, 0.5)

    def calculate_faces(self):
        self.add_face(['left', 'middle'],
                      [['left', 'middle'],
                       ['left', 'top', 'corner'],
                       ['left', 'bottom', 'corner']])

        self.add_face(['left', 'top', 'center'],
                      [['center'],
                       ['left', 'top', 'v_boundary'],
                       [['top'], ['center']]], v_boundary=True)

        self.add_face(['left', 'top', 'interior1'],
                      [['center'],
                       ['left', 'top', 'v_boundary'],
                       ['left', 'top', 'corner']])

        self.add_face(['left', 'top', 'interior2'],
                      [['center'],
                       ['left', 'middle'],
                       ['left', 'top', 'corner']])


class DissectedTriangleTessagon(Tessagon):
    tile_class = DissectedTriangleTile
    metadata = metadata
