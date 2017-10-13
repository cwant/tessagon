from tessagon.core.tile_generator import TileGenerator
from tessagon.core.abstract_tile import AbstractTile

class RotateTileGenerator(TileGenerator):
  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)

    self.rot_factor = kwargs['rot_factor']

    # Rot tiles are not tiles, they are a collection of tiles.
    # They generate interior tiles ((rot_index - 1)^2 of them) and #
    # up to 2 * rot_index boundary tiles that are shared with neighbors
    # (if they exist).
    # Maximum tiles generated per rot_tile is rot_index^2 + 1 tiles
    # With this in mind, you'll want to set u_num and v_num lower than
    # you would with the grid tile generator
    self.id_prefix = 'rot_tiles'
    self.rot_tiles = None

  def create_tiles(self):
    self.rot_tiles = self.initialize_tiles(RotTile,
                                           rot_factor=self.rot_factor)
    self.initialize_neighbors(self.rot_tiles)
    self.initialize_interiors()
    self.initialize_boundaries()
    self.calculate_boundary_neighbors()
    return self.calculate_rot_tiles()

  def initialize_interiors(self):
    for rot_tile in [j for i in self.rot_tiles for j in i]:
      rot_tile.initialize_interior()

  def initialize_boundaries(self):
    for rot_tile in [j for i in self.rot_tiles for j in i]:
      rot_tile.initialize_boundary()

  def calculate_boundary_neighbors(self):
    for rot_tile in [j for i in self.rot_tiles for j in i]:
      rot_tile.calculate_boundary_neighbors()

  def calculate_rot_tiles(self):
    tiles = []
    for rot_tile in [j for i in self.rot_tiles for j in i]:
      tiles += rot_tile.create_tiles()
    return tiles

