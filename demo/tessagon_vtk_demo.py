import os, sys
import vtk
from vtk.util.colors import tomato

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.adaptors.vtk_adaptor import VtkAdaptor

from tessagon.types import *
from tessagon.misc.shapes import *

lut = None

class VtkDemo:
  def __init__(self):
    self.ren = vtk.vtkRenderer()
    self.renWin = vtk.vtkRenderWindow()
    self.renWin.AddRenderer(self.ren)
    self.iren = vtk.vtkRenderWindowInteractor()
    self.iren.SetRenderWindow(self.renWin)

    self.lut = vtk.vtkLookupTable()
    self.lut.SetHueRange(0.6, 0.6)
    self.lut.SetSaturationRange(.5, .5)
    self.lut.SetValueRange(0.2, 1.0)
    self.lut.SetNumberOfColors(256)
    self.lut.Build()

  def main(self):
    self.create_objects()
    self.interact()

  def create_objects(self):
    offset = 15
    row = 0
    column = 0
    # Color patterns
    self.hex_tessagon([column, row, 0])
    self.hex_tessagon([column, row - offset, 0], color_pattern=1)
    self.hex_tessagon([column, row - 2*offset, 0], color_pattern=2)
    column += offset
    self.tri_tessagon([column, row, 0])
    self.tri_tessagon([column, row - offset, 0], color_pattern=1)
    self.tri_tessagon([column, row - 2*offset, 0], color_pattern=2)
    self.tri_tessagon([column, row - 3*offset, 0], color_pattern=3)
    column += offset
    self.dissected_square_tessagon([column, row, 0])
    self.dissected_square_tessagon([column, row - offset, 0], color_pattern=1)
    self.dissected_square_tessagon([column, row - 2*offset, 0],
                                   color_pattern=2)
    column += offset
    self.floret_tessagon([column, row, 0])
    self.floret_tessagon([column, row - offset, 0], color_pattern=1)
    self.floret_tessagon([column, row - 2*offset, 0], color_pattern=2)
    self.floret_tessagon([column, row - 3*offset, 0], color_pattern=3)
    column += offset
    column += offset
    start_column = column

    # Row 1
    self.rhombus_tessagon([column, row, 0])
    column += offset
    self.octo_tessagon([column, row, 0])
    column += offset
    self.hex_tri_tessagon([column, row, 0])
    column += offset
    self.hex_square_tri_tessagon([column, row, 0])

    column = start_column
    row -= offset
    # Row 2
    self.square_tessagon([column, row, 0])
    column += offset
    self.pythagorean_tessagon([column, row, 0])
    column += offset
    self.brick_tessagon([column, row, 0])
    column += offset
    self.dodeca_tessagon([column, row, 0])

    column = start_column
    row -= offset
    # Row 3
    self.square_tri_tessagon([column, row, 0])
    column += offset
    self.weave_tessagon([column, row, 0])
    column += offset
    self.hex_big_tri_tessagon([column, row, 0])
    column += offset
    self.zig_zag_tessagon([column, row, 0])

  def interact(self):
    self.ren.SetBackground(0.3, 0.3, 0.3)
    self.renWin.SetSize(800, 600)
    self.iren.Initialize()
    self.ren.ResetCamera()
    self.renWin.Render()
    self.iren.Start()

  def tessellate(self, f, tessagon_class, **kwargs):
    extra_args = {'function': f,
                  'adaptor_class' : VtkAdaptor}
    tessagon = tessagon_class(**{**kwargs, **extra_args})

    poly_data = tessagon.create_mesh()
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(poly_data)
    mapper.SetLookupTable(self.lut)
    mapper.SetScalarRange(poly_data.GetScalarRange())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(tomato)
    actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)
    actor.GetProperty().EdgeVisibilityOn()
    actor.SetPosition(kwargs['position'])

    self.ren.AddActor(actor)

  def rotated_cylinder(self, u,v):
    (x, y, z) = cylinder(u, v)
    return [x, z, y]

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
    return self.tessellate(self.rotated_cylinder, HexTessagon,
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

  def rhombus_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 40,
      'v_num': 6,
      'v_twist': True,
      'position': position
    }
    return self.tessellate(klein, RhombusTessagon, **options)

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

  def square_tessagon(self, position):
    options = {
      'u_range': [0.0, 1.0],
      'v_range': [0.0, 1.0],
      'u_num': 15,
      'v_num': 4,
      'rot_factor': 2,
      'position': position
    }
    return self.tessellate(torus, SquareTessagon, **options)

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

  def floret_torus(self, u, v):
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
    return self.tessellate(self.floret_torus, FloretTessagon,
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
    return self.tessellate(self.rotated_cylinder, DissectedSquareTessagon,
                           **{**kwargs, **options})
VtkDemo().main()
