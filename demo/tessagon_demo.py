import bpy
from importlib import reload
import tessagon
reload(tessagon)

from hex_tessagon import HexTessagon
from tri_tessagon import TriTessagon
from octo_tessagon import OctoTessagon
from rhombus_tessagon import RhombusTessagon
from hex_tri_tessagon import HexTriTessagon
from hex_square_tri_tessagon import HexSquareTriTessagon
from square_tessagon import SquareTessagon
from pythagorean_tessagon import PythagoreanTessagon

from shapes import torus, other_torus, cylinder, mobius, plane

# Optional, for the wire_skin demos
# https://github.com/cwant/wire_skin
is_wire_skin_loaded = False
try:
  import wire_skin
  reload(wire_skin)
  from wire_skin import WireSkin
  is_wire_skin_loaded = True
except:
  print('Could not load wire_skin, some demoes skipped')

def main():
  layer10()
  
def main2():
  # A bunch of layers have demos

  # Hexagon Torii
  layer1()
  
  # Triangle Torii
  layer2()
  
  # RhombusTessagon
  layer3()

  # OctoTessagon
  layer4()

  # HexTriTessagon
  layer5()

  # HexSquareTriTessagon
  layer6()

  # SquareTessagon
  layer7()

  # PythagoreanTessagon
  layer8()

  # Rotated Tiles
  layer11()
  
  if is_wire_skin_loaded:
    # WireSkin demo, hexagons
    layer16()

    # WireSkin demo, triangles and booleans
    layer17()
    pass

  # Non-cyclic Torus
  layer18()

  # Mobius Tessagon
  layer19()

def tessellate(out_name, f, tessagon_class, **kwargs):
  output_object = bpy.data.objects[out_name]
  me = output_object.data
  output_materials = me.materials

  tessagon = tessagon_class(f, **kwargs)

  bm = tessagon.create_bmesh()
  bm.to_mesh(me)
  #for material in output_materials:
  #  me.materials.append(material)
  output_object.data = me
  me.update()
  
def layer1():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 35,
    'v_num': 5
  }
  tessellate("HexTessagon1", torus, HexTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 8,
    'v_num': 20
  }
  tessellate("HexTessagon2", other_torus, HexTessagon, **options)

def layer2():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 35,
    'v_num': 12
  }
  tessellate("TriTessagon1", torus, TriTessagon, **options)

  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 6,
    'v_num': 35
  }
  tessellate("TriTessagon2", other_torus, TriTessagon, **options)

def layer3():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 30,
    'v_num': 4
  }
  tessellate("RhombusTessagon1", torus, RhombusTessagon, **options)

def layer4():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 8
  }
  tessellate("OctoTessagon1", torus, OctoTessagon, **options)

def layer5():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 6
  }
  tessellate("HexTriTessagon1", torus, HexTriTessagon, **options)

def layer6():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 45,
    'v_num': 5
  }
  tessellate("HexSquareTriTessagon1", torus, HexSquareTriTessagon, **options)

def layer7():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 60,
    'v_num': 16
  }
  tessellate("SquareTessagon1", torus, SquareTessagon, **options)

def layer8():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 25,
    'v_num': 6
  }
  tessellate("PythagoreanTessagon1", torus, PythagoreanTessagon, **options)

def layer10():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 2,
    'v_num': 2,
    'u_cyclic': False,
    'v_cyclic': False,
    'rot_factor': 2
  }
  tessellate("Test", plane, SquareTessagon, **options)

def layer11():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 10,
    'v_num': 2,
    'rot_factor': 5
  }
  tessellate("HexTessagonRot", torus, SquareTessagon, **options)

def wire_to_skin(in_name, out_name, **kwargs):
  input_object = bpy.data.objects[in_name]
  output_object = bpy.data.objects[out_name]
  output_materials = output_object.data.materials

  wire_skin = \
    WireSkin(input_object.data, **kwargs)

  me = wire_skin.create_mesh()
  for material in output_materials:
    me.materials.append(material)
  output_object.data = me

def layer18():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 40,
    'v_num': 5,
    'u_cyclic': True,
    'v_cyclic': False
  }
  tessellate("Tessagon7", cylinder, HexTessagon, **options)

def layer19():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 5,
    'v_num': 40,
    'u_cyclic': False,
    #'u_twist': True,
    'v_cyclic': False
  }
  tessellate("Tessagon8", mobius, HexTessagon, **options)

def layer16():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 8,
    'v_num': 20
  }
  tessellate("Tessagon5", other_torus, HexTessagon, **options)

  options = {
    'width': 0.1,
    'height': 0.4,
    'inside_radius': 0.1,
    'outside_radius': 0.2,
    'dist': 0.1,
    'crease': 1.0
  }
  wire_to_skin("Tessagon5", "WireSkin5", **options)

def layer17():
  options = {
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 35,
    'v_num': 12
  }
  tessellate("Tessagon6", torus, TriTessagon, **options)

  options = {
    'width': 0.2,
    'height': 0.2,
    'inside_radius': 0.3,
    'outside_radius': 0.3,
    'dist': 0.4,
    'proportional_scale': True
  }
  wire_to_skin("Tessagon6", "WireSkin6", **options)
