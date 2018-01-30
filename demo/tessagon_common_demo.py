from tessagon.types import *
from tessagon.misc.shapes import *

class TessagonCommonDemo:

  # This is an abstract class that handles common code for the
  # demos. Each subclass needs to implement the 'tessellate' method
  # which instantiates each tessagon class, creates a mesh, and puts it
  # in the scene for the particular software package.

  def create_objects(self):
    # Two grids of objects, colored ones on one side, non-colored on the other

    offset = 15
    row = 0
    column = 0
    # Color patterns
    self.hex_tessagon([column, 0, row])
    for i in range(HexTessagon.num_color_patterns()):
      color_pattern = i+1
      self.hex_tessagon([column, 0, row - color_pattern * offset],
                        color_pattern=color_pattern)
    column += offset

    self.tri_tessagon([column, 0, row])
    for i in range(TriTessagon.num_color_patterns()):
      color_pattern = i+1
      self.tri_tessagon([column, 0, row - color_pattern * offset],
                        color_pattern=color_pattern)
    column += offset

    self.dissected_square_tessagon([column, 0, row])
    for i in range(DissectedSquareTessagon.num_color_patterns()):
      color_pattern = i+1
      self.dissected_square_tessagon([column, 0, row - color_pattern * offset],
                                     color_pattern=color_pattern)
    column += offset

    self.floret_tessagon([column, 0, row])
    for i in range(FloretTessagon.num_color_patterns()):
      color_pattern = i+1
      self.floret_tessagon([column, 0, row - color_pattern * offset],
                           color_pattern=color_pattern)
    column += offset

    self.square_tessagon([column, 0, row])
    for i in range(SquareTessagon.num_color_patterns()):
      color_pattern = i+1
      self.square_tessagon([column, 0, row - color_pattern * offset],
                           color_pattern=color_pattern)

    # Non-colored objects
    column += offset
    column += offset
    start_column = column
    # Row 1
    self.rhombus_tessagon([column, 0, row])
    column += offset
    self.octo_tessagon([column, 0, row])
    column += offset
    self.hex_tri_tessagon([column, 0, row])
    column += offset
    self.hex_square_tri_tessagon([column, 0, row])

    column = start_column
    row -= offset
    # Row 2
    self.pythagorean_tessagon([column, 0, row])
    column += offset
    self.brick_tessagon([column, 0, row])
    column += offset
    self.dodeca_tessagon([column, 0, row])
    column += offset
    self.zig_zag_tessagon([column, 0, row])

    column = start_column
    row -= offset
    # Row 3
    self.square_tri_tessagon([column, 0, row])
    column += offset
    self.weave_tessagon([column, 0, row])
    column += offset
    self.hex_big_tri_tessagon([column, 0, row])
    column += offset
    self.square_tri2_tessagon([column, 0, row])

    column = start_column
    row -= offset
    # Row 3
    self.dodeca_tri_tessagon([column, 0, row])
    column += offset
    self.dissected_triangle_tessagon([column, 0, row])
    column += offset
    self.dissected_hex_quad_tessagon([column, 0, row])
    column += offset
    self.dissected_hex_tri_tessagon([column, 0, row])

    column = start_column
    row -= offset
    # Row 4
    self.penta_tessagon([column, 0, row])
    column += offset
    self.penta2_tessagon([column, 0, row])

  def hex_tessagon(self, position, **kwargs):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 45,
      'v_num': 3,
      'u_cyclic': True,
      'v_cyclic': False,
      'position': position
    }
    return self.tessellate(cylinder, HexTessagon,
                           **{**kwargs, **options})

  def tri_tessagon(self, position, **kwargs):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 36,
      'v_num': 12,
      'position': position
    }
    return self.tessellate(torus, TriTessagon, **{**kwargs, **options})

  def square_tessagon(self, position, **kwargs):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 24,
      'v_num': 6,
      'rot_factor': 2,
      'position': position
    }
    return self.tessellate(torus, SquareTessagon, **{**kwargs, **options})

  def rhombus_klein(self, u, v):
    (x, y, z) = klein(u, v)
    return (x, z, -y)

  def rhombus_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 40,
      'v_num': 6,
      'v_twist': True,
      'position': position
    }
    return self.tessellate(self.rhombus_klein, RhombusTessagon, **options)

  def octo_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 4,
      'v_num': 40,
      'v_cyclic': True,
      'u_cyclic': False,
      'u_twist': True,
      'position': position
    }
    return self.tessellate(mobius, OctoTessagon, **options)

  def hex_tri_tessagon(self, position):
    options = {
      'u_range': [-1.0, 1.0],
      'v_range': [-1.0, 1.0],
      'u_num': 15,
      'v_num': 10,
      'u_cyclic': False,
      'v_cyclic': False,
      'position': position
    }
    return self.tessellate(paraboloid, HexTriTessagon, **options)

  def hex_square_tri_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 45,
      'v_num': 5,
      'position': position
    }
    return self.tessellate(torus, HexSquareTriTessagon, **options)

  def pythagorean_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 25,
      'v_num': 6,
      'position': position
    }
    return self.tessellate(torus, PythagoreanTessagon, **options)

  def brick_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 15,
      'v_num': 3,
      'rot_factor': 3,
      'position': position
    }
    return self.tessellate(torus, BrickTessagon, **options)

  def dodeca_tessagon(self, position):
    options = {
      'u_range': [-1.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 4,
      'v_num': 10,
      'u_cyclic': False,
      'v_cyclic': True,
      'position': position
    }
    return self.tessellate(one_sheet_hyperboloid, DodecaTessagon, **options)

  def square_tri_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 20,
      'v_num': 4,
      'position': position
    }
    return self.tessellate(torus, SquareTriTessagon, **options)

  def weave_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 8,
      'v_num': 6,
      'v_cyclic': False,
      'rot_factor': 1,
      'position': position
    }
    return self.tessellate(sphere, WeaveTessagon, **options)

  def chubby_torus(self, u, v):
    # u_cyclic = True, v_cyclic = True
    r1 = 5.0
    r2 = 1.5
    return general_torus(r1, r2, v, warp_var(u, 0.2))

  def floret_tessagon(self, position, **kwargs):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 2,
      'v_num': 12,
      'position': position
    }
    return self.tessellate(self.chubby_torus, FloretTessagon,
                           **{**kwargs, **options})

  def hex_big_tri_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 5,
      'v_num': 2,
      'position': position
    }
    return self.tessellate(torus, HexBigTriTessagon, **options)

  def zig_zag_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 10,
      'v_num': 2,
      'rot_factor': 2,
      'position': position
    }
    return self.tessellate(torus, ZigZagTessagon, **options)

  def dissected_square_tessagon(self, position, **kwargs):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 32,
      'v_num': 4,
      'u_cyclic': True,
      'v_cyclic': False,
      'position': position
    }
    return self.tessellate(cylinder, DissectedSquareTessagon,
                           **{**kwargs, **options})

  def square_tri2_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 35,
      'v_num': 3,
      'v_cyclic': False,
      'position': position
    }
    return self.tessellate(cylinder, SquareTri2Tessagon, **options)

  def dodeca_tri_tessagon(self, position):
    options = {
      'u_range': [-1.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 3,
      'v_num': 20,
      'u_cyclic': False,
      'v_cyclic': True,
      'position': position
    }
    return self.tessellate(one_sheet_hyperboloid, DodecaTriTessagon, **options)

  def dissected_triangle2_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 10,
      'v_num': 2,
      'rot_factor': 2,
      'position': position
    }
    return self.tessellate(torus, DissectedTriangleTessagon, **options)

  def dissected_triangle_tessagon(self, position, **kwargs):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 16,
      'v_num': 3,
      'u_cyclic': True,
      'v_cyclic': False,
      'position': position
    }
    return self.tessellate(cylinder, DissectedTriangleTessagon,
                           **{**kwargs, **options})

  def dissected_hex_quad_tessagon(self, position, **kwargs):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 10,
      'v_num': 20,
      'u_cyclic': True,
      'v_cyclic': True,
      'position': position
    }
    return self.tessellate(self.chubby_torus, DissectedHexQuadTessagon,
                           **{**kwargs, **options})

  def dissected_hex_tri_tessagon(self, position, **kwargs):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 10,
      'v_num': 20,
      'u_cyclic': True,
      'v_cyclic': True,
      'position': position
    }
    return self.tessellate(self.chubby_torus, DissectedHexTriTessagon,
                           **{**kwargs, **options})

  def penta_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 20,
      'v_num': 4,
      'position': position
    }
    return self.tessellate(torus, PentaTessagon, **options)

  def penta2_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 50,
      'v_num': 4,
      'position': position
    }
    return self.tessellate(torus, Penta2Tessagon, **options)
