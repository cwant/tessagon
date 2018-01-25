from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.types.dissected_hex_quad_tessagon import DissectedHexQuadTile

# Uses the same configuration of vertices as DissectedHexQuadTile
class DissectedHexTriTile(DissectedHexQuadTile):

  # 19 verts, 24 internal triange faces
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

  pass

class DissectedHexTriTessagon(Tessagon):
  tile_class = DissectedHexTriTile
