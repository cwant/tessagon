from math import sqrt

from importlib import reload
import equivalent_corners_tile, tessagon
reload(equivalent_corners_tile)
reload(tessagon)

from equivalent_corners_tile import EquivalentCornersTile
from tessagon import Tessagon

class OctoTile(EquivalentCornersTile):
  CORNER_TO_VERT_RATIO = 1.0 / (2.0 + sqrt(2))

  def init_verts(self):
    return { 'topleft': None,
             'lefttop': None,
             'leftbottom': None,
             'bottomleft': None,
             'bottomright': None,
             'rightbottom': None,
             'righttop': None,
             'topright': None
    }

  def calculate_verts(self):
    #            Topology:
    #  ..0-1..      0 = topleft
    #  ./...\.      1 = topright
    #  2.....3      2 = lefttop
    #  |.....|      3 = righttop
    #  4.....5      4 = leftbottom
    #  .\.../.      5 = rightbottom
    #  ..6-7..      6 = bottomleft
    #               7 = leftbottom

    # ..0-1....0-1.. This illustates which vertices are
    # ./...\../...\. equivalent to vertices on neighboring
    # 2.....32.....3 faces. As such, this reduces which verts we
    # |.....||.....| have to calculate.
    # 4.....54.....5
    # .\.../..\.../.
    # ..6-7....6-7..
    # ..0-1....0-1..
    # ./...\../...\.
    # 2.....32.....3
    # |.....||.....|
    # 4.....54.....5
    # .\.../..\.../.
    # ..6-7....6-7..
    self.topleft_vert()
    self.topright_vert()
    self.lefttop_vert()
    self.leftbottom_vert()
    self.bottomleft_vert()
    self.bottomright_vert()
    self.rightbottom_vert()
    self.righttop_vert()

  def topleft_vert(self):
    vert = self.add_vert('topleft', \
                         self.blend(self.u_range, self.CORNER_TO_VERT_RATIO),
                         self.v_range[0])
    self.set_equivalent_vert(['top'], 'bottomleft', vert)

  def topright_vert(self):
    vert = self.add_vert('topright', \
                         self.blend(self.u_range,
                                    1.0 - self.CORNER_TO_VERT_RATIO),
                         self.v_range[0])
    self.set_equivalent_vert(['top'], 'bottomright', vert)

  def lefttop_vert(self):
    vert = self.add_vert('lefttop', \
                         self.u_range[0],
                         self.blend(self.v_range, self.CORNER_TO_VERT_RATIO))
    self.set_equivalent_vert(['left'], 'righttop', vert)

  def righttop_vert(self):
    vert = self.add_vert('righttop', \
                         self.u_range[1],
                         self.blend(self.v_range, self.CORNER_TO_VERT_RATIO))
    self.set_equivalent_vert(['right'], 'lefttop', vert)

  def leftbottom_vert(self):
    vert = self.add_vert('leftbottom', \
                         self.u_range[0],
                         self.blend(self.v_range,
                                    1.0 - self.CORNER_TO_VERT_RATIO))
    self.set_equivalent_vert(['left'], 'rightbottom', vert)

  def rightbottom_vert(self):
    vert = self.add_vert('rightbottom',
                         self.u_range[1],
                         self.blend(self.v_range,
                                    1.0 - self.CORNER_TO_VERT_RATIO))
    self.set_equivalent_vert(['right'], 'leftbottom', vert)

  def bottomleft_vert(self):
    vert = self.add_vert('bottomleft',
                  self.blend(self.u_range, self.CORNER_TO_VERT_RATIO),
                  self.v_range[1])
    self.set_equivalent_vert(['bottom'], 'topleft', vert)

  def bottomright_vert(self):
    vert = self.add_vert('bottomright',
                         self.blend(self.u_range,
                                    1.0 - self.CORNER_TO_VERT_RATIO),
                         self.v_range[1])
    self.set_equivalent_vert(['bottom'], 'topright', vert)

  #
  #   LEFTTOP..o---o...RIGHTTOP
  #         ../.....\..
  #         ./.......\.
  #         o.........o
  #         |.MIDDLE..|
  #         o.........o    
  #         .\..... ./.
  #         ..\...../..
  # LEFTBOTTOM.o---o.RIGHTBOTTOM
  #

  def middle_face(self):
    self.add_face('middle', [self.get_vert('topleft'),
                             self.get_vert('lefttop'),
                             self.get_vert('leftbottom'),
                             self.get_vert('bottomleft'),
                             self.get_vert('bottomright'),
                             self.get_vert('rightbottom'), 
                             self.get_vert('righttop'),
                             self.get_vert('topright')])
       
  def lefttop_face(self):
    face = self.add_face('lefttop', \
                         [self.get_vert('lefttop'),
                          self.get_vert('topleft'),
                          self.get_neighbor_vert(['top'], 'leftbottom'),
                          self.get_neighbor_vert(['left'], 'topright')])

    self.set_equivalent_face(['top'], 'leftbottom', face)
    self.set_equivalent_face(['top', 'left'], 'rightbottom', face)
    self.set_equivalent_face(['left'], 'righttop', face)

class OctoTessagon(Tessagon):
  def init_tile_class(self):
    return OctoTile
