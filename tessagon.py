import bpy, bmesh
from math import sqrt, sin, cos, atan2, pi
from mathutils import Matrix, Vector

class Tile:
  def __init__(self, f, **kwargs):
    self.f = f
    self.u_range = self.v_range = None
    if 'u_range' in kwargs:
      self.u_range = kwargs['u_range']
    if 'v_range' in kwargs:
      self.v_range = kwargs['v_range']
    if not self.u_range or not self.v_range:
      raise ValueError("Make sure u_range and v_range intervals are set")
    if 'bm' in kwargs:
      self.bm = kwargs['bm']
    if not self.bm:
      raise ValueError("Make sure bm is set (output BMesh)")

    self.neighbors = { 'top': None,
                       'bottom': None,
                       'left': None,
                       'right': None }

    self.verts = self.init_verts()
    self.faces = self.init_faces()

  def set_neighbors(self, **kwargs):
    if 'top' in kwargs:
      self.neighbors['top'] = kwargs['top']
    if 'bottom' in kwargs:
      self.neighbors['bottom'] = kwargs['bottom']
    if 'left' in kwargs:
      self.neighbors['left'] = kwargs['left']
    if 'right' in kwargs:
      self.neighbors['right'] = kwargs['right']

  def blend(self, interval, ratio):
    return (1 - ratio) * interval[0] + ratio * interval[1]

  def get_vert(self, vert_index):
    return self.verts[vert_index]

  def set_vert(self, vert_index, value):
    self.verts[vert_index] = value

  def get_face(self, face_index):
    return self.faces[face_index]

  def set_face(self, face_index, value):
    self.faces[face_index] = value

  def get_neighbor_path(self, neighbor_keys):
    tile = self
    for key in neighbor_keys:
      if not tile.neighbors[key]:
        return None
      tile = tile.neighbors[key]
    return tile

  def get_neighbor_vert(self, neighbor_keys, neighbor_vert_index):
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    return tile.get_vert(neighbor_vert_index)

  def add_vert(self, index, u, v):
    if self.get_vert(index):
      return None
    co = self.f(u,v)
    vert = self.bm.verts.new(co)
    self.set_vert(index, vert)
    return vert

  def set_equivalent_vert(self, neighbor_keys, neighbor_vert_index, vert):
    if not vert:
      return None
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    tile.set_vert(neighbor_vert_index, vert)

  def add_face(self, index, verts):
    if self.get_face(index):
      return None
    for vert in verts:
      if not vert:
        return None
    face = self.bm.faces.new(verts)
    self.set_face(index, face)
    return face

  def set_equivalent_face(self, neighbor_keys, neighbor_face_index, face):
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    tile.set_face(neighbor_face_index, face)

class EquivalentCornersTile(Tile):
  def init_faces(self):
    return { 'middle': None,
             'lefttop': None,
             'leftbottom': None,
             'rightbottom': None,
             'righttop': None }

  def calculate_faces(self):
    self.middle_face()
    self.lefttop_face()
    self.leftbottom_face()
    self.rightbottom_face()
    self.righttop_face()

  def leftbottom_face(self):
    tile = self.get_neighbor_path(['bottom'])
    if not tile:
      return None
    tile.lefttop_face()

  def rightbottom_face(self):
    tile = self.get_neighbor_path(['bottom', 'right'])
    if not tile:
      return None
    tile.lefttop_face()

  def righttop_face(self):
    tile =  self.neighbors['right']
    if not tile:
      return None
    tile.lefttop_face()

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
    self.add_vert('top', \
                  self.blend(self.u_range, 0.5),
                  self.blend(self.v_range, 1.0/6.0))

  def lefttop_vert(self):
    vert = self.add_vert('lefttop', \
                         self.u_range[0],
                         self.blend(self.v_range, 1.0/3.0))
    self.set_equivalent_vert(['left'], 'righttop', vert)

  def leftbottom_vert(self):
    vert = self.add_vert('leftbottom', \
                         self.u_range[0],
                         self.blend(self.v_range, 2.0/3.0))
    self.set_equivalent_vert(['left'], 'rightbottom', vert)

  def bottom_vert(self):
    self.add_vert('bottom',
                  self.blend(self.u_range, 0.5),
                  self.blend(self.v_range, 5.0/6.0))

  def rightbottom_vert(self):
    vert = self.add_vert('rightbottom',
                         self.u_range[1],
                         self.blend(self.v_range, 2.0/3.0))
    self.set_equivalent_vert(['right'], 'leftbottom', vert)

  def righttop_vert(self):
    vert = self.add_vert('righttop',
                         self.u_range[1],
                         self.blend(self.v_range, 1.0/3.0))
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
    #  0.|.1   This is the topology of the tile.
    #  |\|/|   (Not a Dead Kennedy's logo ...).
    #  |.2.|   0 = lefttop
    #  |/|\|   1 = righttop
    #  3.|.4   2 = middle
    #          3 = leftbottom
    #          4 = rightbottom
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
    vert = self.add_vert('lefttop',
                         self.u_range[0],
                         self.v_range[0])
    self.set_equivalent_vert(['left'], 'righttop', vert)
    self.set_equivalent_vert(['top'], 'leftbottom', vert)
    self.set_equivalent_vert(['left', 'top'], 'rightbottom', vert)

  def righttop_vert(self):
    vert = self.add_vert('righttop',
                         self.u_range[1],
                         self.v_range[0])
    self.set_equivalent_vert(['right'], 'lefttop', vert)
    self.set_equivalent_vert(['top'], 'rightbottom', vert)
    self.set_equivalent_vert(['right', 'top'], 'leftbottom', vert)

  def middle_vert(self):
    self.add_vert('middle',
                  self.blend(self.u_range, 0.5),
                  self.blend(self.v_range, 0.5))

  def leftbottom_vert(self):
    vert = self.add_vert('leftbottom',
                         self.u_range[0],
                         self.v_range[1])
    self.set_equivalent_vert(['left'], 'rightbottom', vert)
    self.set_equivalent_vert(['bottom'], 'lefttop', vert)
    self.set_equivalent_vert(['left', 'bottom'], 'righttop', vert)

  def rightbottom_vert(self):
    vert = self.add_vert('rightbottom',
                         self.u_range[1],
                         self.v_range[1])
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

