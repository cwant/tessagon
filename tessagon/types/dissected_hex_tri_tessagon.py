from math import sqrt
from tessagon.types.dissected_hex_quad_tessagon import DissectedHexQuadTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Hexagons Dissected with Triangles',
                            num_color_patterns=1,
                            classification='laves',
                            shapes=['triangles'],
                            sides=[3],
                            uv_ratio=1.0/sqrt(3.0))


# Uses the same configuration of vertices as DissectedHexQuadTile
class DissectedHexTriTile(DissectedHexQuadTile):

    # 19 verts, 24 internal triangle faces
    #
    #  O+++++++++++++++++++O+++++++++++++++++++O
    #  ++ ++               +               ++ ++
    #  + +    ++           +           ++    + +
    #  +  +      ++        +        ++      +  +
    #  +   +         +     +     +         +   +
    #  +     +          ++ + ++          +     +
    #  +      +           +O+           +      +
    #  +       +      ++   +   ++      +       +
    #  +        +  ++      +      ++  +        +
    #  +       ++O         +         O++       +
    #  +    ++    +        +        +    ++    +
    #  +++         ++      +      ++         +++
    #  O+            +     +     +            +O
    #  +   ++         +    +    +         ++   +
    #  +      ++       +   +   +       ++      +
    #  +          ++    +  +  +    ++          +
    #  +             ++  + + +  ++             +
    #  +                 +++++                 +
    #  O+++++++++++++++++++O+++++++++++++++++++O
    #  +             ++  + + +  ++             +
    #  +          ++    +  +  +    ++          +
    #  +      ++       +   +   +       ++      +
    #  +   ++         +    +    +         ++   +
    #  ++            +     +     +            ++
    #  O++         ++      +      ++         ++O
    #  +    ++    +        +        +    ++    +
    #  +       ++O         +         O++       +
    #  +        +  +       +      ++  +        +
    #  +       +      ++   +   ++      +       +
    #  +      +           +O+           +      +
    #  +     +          ++ + ++          +     +
    #  +   +         +     +     +         +   +
    #  +  +      ++        +        ++      +  +
    #  + +    ++           +           ++    + +
    #  ++ ++               +               ++ ++
    #  O+++++++++++++++++++++++++++++++++++++++O

    def init_faces(self):
        return {'left': {'top': {'v_boundary': None,
                                 'u_boundary': None,
                                 'middle': None,
                                 'center': None,
                                 'interior1': None,  # Touches corner
                                 'interior2': None},
                         'bottom': {'v_boundary': None,
                                    'u_boundary': None,
                                    'middle': None,
                                    'center': None,
                                    'interior1': None,
                                    'interior2': None}},
                'right': {'top': {'v_boundary': None,
                                  'u_boundary': None,
                                  'middle': None,
                                  'center': None,
                                  'interior1': None,
                                  'interior2': None},
                          'bottom': {'v_boundary': None,
                                     'u_boundary': None,
                                     'middle': None,
                                     'center': None,
                                     'interior1': None,
                                     'interior2': None}}}

    def calculate_faces(self):
        self.add_face(['left', 'top', 'v_boundary'],
                      [['left', 'top', 'corner'],
                       ['center', 'top', 'v_boundary'],
                       ['center', 'top', 'interior']])

        self.add_face(['left', 'top', 'interior1'],
                      [['left', 'top', 'corner'],
                       ['center', 'top', 'interior'],
                       ['left', 'top', 'interior']])

        self.add_face(['left', 'top', 'u_boundary'],
                      [['left', 'top', 'corner'],
                       ['left', 'top', 'interior'],
                       ['left', 'top', 'u_boundary']])

        self.add_face(['left', 'top', 'middle'],
                      [['center', 'middle'],
                       ['left', 'middle'],
                       ['left', 'top', 'u_boundary']])

        self.add_face(['left', 'top', 'interior2'],
                      [['left', 'top', 'interior'],
                       ['center', 'middle'],
                       ['left', 'top', 'u_boundary']])

        self.add_face(['left', 'top', 'center'],
                      [['center', 'middle'],
                       ['left', 'top', 'interior'],
                       ['center', 'top', 'interior']])

    def color_pattern1(self):
        self.color_paths([
            ['left', 'top', 'v_boundary'],
            ['left', 'top', 'u_boundary'],
            ['left', 'top', 'middle'],
            ['left', 'top', 'center'],

            ['right', 'top', 'interior1'],
            ['right', 'top', 'interior2'],

            ['right', 'bottom', 'v_boundary'],
            ['right', 'bottom', 'u_boundary'],
            ['right', 'bottom', 'middle'],
            ['right', 'bottom', 'center'],

            ['left', 'bottom', 'interior1'],
            ['left', 'bottom', 'interior2'],
        ], 1, 0)


class DissectedHexTriTessagon(Tessagon):
    tile_class = DissectedHexTriTile
    metadata = metadata
