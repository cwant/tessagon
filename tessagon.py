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
    self.verts = [None]*8
    self.faces = { 'top': None,
                   'bottom': None,
                   'left': None,
                   'right': None }

  def set_neighbors(self, **kwargs):
    if 'top' in kwargs:
      self.neighbors['top'] = kwargs['top']
    if 'bottom' in kwargs:
      self.neighbors['bottom'] = kwargs['bottom']
    if 'left' in kwargs:
      self.neighbors['left'] = kwargs['left']
    if 'right' in kwargs:
      self.neighbors['right'] = kwargs['right']

  def calculate_verts(self):
    #  0...1
    #  |...|   This is the topology of the tile.
    #  2...3   The numbers are the verts we want to make,
    #  .\./.   and the lines are the edges between faces.
    #  ..4..   We order our verts going in typical reading order
    #  ..|..   (each line from top to bottom going left to right).
    #  ..5..   Verts are only created if a neighboring tile can
    #  ./.\.   have a face, check out this expanded ASCII art to get
    #  6...7   a sense of how the hexagons fit with adjacent tiles ...

    # 0...1---0...1
    # |...|   |...|
    # 2...3---2...3
    # .\./.   .\./.
    # ..4..   ..4..
    # ..|..   ..|..
    # ..5..   ..5..
    # ./.\.   ./.\.
    # 6...7---6...7  This illustates which vertices are
    # |   |\ /|   |  equivalent to vertices on neighboring
    # |   | X |   |  faces. As such, this reduces which verts we
    # |   |/ \|   |  have to calculate.
    # 0...1---0...1
    # |...|   |...|
    # 2...3---2...3
    # .\./.   .\./.
    # ..4..   ..4..
    # ..|..   ..|..
    # ..5..   ..5..
    # ./.\.   ./.\.
    # 6...7---6...7
    self.vert_0()
    self.vert_2()
    self.vert_4()
    self.vert_5()

  def vert_0(self):
    # Vert 0 gets created if a top or left neighbor.
    # It is top left corner.
    # If left neighbor, it gets added there as Vert 1
    # If top neighbor, it gets added there as Vert 6
    # If top-left neighbor, it gets added there as Vert 7
    if not self.verts[0]:
      if self.neighbors['left'] or self.neighbors['top']:
        u = self.u_range[0]
        v = self.v_range[0]
        co = self.f(u,v)
        bvert = self.bm.verts.new(co)
        self.verts[0] = bvert
        self.set_neighbor_vert(['left'], 1, bvert)
        self.set_neighbor_vert(['top'], 6, bvert)
        self.set_neighbor_vert(['left', 'top'], 7, bvert)

  def vert_2(self):
    # Vert 2 gets created if a top or left neighbor.
    # It is 0.25 down left edge
    # If left neighbor, it gets added there too as Vert 3
    if not self.verts[2]:
      if self.neighbors['left'] or self.neighbors['top']:
        u = self.u_range[0]
        v = self.blend(self.v_range, 0.25)
        co = self.f(u,v)
        bvert = self.bm.verts.new(co)
        self.verts[2] = bvert
        self.set_neighbor_vert(['left'], 3, bvert)

  def vert_4(self):
    # Verts 4 gets created if there is a left, right, or top neighbor.
    # Vert 4 is 0.5 in the u interval.
    # Vert 4 is 0.5 in the v interval
    if self.neighbors['left'] or self.neighbors['right'] or \
       self.neighbors['top']:
      u = self.blend(self.u_range, 0.5)
      v = self.blend(self.v_range, 0.5)
      co = self.f(u,v)
      bvert = self.bm.verts.new(co)
      self.verts[4] = bvert

  def vert_5(self):
    # Verts 4 and 5 get created if there is a left, right, or bottom neighbor.
    # Vert 5 is 0.5 in the u interval.
    # Vert 5 is 0.75 in the v intervalx
    if self.neighbors['left'] or self.neighbors['right'] or \
       self.neighbors['bottom']:
      u = self.blend(self.u_range, 0.5)
      v = self.blend(self.v_range, 0.75)
      co = self.f(u,v)
      bvert = self.bm.verts.new(co)
      self.verts[5] = bvert

  def blend(self, interval, ratio):
    return (1 - ratio) * interval[0] + ratio * interval[1]

  def set_neighbor_vert(self, neighbor_keys, index, value):
    tile = self
    for key in neighbor_keys:
      if not tile.neighbors[key]:
        return None
      tile = tile.neighbors[key]
    tile.verts[index] = value

  def calculate_faces(self):
    #        top
    #
    #       0...1
    #       |...|
    #       2...3
    #       .\./.
    # left  ..4.. right
    #       ..|..
    #       ..5..
    #       ./.\.
    #       6...7
    #
    #      bottom
    #
    self.top_face()
    self.left_face()
    self.right_face()
    self.bottom_face()

  def top_face(self):
    if self.neighbors['top']:
      if self.faces['top']:
        return
      self.faces['top'] = self.neighbors['top'].faces['bottom'] = [None]
      self.faces['top'][0] = self.bm.faces.new([self.verts[0],
                                                self.verts[2],
                                                self.verts[4],
                                                self.verts[3],
                                                self.verts[1],
                                                self.neighbors['top'].verts[5]])

  def left_face(self):
    if self.neighbors['left']:
      if self.faces['left']:
        return
      self.faces['left'] = self.neighbors['left'].faces['right'] = [None]
      self.faces['left'][0] = self.bm.faces.new([self.verts[2],
                                                 self.verts[4],
                                                 self.verts[5],
                                                 self.verts[6],
                                                 self.neighbors['left'].verts[5],
                                                 self.neighbors['left'].verts[4]])

  def right_face(self):
    if self.neighbors['right']:
      if self.faces['right']:
        return
      self.faces['right'] = self.neighbors['right'].faces['left'] = [None]
      self.faces['right'][0] = self.bm.faces.new([self.verts[7],
                                                  self.verts[5],
                                                  self.verts[4],
                                                  self.verts[3],
                                                  self.neighbors['right'].verts[4],
                                                  self.neighbors['right'].verts[5]])

  def bottom_face(self):
    if self.neighbors['bottom']:
      if self.faces['bottom']:
        return
      self.faces['bottom'] = self.neighbors['bottom'].faces['top'] = [None]
      self.faces['bottom'][0] = self.bm.faces.new([self.verts[6],
                                                   self.verts[5],
                                                   self.verts[7],
                                                   self.neighbors['bottom'].verts[3],
                                                   self.neighbors['bottom'].verts[4],
                                                   self.neighbors['bottom'].verts[2]])

class Tessagon:
  def __init__(self, f, **kwargs):
    self.f = f
    self.u_range = self.v_range = None
    self.u_num = self.v_num = None
    self.bm = None
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
        self.tiles[u][v] = Tile(self.f, u_range=[u0, u1], v_range=[v0, v1],
                                bm=self.bm)

  def initialize_neighbors(self):
    for u in range(self.u_num):
      u_prev = (u - 1) % self.u_num
      u_next = (u + 1) % self.u_num
      for v in range(self.v_num):
        v_prev = (v - 1) % self.v_num
        v_next = (v + 1) % self.v_num
        tile = self.tiles[u][v]
        tile.set_neighbors(left=self.tiles[u_prev][v],
                           right=self.tiles[u_next][v],
                           top=self.tiles[u][v_prev],
                           bottom=self.tiles[u][v_next])
        
  def calculate_verts(self):
    for u in range(self.u_num):
      for v in range(self.v_num):
        self.tiles[u][v].calculate_verts()

  def calculate_faces(self):
    for u in range(self.u_num):
      for v in range(self.v_num):
        self.tiles[u][v].calculate_faces()
    bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
