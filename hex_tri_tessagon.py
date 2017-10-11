from importlib import reload
import tile, tessagon
reload(tile)
reload(tessagon)

from tile import Tile
from tessagon import Tessagon

class HexTriTile(Tile):
  #    ....o....  .6..o..6.
  #    .../.\...  .../3\...
  #  ^ --o---o--  --o---o--
  #  | ./.....\.  3/.....\3
  #  | o.......o  o...6...o
  #  | .\...../.  3\...../3
  #  | --o---o--  --o---o--
  #    ...\./...  ...\3/...
  #  V ....o ...  .6..o..6.
  #
  #     U ------>
  def init_verts(self):
    return { 'top': None,
             'left': { 'top': None,
                       'middle': None,
                       'bottom': None },
             'right':  { 'top': None,
                         'middle': None,
                         'bottom': None },
             'bottom': None
    }

  def init_faces(self):
    return { 'center': { 'top': None,
                         'middle': None,
                         'bottom': None },
             'left': { 'top': None,
                       'uppermiddle': None,
                       'lowermiddle': None,
                       'bottom': None },
             'right': { 'top': None,
                        'uppermiddle': None,
                        'lowermiddle': None,
                        'bottom': None } }

  def calculate_verts(self):
    # top vert
    vert = self.add_vert('top', *self.blend(0.5, 1))
    self.set_equivalent_vert(['top'], 'bottom', vert)

    # bottom vert
    vert = self.add_vert('bottom', *self.blend(0.5, 0))
    self.set_equivalent_vert(['bottom'], 'top', vert)

    # left verts
    self.add_vert(['left', 'top'], *self.blend(0.25, 0.75))

    vert = self.add_vert(['left', 'middle'], *self.blend(0, 0.5))
    self.set_equivalent_vert(['left'], ['right', 'middle'], vert)

    self.add_vert(['left', 'bottom'], *self.blend(0.25, 0.25))

    # right verts
    self.add_vert(['right', 'top'], *self.blend(0.75, 0.75))

    vert = self.add_vert(['right', 'middle'], *self.blend(1, 0.5))
    self.set_equivalent_vert(['right'], ['left', 'middle'], vert)

    self.add_vert(['right', 'bottom'], *self.blend(0.75, 0.25))

  def calculate_faces(self):
    self.center_faces()
    self.left_faces()
    self.right_faces()

  def center_faces(self):
    # Top / bottom triangles
    for top_bottom in ['top', 'bottom']:
      self.add_face(['center', top_bottom],
                    [self.get_vert(top_bottom),
                     self.get_vert(['left', top_bottom]),
                     self.get_vert(['right', top_bottom])],
                    face_type='triangle')
    # Middle hexagon
    self.add_face(['center', 'middle'],
                  [self.get_vert(['left', 'top']),
                   self.get_vert(['left', 'middle']),
                   self.get_vert(['left', 'bottom']),
                   self.get_vert(['right', 'bottom']),
                   self.get_vert(['right', 'middle']),
                   self.get_vert(['right', 'top'])],
                  face_type='hexagon')

  def left_top_face(self):
    verts = [self.get_vert('top'),
             self.get_vert(['left', 'top']),
             self.get_neighbor_vert(['left'], ['right', 'top']),
             self.get_neighbor_vert(['left'], 'top'),
             self.get_neighbor_vert(['left', 'top'], ['right', 'bottom']),
             self.get_neighbor_vert(['top'], ['left', 'bottom'])]

    face = self.add_face(['left', 'top'], verts, face_type='hexagon')
    self.set_equivalent_face(['left'], ['right', 'top'], face)
    self.set_equivalent_face(['top', 'left'], ['right', 'bottom'], face)
    self.set_equivalent_face(['top'], ['left', 'bottom'], face)

  def left_faces(self):
    # Hexagons
    self.left_top_face()

    tile = self.get_neighbor_path(['bottom'])
    if not tile:
      return None
    tile.left_top_face()

    # Triangles
    verts = [self.get_vert(['left', 'top']),
             self.get_vert(['left', 'middle']),
             self.get_neighbor_vert(['left'], ['right', 'top'])]
    face = self.add_face(['left', 'uppermiddle'], verts, face_type='triangle')
    self.set_equivalent_face(['left'], ['right', 'uppermiddle'], face)

    verts = [self.get_vert(['left', 'bottom']),
             self.get_vert(['left', 'middle']),
             self.get_neighbor_vert(['left'], ['right', 'bottom'])]
    face = self.add_face(['left', 'lowermiddle'], verts, face_type='triangle')
    self.set_equivalent_face(['left'], ['right', 'lowermiddle'], face)

  def right_faces(self):
    tile = self.get_neighbor_path(['right'])
    if not tile:
      return None
    tile.left_faces()

class HexTriTessagon(Tessagon):
  def init_tile_class(self):
    return HexTriTile
