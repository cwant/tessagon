from math import sqrt

from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon

class Penta2Tile(Tile):
  # 11 verts, 6 faces (2 internal, 4 on boundary)
  #     
  #     O---O
  #     |...|
  #     O...O
  #     .\./.
  #  ^  ..O..
  #  |  ..|..
  #  |  --O--
  #  |  ..|..
  #     ..O..
  #  V  ./.\.
  #     O...O
  #     |...|
  #     O...O
  #
  #    U ----->

  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)
    self.u_symmetric = True
    self.v_symmetric = False

  def init_verts(self):
    return { 'left': { 'top': { 'corner': None,
                                'u_boundary': None},

class Penta2Tessagon(Tessagon):
  tile_class = Penta2Tile
