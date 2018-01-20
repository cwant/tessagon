from math import sqrt

from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon

class SquareTri2Tile(Tile):
  # 12 verts, 15 faces (9 internal, 6 on boundary)
  #     
  #  ^  --1---2-- row5   --o---o--  
  #  |  ..|...|..        11|12.|13  row4
  #  |  --3---4-- row4   --o---o--
  #  |  ./.\./.\.        1/2\3/4\5  row3
  #     5---6---7 row3   o---o---o
  #  V  |...|...|        |14.|15.|  row2
  #     8---9--10 row2   o---o---o
  #     .\./.\./.        6\7/8\9/10 row1
  #     -11--12-- row1   --o---o--
  #
  #      U ----->  

  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)
    self.u_symmetric = True
    self.v_symmetric = False

  def init_verts(self):
    return { 'left': { 'row1': None,
                       'row2': None,
                       'row3': None,
                       'row4': None,
                       'row5': None },
             'right': { 'row1': None,
                        'row2': None,
                        'row3': None,
                        'row4': None,
                        'row5': None },
             'middle': { 'row2': None,
                         'row3': None } }

  def init_faces(self):
    return { 'left': { 'row1': { 'inner': None,
                                 'outer': None },
                       'row2': None,
                       'row3': { 'inner': None,
                                 'outer': None },
                       'row4': None },
             'right': { 'row1': { 'inner': None,
                                  'outer': None },
                        'row2': None,
                        'row3': { 'inner': None,
                                  'outer': None },
                        'row4': None },
             'middle': { 'row1': None,
                         'row3': None,
                         'row4': None, } }

  def calculate_verts(self):
    # u_unit is the length of the edges expressed as a proportion of the tile
    u0 = 0
    u1 = 0.25
    u2 = 0.5
    u3 = 0.75
    u4 = 1.0

    v_denom = 2 + sqrt(3)
    v_unit1 = 1 / v_denom
    v_unit2 = sqrt(3) / (2 * v_denom)
    v0 = 0
    v1 = v_unit2
    v2 = v1 + v_unit1
    v3 = v2 + v_unit2
    v4 = 1.0

    # Other verts defined through symmetry
    vert = self.add_vert(['left', 'row1'], u1, v0)
    self.set_equivalent_vert(['bottom'], ['left', 'row5'], vert)
    self.add_vert(['left', 'row2'], u0, v1, u_boundary=True)
    self.add_vert(['left', 'row3'], u0, v2, u_boundary=True)
    self.add_vert(['left', 'row4'], u1, v3)
    vert = self.add_vert(['left', 'row5'], u1, v4)
    self.set_equivalent_vert(['top'], ['left', 'row1'], vert)

    self.add_vert(['middle', 'row2'], u2, v1)
    self.add_vert(['middle', 'row3'], u2, v2)

    # Don't know why I have to do the next two lines to make the topology
    # right, needs debugging
    vert = self.add_vert(['right', 'row1'], u1, v0)
    self.set_equivalent_vert(['bottom'], ['right', 'row5'], vert)
    vert = self.add_vert(['right', 'row5'], u1, v4)
    self.set_equivalent_vert(['top'], ['right', 'row1'], vert)

  def calculate_faces(self):
    self.add_face(['left', 'row1', 'outer'],
                  [['left', 'row2'],
                   ['left', 'row1'],
                   [['left'], ['right', 'row1']]],
                  face_type='triangle', u_boundary=True)

    self.add_face(['left', 'row1', 'inner'],
                  [['left', 'row2'],
                   ['left', 'row1'],
                   ['middle', 'row2']],
                  face_type='triangle')

    self.add_face(['middle', 'row1'],
                  [['left', 'row1'],
                   ['middle', 'row2'],
                   ['right', 'row1']],
                  face_type='triangle')

    self.add_face(['left', 'row2'],
                  [['left', 'row2'],
                   ['middle', 'row2'],
                   ['middle', 'row3'],
                   ['left', 'row3']],
                  face_type='square')

    self.add_face(['left', 'row3', 'outer'],
                  [['left', 'row3'],
                   ['left', 'row4'],
                   [['left'], ['right', 'row4']]],
                  face_type='triangle', u_boundary=True)

    self.add_face(['left', 'row3', 'inner'],
                  [['left', 'row3'],
                   ['left', 'row4'],
                   ['middle', 'row3']],
                  face_type='triangle')

    self.add_face(['middle', 'row3'],
                  [['left', 'row4'],
                   ['middle', 'row3'],
                   ['right', 'row4']],
                  face_type='triangle')

    self.add_face(['left', 'row4'],
                  [['left', 'row5'],
                   ['left', 'row4'],
                   [['left'], ['right', 'row4']],
                   [['left'], ['right', 'row5']]],
                  face_type='square', u_boundary=True)

    self.add_face(['middle', 'row4'],
                  [['left', 'row5'],
                   ['left', 'row4'],
                   ['right', 'row4'],
                   ['right', 'row5']],
                  face_type='square')

class SquareTri2Tessagon(Tessagon):
  tile_class = SquareTri2Tile
