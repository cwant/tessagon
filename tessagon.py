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

    if 'adaptor_class' in kwargs:
      adaptor_class = kwargs['adaptor_class']
      self.mesh_adaptor = adaptor_class(**kwargs)
    else:
      raise ValueError('Must provide a mesh adaptor class')

    self.tiles = None
    self.face_types = {}
    self.vert_types = {}

  def create_mesh(self):
    self.initialize_tiles()

    self.mesh_adaptor.create_empty_mesh()

    self.calculate_verts()
    self.calculate_faces()

    self.mesh_adaptor.finish_mesh()

    if self.post_process:
      self.post_process()

    return self.mesh_adaptor.get_mesh()

  def initialize_tiles(self):
    self.tiles = self.tile_generator.create_tiles()
        
  def calculate_verts(self):
    for tile in self.tiles:
      tile.calculate_verts()

  def calculate_faces(self):
    for tile in self.tiles:
      tile.calculate_faces()

  def inspect(self):
    print("\n=== %s ===\n" % (self.__class__.__name__))
    for i in range(len(self.tiles)):
      self.tiles[i].inspect(tile_number=i)
