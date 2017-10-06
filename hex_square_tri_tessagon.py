from math import sqrt

from importlib import reload
import tile, tessagon
reload(tile)
reload(tessagon)

from tile import Tile
from tessagon import Tessagon

class HexSquareTriTile(Tile):
  # 14 verts, 19 faces (7 internal, 12 on boundary)
  # The angles make it hard to draw all edges, some excluded
  #
  #  ...|...|...  6..|.4.|..6
  #  ...o---o...  ...o---o...
  #  o ..\./...o  o.4.\3/.4.o
  #  .\...o.../.  3\...o.../3 Numbers are faces with # sides
  #  --o.....o--  --o.....o--
  #  ..|.....|..  4.|..6..|.4
  #  --o.... o--  --o.... o--
  #  ./.. o...\.  3/.. o...\3
  #  o.../.\...o  o.4./3\.4.o
  #  ...o---o...  ...o---o...
  #  ...|...|...  6..|.4.|..6

  def init_verts(self):
    return { 'left': { 'top': None,
                       'uppermiddle': None,
                       'lowermiddle': None,
                       'bottom': None },
             'right': { 'top': None,
                        'uppermiddle': None,
                        'lowermiddle': None,
                        'bottom': None },
             'top': { 'left': None,
                      'middle': None,
                      'right': None },
             'bottom': { 'left': None,
                         'middle': None,
                         'right': None }
    }

  def calculate_verts(self):
    ulen = 1.0 / (1.0 + sqrt(3))
    u0 = self.u_range[0]
    u1 = self.blend(self.u_range, 0.5*ulen)
    u2 = self.blend(self.u_range, 0.5*(1.0-ulen))
    u3 = self.blend(self.u_range, 0.5)
    u4 = self.blend(self.u_range, 0.5*(1.0+ulen))
    u5 = self.blend(self.u_range, 1.0 - 0.5*ulen)
    u6 = self.u_range[1]

    vlen = 1.0 / (3.0 + sqrt(3))
    v0 = self.blend(self.v_range, 0.5*vlen)
    v1 = self.blend(self.v_range, vlen)
    v2 = self.blend(self.v_range, 0.5 - vlen)
    v3 = self.blend(self.v_range, 2.0*vlen)
    v4 = self.blend(self.v_range, 1.0 - 2.0*vlen)
    v5 = self.blend(self.v_range, 0.5 + vlen)
    v6 = self.blend(self.v_range, 1.0 - vlen)
    v7 = self.blend(self.v_range, 1.0 - 0.5*vlen)

    # Top triangle
    self.add_vert(['top', 'left'], u2, v0)
    self.add_vert(['top', 'middle'], u3, v2)
    self.add_vert(['top', 'right'], u4, v0)

    # Bottom triangle
    self.add_vert(['bottom', 'left'], u2, v7)
    self.add_vert(['bottom', 'middle'], u3, v5)
    self.add_vert(['bottom', 'right'], u4, v7)

    # Left verts
    vert = self.add_vert(['left','top'], u0, v1)
    self.set_equivalent_vert(['left'], ['right', 'top'], vert)
    self.add_vert(['left','uppermiddle'], u1, v3)
    self.add_vert(['left','lowermiddle'], u1, v4)
    vert = self.add_vert(['left','bottom'], u0, v6)
    self.set_equivalent_vert(['left'], ['right', 'bottom'], vert)

    # Right verts
    vert = self.add_vert(['right','top'], u6, v1)
    self.set_equivalent_vert(['right'], ['left', 'top'], vert)
    self.add_vert(['right','uppermiddle'], u5, v3)
    self.add_vert(['right','lowermiddle'], u5, v4)
    vert = self.add_vert(['right','bottom'], u6, v6)
    self.set_equivalent_vert(['right'], ['left', 'bottom'], vert)

  def init_faces(self):
    return { 'hex': { 'lefttop': None,
                      'righttop': None,
                      'middle': None,
                      'leftbottom': None,
                      'rightbottom': None },
             'tri': { 'top': None,
                      'lefttop': None,
                      'righttop': None,
                      'leftbottom': None,
                      'rightbottom': None,
                      'bottom': None },
             'square': { 'top': None,
                         'lefttop': None,
                         'righttop': None,
                         'left': None,
                         'right': None,
                         'leftbottom': None,
                         'rightbottom': None,
                         'bottom': None } }

  def calculate_faces(self):
    self.outer_faces()
    self.inner_faces()

  def outer_faces(self):
    # Left outer faces
    self.left_outer_faces()
    # Right outer faces
    tile = self.get_neighbor_path(['right'])
    if tile:
      tile.left_outer_faces()
    # Top square
    self.top_square()
    # Bottom square
    tile = self.get_neighbor_path(['bottom'])
    if tile:
      tile.top_square()

  def left_outer_faces(self):
    # Two hexes
    self.left_top_corner_hex()
    tile = self.get_neighbor_path(['bottom'])
    if tile:
      tile.left_top_corner_hex()
    # Two triangles
    verts = [self.get_vert(['left', 'top']),
             self.get_vert(['left', 'uppermiddle']),
             self.get_neighbor_vert(['left'], ['right', 'uppermiddle'])]
    face = self.add_face(['tri', 'lefttop'], verts, face_type='triangle')
    self.set_equivalent_face(['left'], ['tri', 'righttop'], face)
    verts = [self.get_vert(['left', 'bottom']),
            self.get_vert(['left', 'lowermiddle']),
             self.get_neighbor_vert(['left'], ['right', 'lowermiddle'])]
    face = self.add_face(['tri', 'leftbottom'], verts, face_type='triangle')
    self.set_equivalent_face(['left'], ['tri', 'rightbottom'], face)
    # One square
    verts = [self.get_vert(['left', 'uppermiddle']),
             self.get_vert(['left', 'lowermiddle']),
             self.get_neighbor_vert(['left'], ['right', 'lowermiddle']),
             self.get_neighbor_vert(['left'], ['right', 'uppermiddle'])]
    face = self.add_face(['square', 'left'], verts, face_type='square')
    self.set_equivalent_face(['left'], ['square', 'right'], face)

  def left_top_corner_hex(self):
    verts = [self.get_vert(['top', 'left']),
             self.get_vert(['left', 'top']),
             self.get_neighbor_vert(['left'], ['top', 'right']),
             self.get_neighbor_vert(['left', 'top'], ['bottom', 'right']),
             self.get_neighbor_vert(['top'], ['left', 'bottom']),
             self.get_neighbor_vert(['top'], ['bottom', 'left'])]

    face = self.add_face(['hex', 'lefttop'], verts, face_type='hexagon')
    self.set_equivalent_face(['left'], ['hex', 'righttop'], face)
    self.set_equivalent_face(['top', 'left'], ['hex', 'rightbottom'], face)
    self.set_equivalent_face(['top'], ['hex', 'leftbottom'], face)

  def top_square(self):
    verts = [self.get_vert(['top', 'left']),
             self.get_vert(['top', 'right']),
             self.get_neighbor_vert(['top'], ['bottom', 'right']),
             self.get_neighbor_vert(['top'], ['bottom', 'left'])]

    face = self.add_face(['square', 'top'], verts, face_type='square')
    self.set_equivalent_face(['top'], ['square', 'bottom'], face)

  def inner_faces(self):
    # Hexagon
    verts = [self.get_vert(['top', 'middle']),
             self.get_vert(['left', 'uppermiddle']),
             self.get_vert(['left', 'lowermiddle']),
             self.get_vert(['bottom', 'middle']),
             self.get_vert(['right', 'lowermiddle']),
             self.get_vert(['right', 'uppermiddle'])]
    self.add_face(['hex', 'middle'], verts, face_type='hexagon')

    # Top triangle
    verts = [self.get_vert(['top', 'left']),
             self.get_vert(['top', 'right']),
             self.get_vert(['top', 'middle'])]
    self.add_face(['tri', 'top'], verts, face_type='triangle')

    # Bottom triangle
    verts = [self.get_vert(['bottom', 'left']),
             self.get_vert(['bottom', 'right']),
             self.get_vert(['bottom', 'middle'])]
    self.add_face(['tri', 'bottom'], verts, face_type='triangle')

    # Lefttop square
    verts = [self.get_vert(['top', 'left']),
             self.get_vert(['top', 'middle']),
             self.get_vert(['left', 'uppermiddle']),
             self.get_vert(['left', 'top'])]
    self.add_face(['square', 'lefttop'], verts, face_type='square')

    # Righttop square
    verts = [self.get_vert(['top', 'right']),
             self.get_vert(['top', 'middle']),
             self.get_vert(['right', 'uppermiddle']),
             self.get_vert(['right', 'top'])]
    self.add_face(['square', 'righttop'], verts, face_type='square')

    # Leftbottom square
    verts = [self.get_vert(['bottom', 'left']),
             self.get_vert(['bottom', 'middle']),
             self.get_vert(['left', 'lowermiddle']),
             self.get_vert(['left', 'bottom'])]
    self.add_face(['square', 'leftbottom'], verts, face_type='square')

    # Rightbottom square
    verts = [self.get_vert(['bottom', 'right']),
             self.get_vert(['bottom', 'middle']),
             self.get_vert(['right', 'lowermiddle']),
             self.get_vert(['right', 'bottom'])]
    self.add_face(['square', 'rightbottom'], verts, face_type='square')

class HexSquareTriTessagon(Tessagon):
  def init_tile_class(self):
    return HexSquareTriTile
