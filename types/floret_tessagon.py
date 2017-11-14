from math import sqrt
from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile

class Floret:
  def __init__(self, tile, i, middle_point):
    self.tile = tile
    self.neighbors = [None]*6
    self.verts = [None]*19
    self.faces = [None]*6
    self.middle_point = middle_point

  def set_neighbor(self, index, floret):
    if self.neighbors[index]: return
    if not floret: return
    self.neighbors[index] = floret
    floret.neighbors[(index + 3) % 6] = self

  def offset_point(self, offset_u, offset_v):
    uv = [self.middle_point[0] + offset_u, self.middle_point[1] + offset_v] 
    return self.tile.f(*self.tile._blend(*uv))

  def offset_vert(self, offset_u, offset_v):
    point = self.offset_point(offset_u, offset_v)
    return self.tile.mesh_adaptor.create_vert(point)

  def add_offset_vert(self, i, offset_u, offset_v):
    if self.verts[i]: return
    vert = self.verts[i] = self.offset_vert(offset_u, offset_v)
    if vert:
      if i == 18:
        self.tile.tessagon.vert_types['center'].append(vert)
      elif i % 3 == 2:
        self.tile.tessagon.vert_types['other'].append(vert)
      else:
        self.tile.tessagon.vert_types['edge_to_center'].append(vert)

  def calculate_verts(self):
    self.add_offset_vert(18, 0, 0)

    unit_u = 2.0 / 42.0
    unit_v = 1.0 / 14.0
    h_u = unit_u * 0.5 * sqrt(3)
    h_v = unit_v * 0.5 * sqrt(3)

    d_u = 2.0 * unit_u
    d_v = 2.0 * unit_v
    self.add_offset_vert(0, d_u, 0)
    self.add_offset_vert(9, -d_u, 0)

    self.add_offset_vert(2, d_u, d_v)
    self.add_offset_vert(16, d_u, -d_v)
    self.add_offset_vert(7, -d_u, d_v)
    self.add_offset_vert(11, -d_u, -d_v)
    d_u = unit_u
    self.add_offset_vert(3, d_u, d_v)
    self.add_offset_vert(15, d_u, -d_v)
    self.add_offset_vert(6, -d_u, d_v)
    self.add_offset_vert(12, -d_u, -d_v)
    d_u = 0.5 * unit_u
    d_v = 3 * unit_v
    self.add_offset_vert(4, d_u, d_v)
    self.add_offset_vert(14, d_u, -d_v)
    self.add_offset_vert(5, -d_u, d_v)
    self.add_offset_vert(13, -d_u, -d_v)
    d_u = 2.5 * unit_u
    d_v = unit_v
    self.add_offset_vert(1, d_u, d_v)
    self.add_offset_vert(17, d_u, -d_v)
    self.add_offset_vert(8, -d_u, d_v)
    self.add_offset_vert(10, -d_u, -d_v)

    # Making things non-manifold using mathemagics
    for neighbor in range(6):
      other_floret = self.neighbors[neighbor]
      if not other_floret: continue
      for i in range(4):
        src = (3 * neighbor + i - 1) % 18
        dest = (3 * neighbor - i + 11) % 18
        if self.verts[src]:
          other_floret.verts[dest] = self.verts[src]

  def calculate_faces(self):
    for i in range(6):
      last = (3*i + 3) % 18
      verts = [self.verts[3*i], self.verts[3*i + 1],
               self.verts[3*i + 2], self.verts[last],
               self.verts[18]]
      self.faces[i] = self.tile.mesh_adaptor.create_face(verts)

