import os, sys
import vtk
from vtk.util.colors import tomato

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.adaptors.vtk_adaptor import VtkAdaptor

from tessagon.types import *
from tessagon.misc.shapes import *

def main():
  ren = vtk.vtkRenderer()
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(ren)
  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)

  offset = 15
  # Row 1
  row1 = 0
  ren.AddActor(hex_tessagon([0, row1, 0]))
  ren.AddActor(tri_tessagon([offset, row1, 0]))
  ren.AddActor(tri_tessagon([offset, row1 - offset, 0], color_pattern=1))
  ren.AddActor(tri_tessagon([offset, row1 - 2*offset, 0], color_pattern=2))
  ren.AddActor(tri_tessagon([offset, row1 - 3*offset, 0], color_pattern=3))
  ren.AddActor(rhombus_tessagon([2*offset, row1, 0]))
  ren.AddActor(octo_tessagon([3*offset, row1, 0]))
  ren.AddActor(hex_tri_tessagon([4*offset, row1, 0]))
  ren.AddActor(hex_square_tri_tessagon([5*offset, row1, 0]))
  ren.AddActor(square_tessagon([6*offset, row1, 0]))
  ren.AddActor(pythagorean_tessagon([7*offset, row1, 0]))

  # Row 2
  row2 = -4 * offset
  ren.AddActor(brick_tessagon([0, row2, 0]))
  ren.AddActor(dodeca_tessagon([offset, row2, 0]))
  ren.AddActor(square_tri_tessagon([2*offset, row2, 0]))
  ren.AddActor(weave_tessagon([3*offset, row2, 0]))
  ren.AddActor(floret_tessagon([4*offset, row2, 0]))
  ren.AddActor(hex_big_tri_tessagon([5*offset, row2, 0]))
  ren.AddActor(zig_zag_tessagon([6*offset, row2, 0]))

  ren.SetBackground(0.3, 0.3, 0.3)
  renWin.SetSize(800, 600)
  iren.Initialize()
  ren.ResetCamera()
  renWin.Render()
  iren.Start()

def tessellate(f, tessagon_class, **kwargs):
  extra_args = {'function': f,
                'adaptor_class' : VtkAdaptor}
  tessagon = tessagon_class(**{**kwargs, **extra_args})

  poly_data = tessagon.create_mesh()
  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputData(poly_data)
  actor = vtk.vtkActor()
  actor.SetMapper(mapper)
  actor.GetProperty().SetColor(tomato)
  actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)
  actor.GetProperty().EdgeVisibilityOn()
  actor.SetPosition(kwargs['position'])

  return actor

def hex_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 45,
    'v_num': 3,
    'u_cyclic': True,
    'v_cyclic': False,
    'position': position
  }
  return tessellate(cylinder, HexTessagon, **options)

def tri_tessagon(position, **kwargs):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 36,
    'v_num': 12,
    'position': position
  }
  return tessellate(torus, TriTessagon, **{**kwargs, **options})

def rhombus_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 6,
    'v_twist': True,
    'position': position
  }
  return tessellate(klein, RhombusTessagon, **options)

def octo_tessagon(position):
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
  return tessellate(mobius, OctoTessagon, **options)

def hex_tri_tessagon(position):
  options = {
    'u_range': [-1.0, 1.0],
    'v_range': [-1.0, 1.0],
    'u_num': 15,
    'v_num': 10,
    'u_cyclic': False,
    'v_cyclic': False,
    'position': position
  }
  return tessellate(paraboloid, HexTriTessagon, **options)

def hex_square_tri_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 45,
    'v_num': 5,
    'position': position
  }
  return tessellate(torus, HexSquareTriTessagon, **options)

def square_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 15,
    'v_num': 4,
    'rot_factor': 2,
    'position': position
  }
  return tessellate(torus, SquareTessagon, **options)

def pythagorean_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 25,
    'v_num': 6,
    'position': position
  }
  return tessellate(torus, PythagoreanTessagon, **options)

def brick_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 15,
    'v_num': 3,
    'rot_factor': 3,
    'position': position
  }
  return tessellate(torus, BrickTessagon, **options)

def dodeca_tessagon(position):
  options = {
    'u_range': [-1.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 4,
    'v_num': 10,
    'u_cyclic': False,
    'v_cyclic': True,
    'position': position
  }
  return tessellate(one_sheet_hyperboloid, DodecaTessagon, **options)

def square_tri_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 20,
    'v_num': 4,
    'position': position
  }
  return tessellate(torus, SquareTriTessagon, **options)

def weave_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 8,
    'v_num': 6,
    'v_cyclic': False,
    'rot_factor': 1,
    'position': position
  }
  return tessellate(sphere, WeaveTessagon, **options)

def floret_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 5,
    'v_num': 2,
    'position': position
  }
  return tessellate(torus, FloretTessagon, **options)

def hex_big_tri_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 5,
    'v_num': 2,
    'position': position
  }
  return tessellate(torus, HexBigTriTessagon, **options)

def zig_zag_tessagon(position):
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 10,
    'v_num': 2,
    'rot_factor': 2,
    'position': position
  }
  return tessellate(torus, ZigZagTessagon, **options)

main()
