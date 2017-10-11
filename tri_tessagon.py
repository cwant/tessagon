from importlib import reload

import tile, tessagon
reload(tile)
reload(tessagon)

from tile import Tile
from tessagon import Tessagon

class TriTile(Tile):
  def init_verts(self):
    return { 'lefttop': None,
             'righttop': None,
             'middle': None,
             'leftbottom': None,
             'rightbottom': None }

  def init_faces(self):
    return { 'lefttop': None,
             'righttop': None,
             'leftbottom': None,
             'rightbottom': None,
             'left': None,
             'right': None }

  def calculate_verts(self):
    #  ^  0.|.1   This is the topology of the tile.
    #  |  |\|/|   (Not a Dead Kennedy's logo ...).
    #  |  |.2.|   0 = lefttop
    #  |  |/|\|   1 = righttop
    #  V  3.|.4   2 = middle
    #             3 = leftbottom
    #  U ----->   4 = rightbottom
    #           
    #  0.|.1---0.|.1
    #  |\|/|   |\|/|
    #  |.2.|   |.2.|
    #  |/|\|   |/|\|
    #  3.|.4---3.|.4 That X thingy in the middle tells us that
    #  | | |\ /| | | vert zero is the same vert as a number of other verts
    #  | | | X | | | on neighboring tiles.
    #  | | |/ \| | |
    #  0.|.1---0.|.1
    #  |\|/|   |\|/|
    #  |.2.|   |.2.|
    #  |/|\|   |/|\|
    #  3.|.4---3.|.4

    self.lefttop_vert()
    self.righttop_vert()
    self.middle_vert()
    self.leftbottom_vert()
    self.rightbottom_vert()

  def lefttop_vert(self):
    vert = self.add_vert('lefttop', *self.blend(0, 1))
    self.set_equivalent_vert(['left'], 'righttop', vert)
    self.set_equivalent_vert(['top'], 'leftbottom', vert)
    self.set_equivalent_vert(['left', 'top'], 'rightbottom', vert)

  def righttop_vert(self):
    vert = self.add_vert('righttop', *self.blend(1, 1))
    self.set_equivalent_vert(['right'], 'lefttop', vert)
    self.set_equivalent_vert(['top'], 'rightbottom', vert)
    self.set_equivalent_vert(['right', 'top'], 'leftbottom', vert)

  def middle_vert(self):
    self.add_vert('middle', *self.blend(0.5, 0.5))

  def leftbottom_vert(self):
    vert = self.add_vert('leftbottom', *self.blend(0, 0))
    self.set_equivalent_vert(['left'], 'rightbottom', vert)
    self.set_equivalent_vert(['bottom'], 'lefttop', vert)
    self.set_equivalent_vert(['left', 'bottom'], 'righttop', vert)

  def rightbottom_vert(self):
    vert = self.add_vert('rightbottom', *self.blend(1, 0))
    self.set_equivalent_vert(['right'], 'leftbottom', vert)
    self.set_equivalent_vert(['bottom'], 'righttop', vert)
    self.set_equivalent_vert(['right', 'bottom'], 'lefttop', vert)

  def calculate_faces(self):
    #     lefttop   righttop
    #           0.|.1
    #           |\|/|
    #      left |.2.| right   
    #           |/|\|         
    #           3.|.4         
    #  leftbottom   rightbottom

    self.lefttop_face()
    self.righttop_face()
    self.left_face()
    self.right_face()
    self.leftbottom_face()
    self.rightbottom_face()

  def lefttop_face(self):
    face = self.add_face('lefttop',
                         [self.get_vert('lefttop'),
                          self.get_vert('middle'),
                          self.get_neighbor_vert(['top'], 'middle')])
    self.set_equivalent_face(['top'], 'leftbottom', face)

  def righttop_face(self):
    face = self.add_face('righttop',
                         [self.get_vert('middle'),
                          self.get_vert('righttop'),
                          self.get_neighbor_vert(['top'], 'middle')])
    self.set_equivalent_face(['top'], 'rightbottom', face)
 
  def left_face(self):
    self.add_face('left', [self.get_vert('lefttop'),
                           self.get_vert('leftbottom'),
                           self.get_vert('middle')])

  def right_face(self):
    self.add_face('right', [self.get_vert('middle'),
                            self.get_vert('rightbottom'),
                            self.get_vert('righttop')])

  def leftbottom_face(self):
    tile = self.get_neighbor_path(['bottom'])
    if not tile:
      return None
    tile.lefttop_face()

  def rightbottom_face(self):
    tile = self.get_neighbor_path(['bottom'])
    if not tile:
      return None
    tile.righttop_face()

class TriTessagon(Tessagon):
  def init_tile_class(self):
    return TriTile
