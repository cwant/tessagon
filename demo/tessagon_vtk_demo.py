import os, sys
import vtk
from vtk.util.colors import tomato

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.adaptors.vtk_adaptor import VtkAdaptor

from tessagon.types.hex_tessagon import HexTessagon
from tessagon.types.tri_tessagon import TriTessagon
from tessagon.types.octo_tessagon import OctoTessagon
from tessagon.types.rhombus_tessagon import RhombusTessagon
from tessagon.types.hex_tri_tessagon import HexTriTessagon
from tessagon.types.hex_square_tri_tessagon import HexSquareTriTessagon
from tessagon.types.square_tessagon import SquareTessagon
from tessagon.types.pythagorean_tessagon import PythagoreanTessagon
from tessagon.types.brick_tessagon import BrickTessagon
from tessagon.types.dodeca_tessagon import DodecaTessagon

from tessagon.misc.shapes import *

def main():
  ren = vtk.vtkRenderer()
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(ren)
  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)

  ren.AddActor(hex_tessagon())
  ren.AddActor(tri_tessagon())
  ren.AddActor(rhombus_tessagon())
  ren.AddActor(octo_tessagon())
  ren.AddActor(hex_tri_tessagon())
  ren.AddActor(hex_square_tri_tessagon())
  ren.AddActor(square_tessagon())
  ren.AddActor(pythagorean_tessagon())
  ren.AddActor(brick_tessagon())
  ren.AddActor(dodeca_tessagon())

  ren.SetBackground(0.3, 0.3, 0.3)
  renWin.SetSize(800, 600)
  iren.Initialize()
  ren.ResetCamera()
  renWin.Render()
  iren.Start()

def tessellate(f, tessagon_class, **kwargs):
  extra_args = {'adaptor_class' : VtkAdaptor}
  tessagon = tessagon_class(f, **{**kwargs, **extra_args})

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

def hex_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 5,
    'u_cyclic': True,
    'v_cyclic': False,
    'position': [0, 0, 0]
  }
  return tessellate(cylinder, HexTessagon, **options)

def tri_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 35,
    'v_num': 12,
    'position': [0, 15, 0]
  }
  return tessellate(torus, TriTessagon, **options)

def rhombus_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 6,
    'v_twist': True,
    'position': [0, 30, 0]
  }
  return tessellate(klein, RhombusTessagon, **options)

def octo_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 4,
    'v_num': 40,
    'v_cyclic': True,
    'u_cyclic': False,
    'u_twist': True,
    'position': [0, 45, 0]
  }
  return tessellate(mobius, OctoTessagon, **options)

def hex_tri_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 6,
    'position': [0, 60, 0]
  }
  return tessellate(torus, HexTriTessagon, **options)

def hex_square_tri_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 45,
    'v_num': 5,
    'position': [15, 0, 0]
  }
  return tessellate(torus, HexSquareTriTessagon, **options)

def square_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 15,
    'v_num': 4,
    'rot_factor': 2,
    'position': [15, 15, 0]
  }
  return tessellate(torus, SquareTessagon, **options)

def pythagorean_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 25,
    'v_num': 6,
    'position': [15, 30, 0]
  }
  return tessellate(torus, PythagoreanTessagon, **options)

def brick_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 15,
    'v_num': 3,
    'rot_factor': 3,
    'position': [15, 45, 0]
  }
  return tessellate(torus, BrickTessagon, **options)

def dodeca_tessagon():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 25,
    'v_num': 3,
    'position': [15, 60, 0]
  }
  return tessellate(torus, DodecaTessagon, **options)

main()
