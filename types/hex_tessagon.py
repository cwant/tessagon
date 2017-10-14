from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile

class HexTile(Tile):
  #    ..|..
  #    ..o..
  # ^  ./.\.
  # |  o...o
  # |  |...|
  # |  o...o
  # |  .\./.
  #    ..o..
  # V  ..|..
  #
  #     U --->

  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)
    self.u_symmetric = True
    self.v_symmetric = True

  def init_verts(self):
    return { 'top': { 'left': None, 'center': None, 'right': None},
             'bottom': { 'left': None, 'center': None, 'right': None} }

  def init_faces(self):
    return  { 'middle': None,
              'top': { 'left': None, 'right': None},
              'bottom': { 'left': None, 'right': None} }

  def calculate_verts(self):
    self.add_vert(['top', 'center'], 0.5, 5.0/6.0)
    self.add_vert(['top', 'left'], 0, 2.0/3.0, u_boundary=True)

  def calculate_faces(self):
    self.add_face('middle', [['top', 'center'],
                             ['top', 'left'],
                             ['bottom', 'left'],
                             ['bottom', 'center'],
                             ['bottom', 'right'],
                             ['top', 'right']])

    self.add_face(['top', 'left'],
                  [['top', 'left'],
                   ['top', 'center'],
                   [['top'], ['bottom', 'center']],
                   [['top'], ['bottom', 'left']],
                   [['top', 'left'], ['bottom', 'center']],
                   [['left'], ['top', 'center']]], corner=True)

class HexTessagon(Tessagon):
  def init_tile_class(self):
    return HexTile
