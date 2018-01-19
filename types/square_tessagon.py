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

  def calculate_colors(self):
    if self.color_pattern == 1:
      self.color_pattern1()
    elif self.color_pattern == 2:
      self.color_pattern2()
    elif self.color_pattern == 3:
      self.color_pattern3()
    elif self.color_pattern == 4:
      self.color_pattern4()
    elif self.color_pattern == 5:
      self.color_pattern5()
    elif self.color_pattern == 6:
      self.color_pattern6()
    elif self.color_pattern == 7:
      self.color_pattern7()
    elif self.color_pattern == 8:
      self.color_pattern8()

  def color_pattern1(self):
    if (self.fingerprint[0] + self.fingerprint[1]) % 2 == 0:
      self.color_face(['middle'], 0)
    else:
      self.color_face(['middle'], 1)

  def color_pattern2(self):
    if (self.fingerprint[0] + self.fingerprint[1]) % 2 == 0:
      self.color_face(['middle'], 0)
    elif self.fingerprint[0] % 2 == 0:
      self.color_face(['middle'], 1)
    else:
      self.color_face(['middle'], 2)

  def color_pattern3(self):
    if (self.fingerprint[0] * self.fingerprint[1]) % 2 == 0:
      self.color_face(['middle'], 0)
    else:
      self.color_face(['middle'], 1)

  def color_pattern4(self):
    if self.fingerprint[1] % 2 == 0:
      self.color_face(['middle'], 0)
    else:
      if ((self.fingerprint[1] // 2) + self.fingerprint[0]) % 2 == 0:
        self.color_face(['middle'], 0)
      else:
        self.color_face(['middle'], 1)

  def color_pattern5(self):
    if self.fingerprint[1] % 2 == 0:
      self.color_face(['middle'], 0)
    else:
      self.color_face(['middle'], 1)

  def color_pattern6(self):
    if self.fingerprint[1] % 2 == 0:
      self.color_face(['middle'], 0)
    else:
      if self.fingerprint[0] % 2 == 0:
        self.color_face(['middle'], 1)
      else:
        self.color_face(['middle'], 2)

  def color_pattern7(self):
    if self.fingerprint[1] % 2 == 0:
      self.color_face(['middle'], 0)
    else:
      if ((self.fingerprint[1] // 2) + self.fingerprint[0]) % 2 == 0:
        self.color_face(['middle'], 1)
      else:
        self.color_face(['middle'], 2)

  def color_pattern8(self):
    if self.fingerprint[1] % 2 == 0:
      if self.fingerprint[0] % 2 == 0:
        self.color_face(['middle'], 0)
      else:
        self.color_face(['middle'], 1)
    else:
      if self.fingerprint[0] % 2 == 0:
        self.color_face(['middle'], 2)
      else:
        self.color_face(['middle'], 3)

class SquareTessagon(Tessagon):
  def init_tile_class(self):
    return SquareTile