class FloretTile(Tile):
  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)
    self.florets = [None] * 14

  def initialize_florets(self):
    for i in range(14):
      self.initialize_floret(i)

  def initialize_floret(self, i):
    if self.florets[i]: return

    if i in [0, 1, 2]:
      if not self.get_neighbor_tile(['bottom']): return
      if i == 0:
        if not self.get_neighbor_tile(['left']): return
        if not self.get_neighbor_tile(['bottom', 'left']): return

    if i == 5:
      if not self.get_neighbor_tile(['left']): return
    if i == 9:
      if not self.get_neighbor_tile(['right']): return

    if i in [12, 13]:
      if not self.get_neighbor_tile(['top']): return

    u = i * (3.0 / 14.0)
    v = u / 3.0
    while u > 1:
      u -= 1.0
    self.florets[i] = Floret(self, i, [u, v])

  def initialize_florets_neighbors(self):
    for i in range(14):
      self.initialize_floret_neighbors(i)

  def initialize_floret_neighbors(self, i):
    # All of this is to ensure the mesh is non-manifold
    if not self.florets[i]: return
    floret = self.florets[i]
    row = i // 5 # must be integer division
    column = i % 5

    # neighbor 0:
    if column < 4 and i < 13:
      floret.set_neighbor(0, self.florets[i + 1])
    elif i == 13:
      floret.set_neighbor(0, self.get_neighbor_floret(['right', 'top'], 0))
    else:
      floret.set_neighbor(0, self.get_neighbor_floret(['right'], i + 1))

    # neighbor 1:
    if row < 2 and i < 9:
      floret.set_neighbor(1, self.florets[i + 5])
    elif i == 9:
      floret.set_neighbor(1, self.get_neighbor_floret(['right', 'top'], 0))
    else:
      floret.set_neighbor(1, self.get_neighbor_floret(['top'], i - 9))

    # neighbor 2:
    if row < 2 and column > 0:
      floret.set_neighbor(2, self.florets[i + 4])
    elif column == 0 and i != 10:
      floret.set_neighbor(2, self.get_neighbor_floret(['left'], i + 4))
    else:
      floret.set_neighbor(2, self.get_neighbor_floret(['top'], i - 10))

    # neighbor 3:
    if column > 1:
      floret.set_neighbor(3, self.florets[i - 1])
    elif i == 0:
      floret.set_neighbor(3, self.get_neighbor_floret(['left', 'bottom'], 13))
    else:
      floret.set_neighbor(3, self.get_neighbor_floret(['left'], i - 1))

    # neighbor 4:
    if row > 0:
      floret.set_neighbor(4, self.florets[i - 5])
    elif i == 0:
      floret.set_neighbor(4, self.get_neighbor_floret(['left', 'bottom'], 9))
    else:
      floret.set_neighbor(4, self.get_neighbor_floret(['bottom'], i + 9))

    # neighbor 5:
    if row > 0 and column < 4:
      floret.set_neighbor(5, self.florets[i - 4])
    elif column == 4:
      floret.set_neighbor(5, self.get_neighbor_floret(['right'], i - 4))
    else:
      floret.set_neighbor(5, self.get_neighbor_floret(['bottom'], i + 10))

  def get_neighbor_floret(self, neighbor_keys, index):
    tile = self.get_neighbor_tile(neighbor_keys)
    if not tile: return None
    return tile.florets[index]

  def init_verts(self):
    # The florets handle the storage for the verts
    return None

  def calculate_verts(self):
    for floret in self.florets:
      if floret: floret.calculate_verts()

  def init_faces(self):
    # The florets handle the storage for the faces
    return None

  def calculate_faces(self):
    for floret in self.florets:
      if floret: floret.calculate_faces()

class FloretTessagon(Tessagon):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.florets = []
    self.vert_types = { 'center': [], 'edge_to_center': [], 'other': [] }

  def init_tile_class(self):
    return FloretTile

  def _initialize_tiles(self):
    super()._initialize_tiles()
    self._initialize_florets()
    self._initialize_floret_neighbors()

  def _initialize_florets(self):
    for tile in self.tiles:
      tile.initialize_florets()

  def _initialize_floret_neighbors(self):
    for tile in self.tiles:
      tile.initialize_florets_neighbors()
