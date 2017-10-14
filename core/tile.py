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

  def add_vert(self, index_path, ratio_u, ratio_v, **kwargs):
    vert = self.get_vert(index_path)
    if not vert:
      coords = self.f(*self.blend(ratio_u, ratio_v))
      vert = self.mesh_adaptor.create_vert(coords)

      self.set_vert(index_path, vert)
      if 'vert_type' in kwargs:
        if not kwargs['vert_type'] in self.tessagon.vert_types:
          self.tessagon.vert_types[kwargs['vert_type']] = []
          self.tessagon.vert_types[kwargs['vert_type']].append(face)

    if not 'symmetry' in kwargs:
      extra_args = { 'symmetry': True}
      if self.u_symmetric:
        # Add reflection about u
        u_flip_path = self.u_flip(index_path)
        self.add_vert(u_flip_path, 1.0 - ratio_u, ratio_v,
                      **{**kwargs, **extra_args})
        if self.v_symmetric:
          # Add diagonally across
          uv_flip_path = self.v_flip(u_flip_path)
          self.add_vert(uv_flip_path, 1.0 - ratio_u, 1.0 - ratio_v,
                        **{**kwargs, **extra_args})
      if self.v_symmetric:
        # Add reflection about v
        v_flip_path = self.v_flip(index_path)
        self.add_vert(v_flip_path, ratio_u, 1.0 - ratio_v,
                      **{**kwargs, **extra_args})
    
    # Make sure equivalent symmetric vertices are set
    if 'u_boundary' in kwargs:
      self.set_u_equivalent_vert(index_path, vert, **kwargs)
    if 'v_boundary' in kwargs:
      self.set_v_equivalent_vert(index_path, vert, **kwargs)
    if 'corner' in kwargs:
      self.set_u_equivalent_vert(index_path, vert, **kwargs)
      self.set_v_equivalent_vert(index_path, vert, **kwargs)
      self.set_uv_equivalent_vert(index_path, vert, **kwargs)
      
    return vert

  def set_equivalent_vert(self, neighbor_keys, index_path, vert, **kwargs):
    if not vert:
      return None
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    tile.set_vert(index_path, vert)

  def set_u_equivalent_vert(self, index_path, vert, **kwargs):
    u_index = self.u_index(index_path)
    u_flip_path = self.u_flip(index_path)
    self.set_equivalent_vert([u_index], u_flip_path, vert, **kwargs)

  def set_v_equivalent_vert(self, index_path, vert, **kwargs):
    v_index = self.v_index(index_path)
    v_flip_path = self.v_flip(index_path)
    self.set_equivalent_vert([v_index], v_flip_path, vert, **kwargs)

  def set_uv_equivalent_vert(self, index_path, vert, **kwargs):
    u_index = self.u_index(index_path)
    v_index = self.v_index(index_path)
    u_flip_path = self.u_flip(index_path)
    uv_flip_path = self.v_flip(u_flip_path)
    self.set_equivalent_vert([u_index, v_index], uv_flip_path, vert, **kwargs)

  def add_face(self, index_path, vert_index_paths, **kwargs):
    if self.get_face(index_path):
      return None

    verts = []
    for vert_index_path in vert_index_paths:
      if isinstance(vert_index_path[0], list):
        vert = self.get_neighbor_vert(vert_index_path[0], vert_index_path[1])
      else:
        vert = self.get_vert(vert_index_path)
      if not vert: return None
      verts.append(vert)

    face = self.mesh_adaptor.create_face(verts)

    self.set_face(index_path, face)
    if 'face_type' in kwargs:
      if not kwargs['face_type'] in self.tessagon.face_types:
        self.tessagon.face_types[kwargs['face_type']] = []
      self.tessagon.face_types[kwargs['face_type']].append(face)

    if not 'symmetry' in kwargs:
      extra_args = { 'symmetry': True}
      if self.u_symmetric:
        # Add reflection about u
        u_flip_path = self.u_flip(index_path)
        u_flip_verts_paths = self.u_flip(vert_index_paths)
        self.add_face(u_flip_path, u_flip_verts_paths, **{**kwargs, **extra_args})
        if self.v_symmetric:
          # Add diagonally across
          uv_flip_path = self.v_flip(u_flip_path)
          uv_flip_verts_paths = self.v_flip(u_flip_verts_paths)
          self.add_face(uv_flip_path, uv_flip_verts_paths, **{**kwargs, **extra_args})
      if self.v_symmetric:
        # Add reflection about v
        v_flip_path = self.v_flip(index_path)
        v_flip_verts_paths = self.v_flip(vert_index_paths)
        self.add_face(v_flip_path, v_flip_verts_paths, **{**kwargs, **extra_args})

    # Make sure equivalent symmetric faces are set
    if 'u_boundary' in kwargs:
      self.set_u_equivalent_face(index_path, face, **kwargs)
    if 'v_boundary' in kwargs:
      self.set_v_equivalent_face(index_path, face, **kwargs)
    if 'corner' in kwargs:
      self.set_u_equivalent_face(index_path, face, **kwargs)
      self.set_v_equivalent_face(index_path, face, **kwargs)
      self.set_uv_equivalent_face(index_path, face, **kwargs)

    return face

  def set_equivalent_face(self, neighbor_keys, index_path, face, **kwargs):
    tile = self.get_neighbor_path(neighbor_keys)
    if not tile:
      return None
    tile.set_face(index_path, face)

  def set_u_equivalent_face(self, index_path, face, **kwargs):
    u_index = self.u_index(index_path)
    u_flip_path = self.u_flip(index_path)
    self.set_equivalent_face([u_index], u_flip_path, face, **kwargs)

  def set_v_equivalent_face(self, index_path, face, **kwargs):
    v_index = self.v_index(index_path)
    v_flip_path = self.v_flip(index_path)
    self.set_equivalent_face([v_index], v_flip_path, face, **kwargs)

  def set_uv_equivalent_face(self, index_path, face, **kwargs):
    u_index = self.u_index(index_path)
    v_index = self.v_index(index_path)
    u_flip_path = self.u_flip(index_path)
    uv_flip_path = self.v_flip(u_flip_path)
    self.set_equivalent_face([u_index, v_index], uv_flip_path, face, **kwargs)
