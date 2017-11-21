from tessagon.core.stamp14_tessagon import Stamp14, Stamp14Tile, Stamp14Tessagon

# To get a sense of how Florets repeat over tiles, see:
#   https://github.com/cwant/tessagon/blob/master/documentation/images/florets_repeat.png
# To see how the Florets are arranged on a tile, see:
#   https://github.com/cwant/tessagon/blob/master/documentation/images/florets_tiles.png
# To see how Floret neighbors, verts and faces are arranged, see:
#   https://github.com/cwant/tessagon/blob/master/documentation/images/florets_neighbors_verts_faces.png

class Floret(Stamp14):
  def init_verts(self):
    return [None]*19

  def init_faces(self):
    return [None]*6

  def add_offset_vert(self, i, offset_u, offset_v):
    vert = super().add_offset_vert(i, offset_u, offset_v)
    if vert:
      if i == 18:
        self.tile.tessagon.vert_types['center'].append(vert)
      elif i % 3 == 2:
        self.tile.tessagon.vert_types['other'].append(vert)
      else:
        self.tile.tessagon.vert_types['edge_to_center'].append(vert)
    return True

  def calculate_verts(self):
    self.add_offset_vert(18, 0, 0)

    unit_u = 2.0 / 42.0
    unit_v = 1.0 / 14.0

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

class FloretTile(Stamp14Tile):
  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, Floret, **kwargs)

class FloretTessagon(Stamp14Tessagon):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.vert_types = { 'center': [], 'edge_to_center': [], 'other': [] }

  def init_tile_class(self):
    return FloretTile
