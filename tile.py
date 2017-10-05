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

  def get_nested_list_value(self, nested_list, index_path):
    if not isinstance(index_path, list):
      return nested_list[index_path]
    value = nested_list
    for index in index_path:
      value = value[index]
    return value

  def set_nested_list_value(self, nested_list, index_path, value):
    if not isinstance(index_path, list):
      nested_list[index_path] = value
      return
    reference = nested_list
    for index in index_path[0:-1]:
      reference = reference[index]
    reference[index_path[-1]] = value

  def get_vert(self, index_path):
    return self.get_nested_list_value(self.verts, index_path)

  def set_vert(self, index_path, value):
    self.set_nested_list_value(self.verts, index_path, value)

  def get_face(self, index_path):
    return self.get_nested_list_value(self.faces, index_path)

  def set_face(self, index_path, value):
    self.set_nested_list_value(self.faces, index_path, value)

  def get_neighbor_path(self, neighbor_keys):
    tile = self
    for key in neighbor_keys:
      if not tile.neighbors[key]:
        return None
      tile = tile.neighbors[key]
    return tile

  def get_neighbor_vert(self, neighbor_keys, index_path):
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    return tile.get_vert(index_path)

  def add_vert(self, index_path, u, v):
    if self.get_vert(index_path):
      return None
    co = self.f(u,v)
    vert = self.bm.verts.new(co)
    self.set_vert(index_path, vert)
    return vert

  def set_equivalent_vert(self, neighbor_keys, index_path, vert):
    if not vert:
      return None
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    tile.set_vert(index_path, vert)

  def add_face(self, index_path, verts):
    if self.get_face(index_path):
      return None
    for vert in verts:
      if not vert:
        return None
    face = self.bm.faces.new(verts)
    self.set_face(index_path, face)
    return face

  def set_equivalent_face(self, neighbor_keys, index_path, face):
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    tile.set_face(index_path, face)
