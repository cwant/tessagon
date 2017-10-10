import bmesh

from importlib import reload
import rotate_tile_generator
reload(rotate_tile_generator)

from grid_tile_generator import GridTileGenerator
from rotate_tile_generator import RotateTileGenerator

class Tessagon:
  def __init__(self, f, **kwargs):
    self.f = f
    self.tile_class = self.init_tile_class()

    if 'tile_generator' in kwargs:
      self.tile_generator = kwargs['tile_generator'](self, **kwargs)
    elif 'rot_factor' in kwargs:
      self.tile_generator = RotateTileGenerator(self, **kwargs)
    else:
      self.tile_generator = GridTileGenerator(self, **kwargs)

    # Optional post processing function
    self.post_process = None
    if 'post_process' in kwargs:
      self.post_process = kwargs['post_process']

    self.bm = bmesh.new()
    self.tiles = None
    self.face_types = {}
    self.vert_types = {}

  def create_bmesh(self):
    self.initialize_tiles()
    self.calculate_verts()
    self.calculate_faces()
    if self.post_process:
      self.post_process()
    return self.bm

  def initialize_tiles(self):
    self.tiles = self.tile_generator.create_tiles()
        
  def calculate_verts(self):
    for tile in self.tiles:
      tile.calculate_verts()

  def calculate_faces(self):
    for tile in self.tiles:
      tile.calculate_faces()
    bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)

  def inspect(self):
    print("\n=== %s ===\n" % (self.__class__.__name__))
    for i in range(len(self.tiles)):
      self.tiles[i].inspect(tile_number=i)
