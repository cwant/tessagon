from tessagon import Tessagon
from tile import Tile

class SquareTile(Tile):
  def init_verts(self):
    return { 'lefttop': None,
             'leftbottom': None,
             'rightbottom': None,
             'righttop': None
    }

  def calculate_verts(self):
    self.lefttop_vert()
    self.leftbottom_vert()
    self.rightbottom_vert()
    self.righttop_vert()

  def lefttop_vert(self):
    vert = self.add_vert('lefttop', *self.blend(0, 1))
    self.set_equivalent_vert(['left'], 'righttop', vert)
    self.set_equivalent_vert(['left', 'top'], 'rightbottom', vert)
    self.set_equivalent_vert(['top'], 'leftbottom', vert)

  def leftbottom_vert(self):
    vert = self.add_vert('leftbottom', *self.blend(0, 0))
    self.set_equivalent_vert(['left'], 'rightbottom', vert)
    self.set_equivalent_vert(['left', 'bottom'], 'righttop', vert)
    self.set_equivalent_vert(['bottom'], 'lefttop', vert)

  def rightbottom_vert(self):
    vert = self.add_vert('rightbottom', *self.blend(1, 0))
    self.set_equivalent_vert(['right'], 'leftbottom', vert)
    self.set_equivalent_vert(['right', 'bottom'], 'lefttop', vert)
    self.set_equivalent_vert(['bottom'], 'righttop', vert)

  def righttop_vert(self):
    vert = self.add_vert('righttop', *self.blend(1, 1))
    self.set_equivalent_vert(['right'], 'lefttop', vert)
    self.set_equivalent_vert(['right', 'top'], 'leftbottom', vert)
    self.set_equivalent_vert(['top'], 'rightbottom', vert)

  def init_faces(self):
    return { 'middle': None }

  def calculate_faces(self):
    self.add_face('middle', [self.get_vert('lefttop'),
                             self.get_vert('leftbottom'),
                             self.get_vert('rightbottom'),
                             self.get_vert('righttop')])

class SquareTessagon(Tessagon):
  def init_tile_class(self):
    return SquareTile