class Tessagon:
  def __init__(self, f, **kwargs):
    self.f = f
    self.tile_class = self.init_tile_class()
    self.u_range = self.v_range = None
    self.u_num = self.v_num = None
    self.bm = None
    self.u_cyclic = True
    self.v_cyclic = True
    self.u_twist = False
    self.v_twist = False
    if 'u_range' in kwargs:
      self.u_range = kwargs['u_range']
    if 'v_range' in kwargs:
      self.v_range = kwargs['v_range']
    if not self.u_range or not self.v_range:
      raise ValueError("Make sure u_range and v_range intervals are set")
    if 'u_num' in kwargs:
      self.u_num = kwargs['u_num']
    if 'v_num' in kwargs:
      self.v_num = kwargs['v_num']
    if not self.u_num or not self.v_num:
      raise ValueError("Make sure u_num and v_num intervals are set")
    if 'u_cyclic' in kwargs:
      self.u_cyclic = kwargs['u_cyclic']
    if 'v_cyclic' in kwargs:
      self.v_cyclic = kwargs['v_cyclic']
    if 'u_twist' in kwargs:
      self.u_twist = kwargs['u_twist']
    if 'v_twist' in kwargs:
      self.v_twist = kwargs['v_twist']

    self.tiles = [[None for i in range(self.v_num)] for j in range(self.u_num)]
    self.bm = bmesh.new()

  def create_bmesh(self):
    self.initialize_tiles()
    self.initialize_neighbors()
    self.calculate_verts()
    self.calculate_faces()
    return self.bm

  def initialize_tiles(self):
    for u in range(self.u_num):
      u_ratio0 = float(u) / self.u_num
      u_ratio1 = float(u + 1) / self.u_num
      u0 = self.u_range[0] * (1.0 - u_ratio0) + self.u_range[1] * u_ratio0
      u1 = self.u_range[0] * (1.0 - u_ratio1) + self.u_range[1] * u_ratio1
      for v in range(self.v_num):
        v_ratio0 = float(v) / self.v_num
        v_ratio1 = float(v + 1) / self.v_num
        v0 = self.v_range[0] * (1.0 - v_ratio0) + self.v_range[1] * v_ratio0
        v1 = self.v_range[0] * (1.0 - v_ratio1) + self.v_range[1] * v_ratio1
        self.tiles[u][v] = self.tile_class(self.f, u_range=[u0, u1], v_range=[v0, v1],
                                           bm=self.bm)

  def initialize_neighbors(self):
    for u in range(self.u_num):
      u_prev = (u - 1) % self.u_num
      u_next = (u + 1) % self.u_num
      for v in range(self.v_num):
        v_prev = (v - 1) % self.v_num
        v_next = (v + 1) % self.v_num
        tile = self.tiles[u][v]
        if not self.u_cyclic and u == 0:
          left = None
        else:
          left = self.tiles[u_prev][v]
        if not self.v_cyclic and v == 0:
          top = None
        else:
          top = self.tiles[u][v_prev]
        if not self.u_cyclic and u == self.u_num - 1:
          right = None
        else:
          if self.u_twist and u == self.u_num - 1:
            right = self.tiles[u_next][0]
          else:
            right = self.tiles[u_next][v]
        if not self.v_cyclic and v == self.v_num - 1:
          bottom = None
        else:
          if self.v_twist and v == self.v_num - 1:
            bottom = self.tiles[self.u_num - u - 1][v_next]
          else:
            bottom = self.tiles[u][v_next]
        tile.set_neighbors(left=left, right=right, top=top, bottom=bottom)
        
  def calculate_verts(self):
    for u in range(self.u_num):
      for v in range(self.v_num):
        self.tiles[u][v].calculate_verts()

  def calculate_faces(self):
    for u in range(self.u_num):
      for v in range(self.v_num):
        self.tiles[u][v].calculate_faces()
    bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)

class HexTessagon(Tessagon):
  def init_tile_class(self):
    return HexTile

class OctoTessagon(Tessagon):
  def init_tile_class(self):
    return OctoTile

class TriTessagon(Tessagon):
  def init_tile_class(self):
    return TriTile
