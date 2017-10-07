class Tile:
  def __init__(self, f, **kwargs):
    self.f = f
    # Corners is list of tuples [topleft, topright, bottomleft, bottomright]
    self.corners = None
    if 'corners' in kwargs:
      self.corners = kwargs['corners']
      if len(self.corners) != 4 or any (len(v) != 2 for v in self.corners):
        raise ValueError("corner should be a list of four tuples, "\
                         "set either option "\
                         "'corners' or options 'u_range' and 'v_range'")
    elif 'u_range' in kwargs and 'v_range' in kwargs:
      self.corners = [ [kwargs['u_range'][0], kwargs['v_range'][0]],
                       [kwargs['u_range'][1], kwargs['v_range'][0]],
                       [kwargs['u_range'][0], kwargs['v_range'][1]],
                       [kwargs['u_range'][1], kwargs['v_range'][1]] ]
    else:
      raise ValueError("Must set either option "\
                       "'corners' or options 'u_range' and 'v_range'")
    if 'bm' in kwargs:
      self.bm = kwargs['bm']
    if not self.bm:
      raise ValueError("Make sure bm is set (output BMesh)")
    if 'tessagon' in kwargs:
      self.tessagon = kwargs['tessagon']
    if not self.tessagon:
      raise ValueError("Make sure tessagon is set")


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

  def blend_verts(self, vert1, vert2, ratio):
    out = [None, None]
    for i in range(2):
      out[i] = (1 - ratio) * vert1[i] + ratio * vert2[i]
    return out

  def blend(self, ratio_u, ratio_v):
    uv0 = self.blend_verts(self.corners[0],
                           self.corners[1],
                           ratio_u)
    uv1 = self.blend_verts(self.corners[2],
                           self.corners[3],
                           ratio_u)
    return self.blend_verts(uv0, uv1, ratio_v)

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

  def add_vert(self, index_path, u, v, **kwargs):
    if self.get_vert(index_path):
      return None
    co = self.f(u,v)
    vert = self.bm.verts.new(co)
    self.set_vert(index_path, vert)
    if 'vert_type' in kwargs:
      if not kwargs['vert_type'] in self.tessagon.vert_types:
        self.tessagon.face_types[kwargs['vert_type']] = []
      self.tessagon.vert_types[kwargs['vert_type']].append(face)

    return vert

  def set_equivalent_vert(self, neighbor_keys, index_path, vert):
    if not vert:
      return None
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    tile.set_vert(index_path, vert)

  def add_face(self, index_path, verts, **kwargs):
    if self.get_face(index_path):
      return None
    for vert in verts:
      if not vert:
        return None
    face = self.bm.faces.new(verts)
    self.set_face(index_path, face)
    if 'face_type' in kwargs:
      if not kwargs['face_type'] in self.tessagon.face_types:
        self.tessagon.face_types[kwargs['face_type']] = []
      self.tessagon.face_types[kwargs['face_type']].append(face)

    return face

  def set_equivalent_face(self, neighbor_keys, index_path, face):
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    tile.set_face(index_path, face)
