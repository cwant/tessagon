from importlib import reload
import equivalent_corners_tile
import tessagon

from tessagon import Tessagon
from equivalent_corners_tile import EquivalentCornersTile

class HexTile(EquivalentCornersTile):
  def init_verts(self):
    return { 'top': None,
             'lefttop': None,
             'leftbottom': None,
             'bottom': None,
             'rightbottom': None,
             'righttop': None
    }

  def calculate_verts(self):
    #  ..|..   Topology:
    #  ..0..
    #  ./.\.   0 = top
    #  1...2   1 = lefttop
    #  |...|   2 = righttop
    #  3...4   3 = leftbottom
    #  .\./.   4 = rightbottom
    #  ..5..   6 = bottom 
    #  ..|.. 

    # ..|..   ..|..
    # ..0..   ..0..
    # ./.\.   ./.\.
    # 1...2 = 1...2
    # |...|   |...|
    # 3...4 = 3...4
    # .\./.   .\./.
    # ..5..   ..5..
    # ..|..   ..|.. This illustates which vertices are
    #   |   F   |     equivalent to vertices on neighboring
    #   |   A   |     faces. As such, this reduces which verts we
    #   |   C   |     have to calculate.
    # ..|.. E ..|..
    # ..0..   ..0..
    # ./.\.   ./.\.
    # 1...2 = 1...2
    # |...|   |...|
    # 3...4 = 3...4
    # .\./.   .\./.
    # ..5..   ..5..
    # ..|..   ..|..
    self.top_vert()
    self.lefttop_vert()
    self.leftbottom_vert()
    self.bottom_vert()
    self.rightbottom_vert()
    self.righttop_vert()

  def top_vert(self):
    self.add_vert('top', *self.blend(0.5, 1.0/6.0))

  def lefttop_vert(self):
    vert = self.add_vert('lefttop', *self.blend(0, 1.0/3.0))
    self.set_equivalent_vert(['left'], 'righttop', vert)

  def leftbottom_vert(self):
    vert = self.add_vert('leftbottom', *self.blend(0, 2.0/3.0))
    self.set_equivalent_vert(['left'], 'rightbottom', vert)

  def bottom_vert(self):
    self.add_vert('bottom', *self.blend(0.5, 5.0/6.0))

  def rightbottom_vert(self):
    vert = self.add_vert('rightbottom', *self.blend(1, 2.0/3.0))
    self.set_equivalent_vert(['right'], 'leftbottom', vert)

  def righttop_vert(self):
    vert = self.add_vert('righttop', *self.blend(1, 1.0/3.0))
    self.set_equivalent_vert(['right'], 'lefttop', vert)

  #
  #         .....o...
  #         ..../.\....
  #   LEFTTOP../...\.RIGHTTOP
  #         ../.....\..
  #         ./.......\.
  #         o.........o
  #         |.MIDDLE..|
  #         o.........o    
  #         .\..... ./.
  #         ..\...../..
  # LEFTBOTTOM.\.../.RIGHTBOTTOM
  #         ....\./....
  #         .....o.....
  #

  def middle_face(self):
    self.add_face('middle', [self.get_vert('top'),
                             self.get_vert('lefttop'),
                             self.get_vert('leftbottom'),
                             self.get_vert('bottom'),
                             self.get_vert('rightbottom'),
                             self.get_vert('righttop')])
        
  def lefttop_face(self):
    face = self.add_face('lefttop', \
                         [self.get_vert('lefttop'),
                          self.get_vert('top'),
                          self.get_neighbor_vert(['top'], 'bottom'),
                          self.get_neighbor_vert(['top'], 'leftbottom'),
                          self.get_neighbor_vert(['top', 'left'], 'bottom'),
                          self.get_neighbor_vert(['left'], 'top')])

    self.set_equivalent_face(['top'], 'leftbottom', face)
    self.set_equivalent_face(['top', 'left'], 'rightbottom', face)
    self.set_equivalent_face(['left'], 'righttop', face)

class HexTessagon(Tessagon):
  def init_tile_class(self):
    return HexTile
