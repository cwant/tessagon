from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon

class TriTile(Tile):
  #  ^  0.|.1   This is the topology of the tile.
  #  |  |\|/|   (Not a Dead Kennedy's logo ...).
  #  |  |.2.|
  #  |  |/|\|
  #  V  3.|.4
  #
  #  U ----->

  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)
    self.u_symmetric = True
    self.v_symmetric = True


  def init_verts(self):
    return { 'left': {'top': None, 'bottom': None },
             'middle': None,
             'right': {'top': None, 'bottom': None } }

  def init_faces(self):
    return { 'left': {'top': None, 'middle': None, 'bottom': None },
             'right': {'top': None, 'middle': None, 'bottom': None } }

  def calculate_verts(self):
    # Four corners, via symmetry
    self.add_vert(['left', 'top'], 0, 1, corner=True)
    # The middle vert
    self.add_vert('middle', 0.5, 0.5)

  def calculate_faces(self):
    # Four corners, via symmetry
    self.add_face(['left', 'top'],
                  [['left','top'],
                   ['middle'],
                   # Vert on neighboring tile
                   [['top'], ['middle']]], v_boundary=True)
    # Two interior faces, via symmetry
    self.add_face(['left', 'middle'],
                  [['left', 'top'],
                   ['left', 'bottom'],
                   ['middle']])

class TriTessagon(Tessagon):
  def init_tile_class(self):
    return TriTile