# This is both a kind of tile and a tile generator
# It hurts my brain thinking about this stuff
class RotTile(AbstractTile):
  def __init__(self, tessagon, **kwargs):
    super().__init__(tessagon, **kwargs)
    self.n = kwargs['rot_factor']

    self.interior = None
    self.interior_corners = None
    self.boundary = { 'left': None,
                      'right': None,
                      'top': None,
                      'bottom': None }
    # We'll use these a lot
    n2_p1 = self.n**2 + 1.0
    self.c1 = 1.0 / n2_p1
    self.c2 = self.n / n2_p1
    self.c3 = 1.0 - self.c2
    self.c4 = 1.0 - self.c1

    self.tiles = []

  def initialize_interior(self):
    self.interior_corners = [ self.blend(self.c2, self.c1),
                              self.blend(self.c4, self.c2),
                              self.blend(self.c1, self.c3),
                              self.blend(self.c3, self.c4) ]
    if self.n < 2:
      return
    generator = TileGenerator(self.tessagon,
                              corners=self.interior_corners,
                              u_num=self.n-1, v_num=self.n-1,
                              u_cyclic=False, v_cyclic=False,
                              id_prefix=self.id + '.interior')

    self.interior = generator.initialize_tiles(self.tessagon.tile_class)
    generator.initialize_neighbors(self.interior)
    self.tiles += self.flatten_list(self.interior)

  def create_tiles(self):
    return self.tiles
    
  def initialize_boundary(self):
    prefix_base = self.id
    self.initialize_left_boundary(self.id + ".boundary['left']")
    self.initialize_right_boundary(self.id + ".boundary['right']")
    self.initialize_top_boundary(self.id + ".boundary['top']")
    self.initialize_bottom_boundary(self.id + ".boundary['bottom']")

  def initialize_left_boundary(self, id_prefix):
    if not self.boundary['left']:
      tile = self.get_neighbor_path(['left'])
      if tile:
        corners = [ self.blend(0, 0),
                    self.blend(self.c2, self.c1),
                    self.blend(self.c3 - 1.0, self.c4),
                    self.blend(0, 1) ]
        generator = TileGenerator(self.tessagon,
                                  corners=corners,
                                  u_num=1, v_num=self.n,
                                  u_cyclic=False, v_cyclic=False,
                                  id_prefix=id_prefix)
        tiles = generator.initialize_tiles(self.tessagon.tile_class)
        generator.initialize_neighbors(tiles)

        self.boundary['left'] = tiles
        tile.boundary['right'] = tiles
        self.tiles += self.flatten_list(tiles)

  def initialize_bottom_boundary(self, id_prefix):
    if not self.boundary['bottom']:
      tile = self.get_neighbor_path(['bottom'])
      if tile:
        corners = [ self.blend(self.c1, self.c3 - 1.0),
                    self.blend(1, 0),
                    self.blend(0, 0),
                    self.blend(self.c4, self.c2) ]
        generator = TileGenerator(self.tessagon,
                                  corners=corners,
                                  u_num=self.n, v_num=1,
                                  u_cyclic=False, v_cyclic=False,
                                  id_prefix=id_prefix)
        tiles = generator.initialize_tiles(self.tessagon.tile_class)
        generator.initialize_neighbors(tiles)

        self.boundary['bottom'] = tiles
        tile.boundary['top'] = tiles
        self.tiles += self.flatten_list(tiles)

  def initialize_right_boundary(self, id_prefix):
    if not self.boundary['right']:
      tile = self.get_neighbor_path(['right'])
      if tile:
        tile.initialize_left_boundary(id_prefix)

  def initialize_top_boundary(self, id_prefix):
    if not self.boundary['top']:
      tile = self.get_neighbor_path(['top'])
      if tile:
        tile.initialize_bottom_boundary(id_prefix)

  def calculate_boundary_neighbors(self):
    self.calculate_left_boundary_neighbors()
    self.calculate_right_boundary_neighbors()
    self.calculate_top_boundary_neighbors()
    self.calculate_bottom_boundary_neighbors()

  def calculate_left_boundary_neighbors(self):
    if self.boundary['left']:
      for i in range(self.n - 1):
        boundary_tile = self.boundary['left'][0][i]
        other_tile = None
        if self.n > 1:
          other_tile = self.interior[0][i]
        if other_tile:
          boundary_tile.neighbors['right'] = other_tile
          other_tile.neighbors['left'] = boundary_tile
      if self.boundary['top']:
        boundary_tile = self.boundary['left'][0][self.n-1]
        other_tile = self.boundary['top'][0][0]
        boundary_tile.neighbors['right'] = other_tile
        other_tile.neighbors['left'] = boundary_tile

  def calculate_bottom_boundary_neighbors(self):
    if self.boundary['bottom']:
      for i in range(self.n - 1):
        boundary_tile = self.boundary['bottom'][i+1][0]
        other_tile = None
        if self.n > 1:
          other_tile = self.interior[i][0]
        if other_tile:
          boundary_tile.neighbors['top'] = other_tile
          other_tile.neighbors['bottom'] = boundary_tile
      if self.boundary['left']:
        boundary_tile = self.boundary['bottom'][0][0]
        other_tile = self.boundary['left'][0][0]
        boundary_tile.neighbors['top'] = other_tile
        other_tile.neighbors['bottom'] = boundary_tile
        
  def calculate_right_boundary_neighbors(self):
    if self.boundary['right']:
      for i in range(self.n - 1):
        boundary_tile = self.boundary['right'][0][i+1]
        other_tile = None
        if self.n > 1:
          other_tile = self.interior[self.n-2][i]
        if other_tile:
          boundary_tile.neighbors['left'] = other_tile
          other_tile.neighbors['right'] = boundary_tile
      if self.boundary['bottom']:
        boundary_tile = self.boundary['right'][0][0]
        other_tile = self.boundary['bottom'][self.n-1][0]
        boundary_tile.neighbors['left'] = other_tile
        other_tile.neighbors['right'] = boundary_tile

  def calculate_top_boundary_neighbors(self):
    if self.boundary['top']:
      for i in range(self.n - 1):
        boundary_tile = self.boundary['top'][i][0]
        other_tile = None
        if self.n > 1:
          other_tile = self.interior[i][self.n-2]
        if other_tile:
          boundary_tile.neighbors['bottom'] = other_tile
          other_tile.neighbors['top'] = boundary_tile
      if self.boundary['right']:
        boundary_tile = self.boundary['top'][self.n-1][0]
        other_tile = self.boundary['right'][0][self.n-1]
        boundary_tile.neighbors['bottom'] = other_tile
        other_tile.neighbors['top'] = boundary_tile

  def flatten_list(self, l):
    return [item for sublist in l for item in sublist]
