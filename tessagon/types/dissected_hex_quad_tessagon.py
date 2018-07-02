from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Hexagons Dissected with Quads',
                            classification='laves',
                            shapes=['quads'],
                            sides=[4])


class DissectedHexQuadTile(Tile):
    # 19 verts, 14 quad faces (10 internal, 4 on boundary)
    #
    #  O+++++++++++++++++++O+++++++++++++++++++O
    #   +                  +                  +
    #    +                 +                 +
    #     +                +                +
    #      +               +               +
    #        +             +             +
    #         +           +O+           +
    #          +      ++       ++      +
    #           +  ++             ++  +
    #          ++O                   O++
    #       ++    +                 +    ++
    #   ++         ++             ++         ++
    #  O             +           +             O
    #  +              +         +              +
    #  +               +       +               +
    #  +                +     +                +
    #  +                 +   +                 +
    #  O+++++++++++++++++++O+++++++++++++++++++O
    #  +                  + +                  +
    #  +                 +   +                 +
    #  +                +     +                +
    #  +               +       +               +
    #  +              +         +              +
    #  O             +           +             O
    #   ++         ++             ++         ++
    #       ++    +                 +    ++
    #          ++O                   O++
    #           +  ++             ++  +
    #          +      ++       ++      +
    #         +           + +           +
    #        +             O             +
    #      +               +               +
    #     +                +                +
    #    +                 +                 +
    #   +                  +                  +
    #  O+++++++++++++++++++O+++++++++++++++++++O

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': {'corner': None,
                                 'interior': None,
                                 'u_boundary': None},
                         'middle': None,
                         'bottom': {'corner': None,
                                    'interior': None,
                                    'u_boundary': None}},
                'right': {'top': {'corner': None,
                                  'interior': None,
                                  'u_boundary': None},
                          'middle': None,
                          'bottom': {'corner': None,
                                     'interior': None,
                                     'u_boundary': None}},
                'center': {'middle': None,
                           'top': {'v_boundary': None,
                                   'interior': None},
                           'bottom': {'v_boundary': None,
                                      'interior': None}}}

    def init_faces(self):
        return {'left': {'top': {'v_boundary': None,
                                 'u_boundary': None,
                                 'middle': None},
                         'bottom': {'v_boundary': None,
                                    'u_boundary': None,
                                    'middle': None}},
                'right': {'top': {'v_boundary': None,
                                  'u_boundary': None,
                                  'middle': None},
                          'bottom': {'v_boundary': None,
                                     'u_boundary': None,
                                     'middle': None}},
                'center': {'top': None,
                           'bottom': None}}

    def calculate_verts(self):
        self.add_vert(['left', 'top', 'corner'], 0, 1, corner=True)
        self.add_vert(['left', 'top', 'interior'], 0.25, 0.75)
        self.add_vert(['left', 'top', 'u_boundary'], 0, 2.0/3.0,
                      u_boundary=True)

        self.add_vert(['left', 'middle'], 0, 0.5, u_boundary=True)

        self.add_vert(['center', 'middle'], 0.5, 0.5)

        self.add_vert(['center', 'top', 'v_boundary'], 0.5, 1.0,
                      v_boundary=True)
        self.add_vert(['center', 'top', 'interior'], 0.5, 5.0/6.0)

    def calculate_faces(self):
        self.add_face(['left', 'top', 'v_boundary'],
                      [['left', 'top', 'corner'],
                       ['center', 'top', 'v_boundary'],
                       ['center', 'top', 'interior'],
                       ['left', 'top', 'interior']])

        self.add_face(['left', 'top', 'u_boundary'],
                      [['left', 'top', 'corner'],
                       ['left', 'top', 'interior'],
                       ['left', 'top', 'u_boundary'],
                       [['left'], ['right', 'top', 'interior']]],
                      u_boundary=True)

        self.add_face(['left', 'top', 'middle'],
                      [['left', 'top', 'interior'],
                       ['center', 'middle'],
                       ['left', 'middle'],
                       ['left', 'top', 'u_boundary']])

        self.add_face(['center', 'top'],
                      [['center', 'middle'],
                       ['left', 'top', 'interior'],
                       ['center', 'top', 'interior'],
                       ['right', 'top', 'interior']])


class DissectedHexQuadTessagon(Tessagon):
    tile_class = DissectedHexQuadTile
    metadata = metadata
