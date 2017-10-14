from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile

class SquareTile(Tile):
  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)
    self.u_symmetric = True
    self.v_symmetric = True

  def init_verts(self):
    return { 'top': { 'left': None, 'right': None },
             'bottom': { 'left': None, 'right': None } }

  def init_faces(self):
    return { 'middle': None }

  def calculate_verts(self):
    self.add_vert(['top', 'left'], 0, 1, corner=True)

  def init_faces(self):
    return { 'middle': None }

  def calculate_faces(self):
    self.add_face('middle', [['top', 'left'],
                             ['top', 'right'],
                             ['bottom', 'right'],
                             ['bottom', 'left']])

class SquareTessagon(Tessagon):
  def init_tile_class(self):
    return SquareTile
