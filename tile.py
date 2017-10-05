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
