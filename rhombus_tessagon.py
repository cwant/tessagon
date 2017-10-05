from equivalent_corners_tile import EquivalentCornersTile
from tessagon import Tessagon

class RhombusTile(EquivalentCornersTile):
  def init_verts(self):
    return { 'top': None,
             'lefttop': None,
             'righttop': None,
             'middletop': None,
             'leftmiddle': None,
             'rightmiddle': None,
             'middlebottom': None,
             'leftbottom': None,
             'rightbottom': None,
             'bottom': None
    }

  def calculate_verts(self):
    # ..0..  Topology:
    # ./|\.
    # 1.|.2   0 = top
    # |.3.|   1 = lefttop
    # |/.\|   2 = righttop
    # 4...5   3 = middletop
    # |\./|   4 = leftmiddle
    # |.6.|   5 = rightmiddle
    # 7.|.8   6 = middlebottom
    # .\|/.   7 = leftbottom
    # ..9..   8 = rightbottom
    #         9 = bottom
    self.top_vert()
    self.lefttop_vert()
    self.righttop_vert()
    self.middletop_vert()
    self.leftmiddle_vert()
    self.rightmiddle_vert()
    self.middlebottom_vert()
    self.leftbottom_vert()
    self.rightbottom_vert()
    self.bottom_vert()

  def top_vert(self):
    vert = self.add_vert('top', \
                         self.blend(self.u_range, 0.5),
                         self.v_range[0])
    self.set_equivalent_vert(['top'], 'bottom', vert)

  def lefttop_vert(self):
    vert = self.add_vert('lefttop', \
                         self.u_range[0],
                         self.blend(self.v_range, 1.0/6.0))
    self.set_equivalent_vert(['left'], 'righttop', vert)

  def righttop_vert(self):
    vert = self.add_vert('righttop',
                         self.u_range[1],
                         self.blend(self.v_range, 1.0/6.0))
    self.set_equivalent_vert(['right'], 'lefttop', vert)

  def middletop_vert(self):
    self.add_vert('middletop',
                  self.blend(self.u_range, 0.5),
                  self.blend(self.v_range, 1.0/3.0))

  def leftmiddle_vert(self):
    vert = self.add_vert('leftmiddle', \
                         self.u_range[0],
                         self.blend(self.v_range, 1.0/2.0))
    self.set_equivalent_vert(['left'], 'rightmiddle', vert)

  def rightmiddle_vert(self):
    vert = self.add_vert('rightmiddle', \
                         self.u_range[1],
                         self.blend(self.v_range, 1.0/2.0))
    self.set_equivalent_vert(['right'], 'leftmiddle', vert)

  def righttop_vert(self):
    vert = self.add_vert('righttop',
                         self.u_range[1],
                         self.blend(self.v_range, 1.0/6.0))
    self.set_equivalent_vert(['right'], 'lefttop', vert)

  def middlebottom_vert(self):
    self.add_vert('middlebottom',
                  self.blend(self.u_range, 0.5),
                  self.blend(self.v_range, 2.0/3.0))

  def leftbottom_vert(self):
    vert = self.add_vert('leftbottom', \
                         self.u_range[0],
                         self.blend(self.v_range, 5.0/6.0))
    self.set_equivalent_vert(['left'], 'rightbottom', vert)

  def rightbottom_vert(self):
    vert = self.add_vert('rightbottom',
                         self.u_range[1],
                         self.blend(self.v_range, 5.0/6.0))
    self.set_equivalent_vert(['right'], 'leftbottom', vert)

  def bottom_vert(self):
    vert = self.add_vert('bottom',
                         self.blend(self.u_range, 0.5),
                         self.v_range[1])

    self.set_equivalent_vert(['bottom'], 'top', vert)

  def init_faces(self):
    return { 'middle': None,
             'leftmiddletop': None,
             'leftmiddlebottom': None,
             'rightmiddlebottom': None,
             'rightmiddletop': None ,
             'lefttop': None,
             'leftbottom': None,
             'rightbottom': None,
             'righttop': None }


  def calculate_faces(self):
    self.middle_face()
    self.leftmiddletop_face()
    self.rightmiddlebottom_face()
    self.leftmiddlebottom_face()
    self.rightmiddletop_face()
    self.lefttop_face()
    self.leftbottom_face()
    self.rightbottom_face()
    self.righttop_face()

  def middle_face(self):
    self.add_face('middle', [self.get_vert('middletop'),
                             self.get_vert('leftmiddle'),
                             self.get_vert('middlebottom'),
                             self.get_vert('rightmiddle')])
        
  def leftmiddletop_face(self):
    self.add_face('leftmiddletop', [self.get_vert('top'),
                                    self.get_vert('lefttop'),
                                    self.get_vert('leftmiddle'),
                                    self.get_vert('middletop')])
  def rightmiddletop_face(self):
    self.add_face('rightmiddletop', [self.get_vert('top'),
                                     self.get_vert('righttop'),
                                     self.get_vert('rightmiddle'),
                                     self.get_vert('middletop')])

  def leftmiddlebottom_face(self):
    self.add_face('leftmiddlebottom', [self.get_vert('bottom'),
                                       self.get_vert('leftbottom'),
                                       self.get_vert('leftmiddle'),
                                       self.get_vert('middlebottom')])
  def rightmiddlebottom_face(self):
    self.add_face('rightmiddlebottom', [self.get_vert('bottom'),
                                        self.get_vert('rightbottom'),
                                        self.get_vert('rightmiddle'),
                                        self.get_vert('middlebottom')])

  def lefttop_face(self):
    face = self.add_face('lefttop', \
                         [self.get_vert('top'),
                          self.get_vert('lefttop'),
                          self.get_neighbor_vert(['left'], 'top'),
                          self.get_neighbor_vert(['top'], 'leftbottom')])

    self.set_equivalent_face(['top'], 'leftbottom', face)
    self.set_equivalent_face(['top', 'left'], 'rightbottom', face)
    self.set_equivalent_face(['left'], 'righttop', face)

class RhombusTessagon(Tessagon):
  def init_tile_class(self):
    return RhombusTile
