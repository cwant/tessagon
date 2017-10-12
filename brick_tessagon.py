from importlib import reload
import tile
import tessagon

from tessagon import Tessagon
from tile import Tile

class BrickTile(Tile):
  #                 top
  #
  #    -o..o-      -o..o- r
  # ^  .|..|.    l .|..|. i
  # |  .o--o.    e .o--o. g
  # |  .|..|.    f .|..|. h
  # |  -o..o-    t -o..o- t
  # V
  #   U --->       bottom

  def init_verts(self):
    return { 'left': {'top': None, 'middle': None, 'bottom': None },
             'right': {'top': None, 'middle': None, 'bottom': None } }

  def init_faces(self):
    return { 'left': None, 'right': None, 'top': None, 'bottom': None }

  def calculate_verts(self):
    # corners
    vert = self.add_vert(['left', 'bottom'], *self.blend(0.25, 0.0))
    self.set_equivalent_vert(['bottom'], ['left', 'top'], vert)

    vert = self.add_vert(['right', 'bottom'], *self.blend(0.75, 0.0))
    self.set_equivalent_vert(['bottom'], ['right', 'top'], vert)

    vert = self.add_vert(['left', 'top'], *self.blend(0.25, 1.0))
    self.set_equivalent_vert(['top'], ['left', 'bottom'], vert)

    vert = self.add_vert(['right', 'top'], *self.blend(0.75, 1.0))
    self.set_equivalent_vert(['top'], ['right', 'bottom'], vert)

    # middle
    self.add_vert(['left', 'middle'], *self.blend(0.25, 0.5))
    self.add_vert(['right', 'middle'], *self.blend(0.75, 0.5))

  def calculate_faces(self):
    face = self.add_face('left',
                         [self.get_vert(['left','top']),
                          self.get_vert(['left', 'middle']),
                          self.get_vert(['left', 'bottom']),
                          self.get_neighbor_vert(['left'], ['right', 'bottom']),
                          self.get_neighbor_vert(['left'], ['right', 'middle']),
                          self.get_neighbor_vert(['left'], ['right', 'top'])])
    self.set_equivalent_face(['left'], 'right', face)

    face = self.add_face('right',
                         [self.get_vert(['right','top']),
                          self.get_vert(['right', 'middle']),
                          self.get_vert(['right', 'bottom']),
                          self.get_neighbor_vert(['right'], ['left', 'bottom']),
                          self.get_neighbor_vert(['right'], ['left', 'middle']),
                          self.get_neighbor_vert(['right'], ['left', 'top'])])
    self.set_equivalent_face(['right'], 'left', face)

    face = self.add_face('bottom',
                         [self.get_vert(['left', 'middle']),
                          self.get_vert(['left', 'bottom']),
                          self.get_neighbor_vert(['bottom'], ['left', 'middle']),
                          self.get_neighbor_vert(['bottom'], ['right', 'middle']),
                          self.get_vert(['right', 'bottom']),
                          self.get_vert(['right', 'middle'])])
    self.set_equivalent_face(['bottom'], 'top', face)

    face = self.add_face('top',
                         [self.get_vert(['left', 'middle']),
                          self.get_vert(['left', 'top']),
                          self.get_neighbor_vert(['top'], ['left', 'middle']),
                          self.get_neighbor_vert(['top'], ['right', 'middle']),
                          self.get_vert(['right', 'top']),
                          self.get_vert(['right', 'middle'])])
    self.set_equivalent_face(['top'], 'bottom', face)

class BrickTessagon(Tessagon):
  def init_tile_class(self):
    return BrickTile
