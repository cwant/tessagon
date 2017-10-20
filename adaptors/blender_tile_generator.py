class BlenderTileGenerator:
  def __init__(self, tessagon, **kwargs):
    self.tessagon = tessagon
    self.bmesh = kwargs['mesh']

  def create_tiles(self):
    tiles = []
    for face in self.bmesh.faces:
      if face.verts.count == 4:
        corners = [ face.verts[0].
