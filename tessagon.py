import bpy, bmesh
from math import sqrt, sin, cos, atan2, pi
from mathutils import Matrix, Vector

from tri_tessagon import TriTessagon
from hex_tessagon import HexTessagon
from octo_tessagon import OctoTessagon
from rhombus_tessagon import RhombusTessagon

class Tessagon:
  def __init__(self, f, **kwargs):
    self.f = f
    self.tile_class = self.init_tile_class()
    self.u_range = self.v_range = None
    self.u_num = self.v_num = None
    self.bm = None
    self.u_cyclic = True
    self.v_cyclic = True
    self.u_twist = False
    self.v_twist = False
    if 'u_range' in kwargs:
      self.u_range = kwargs['u_range']
    if 'v_range' in kwargs:
      self.v_range = kwargs['v_range']
    if not self.u_range or not self.v_range:
      raise ValueError("Make sure u_range and v_range intervals are set")
    if 'u_num' in kwargs:
      self.u_num = kwargs['u_num']
    if 'v_num' in kwargs:
      self.v_num = kwargs['v_num']
    if not self.u_num or not self.v_num:
      raise ValueError("Make sure u_num and v_num intervals are set")
    if 'u_cyclic' in kwargs:
      self.u_cyclic = kwargs['u_cyclic']
    if 'v_cyclic' in kwargs:
      self.v_cyclic = kwargs['v_cyclic']
    if 'u_twist' in kwargs:
      self.u_twist = kwargs['u_twist']
    if 'v_twist' in kwargs:
      self.v_twist = kwargs['v_twist']

    self.tiles = [[None for i in range(self.v_num)] for j in range(self.u_num)]
    self.bm = bmesh.new()

  def create_bmesh(self):
    self.initialize_tiles()
    self.initialize_neighbors()
    self.calculate_verts()
    self.calculate_faces()
    return self.bm

  def initialize_tiles(self):
    for u in range(self.u_num):
      u_ratio0 = float(u) / self.u_num
      u_ratio1 = float(u + 1) / self.u_num
      u0 = self.u_range[0] * (1.0 - u_ratio0) + self.u_range[1] * u_ratio0
      u1 = self.u_range[0] * (1.0 - u_ratio1) + self.u_range[1] * u_ratio1
      for v in range(self.v_num):
        v_ratio0 = float(v) / self.v_num
        v_ratio1 = float(v + 1) / self.v_num
        v0 = self.v_range[0] * (1.0 - v_ratio0) + self.v_range[1] * v_ratio0
        v1 = self.v_range[0] * (1.0 - v_ratio1) + self.v_range[1] * v_ratio1
        self.tiles[u][v] = self.tile_class(self.f, u_range=[u0, u1], v_range=[v0, v1],
                                           bm=self.bm)

  def initialize_neighbors(self):
    for u in range(self.u_num):
      u_prev = (u - 1) % self.u_num
      u_next = (u + 1) % self.u_num
      for v in range(self.v_num):
        v_prev = (v - 1) % self.v_num
        v_next = (v + 1) % self.v_num
        tile = self.tiles[u][v]
        if not self.u_cyclic and u == 0:
          left = None
        else:
          left = self.tiles[u_prev][v]
        if not self.v_cyclic and v == 0:
          top = None
        else:
          top = self.tiles[u][v_prev]
        if not self.u_cyclic and u == self.u_num - 1:
          right = None
        else:
          if self.u_twist and u == self.u_num - 1:
            right = self.tiles[u_next][0]
          else:
            right = self.tiles[u_next][v]
        if not self.v_cyclic and v == self.v_num - 1:
          bottom = None
        else:
          if self.v_twist and v == self.v_num - 1:
            bottom = self.tiles[self.u_num - u - 1][v_next]
          else:
            bottom = self.tiles[u][v_next]
        tile.set_neighbors(left=left, right=right, top=top, bottom=bottom)
        
  def calculate_verts(self):
    for u in range(self.u_num):
      for v in range(self.v_num):
        self.tiles[u][v].calculate_verts()

  def calculate_faces(self):
    for u in range(self.u_num):
      for v in range(self.v_num):
        self.tiles[u][v].calculate_faces()
    bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
