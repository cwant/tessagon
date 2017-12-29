import os, sys
import vtk
from vtk.util.colors import tomato

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.adaptors.vtk_adaptor import VtkAdaptor
from tessagon_common_demo import TessagonCommonDemo

class VtkDemo(TessagonCommonDemo):
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

VtkDemo().main()
