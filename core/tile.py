from tessagon.core.abstract_tile import AbstractTile

class Tile(AbstractTile):
  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)

    self.mesh_adaptor = tessagon.mesh_adaptor

    self.verts = self.init_verts()
    self.faces = self.init_faces()

  def get_vert(self, index_path):
    return self.get_nested_list_value(self.verts, index_path)

  def set_vert(self, index_path, value):
    self.set_nested_list_value(self.verts, index_path, value)

  def get_face(self, index_path):
    return self.get_nested_list_value(self.faces, index_path)

  def set_face(self, index_path, value):
    self.set_nested_list_value(self.faces, index_path, value)

  def get_neighbor_vert(self, neighbor_keys, index_path):
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    return tile.get_vert(index_path)

  def add_vert(self, index_path, u, v, **kwargs):
    if self.get_vert(index_path):
      return None
    coords = self.f(u,v)

    vert = self.mesh_adaptor.create_vert(coords)

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

    face = self.mesh_adaptor.create_face(verts)

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
