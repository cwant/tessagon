from value_blend import ValueBlend

class TileGenerator(ValueBlend):
  def __init__(self, tessagon, **kwargs):
    self.tessagon = tessagon

    # Corners is list of tuples [topleft, topright, bottomleft, bottomright]
    self.corners = None
    self.init_corners(**kwargs)

    self.u_num = self.v_num = None
    self.u_cyclic = True
    self.v_cyclic = True
    self.u_twist = False
    self.v_twist = False

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

  def initialize_tiles(self, tile_class, **kwargs):
    tiles = [[None for i in range(self.v_num)] for j in range(self.u_num)]

    for u in range(self.u_num):
      u_ratio0 = float(u) / self.u_num
      u_ratio1 = float(u + 1) / self.u_num
      for v in range(self.v_num):
        v_ratio0 = float(v) / self.v_num
        v_ratio1 = float(v + 1) / self.v_num
        corners_arg = { 'corners': [self.blend(u_ratio0, v_ratio0),
                                    self.blend(u_ratio1, v_ratio0),
                                    self.blend(u_ratio0, v_ratio1),
                                    self.blend(u_ratio1, v_ratio1)] }
        tiles[u][v] = self.tessagon.tile_class(self.tessagon,
                                               **{**kwargs, **corners_arg})
    return tiles

  def initialize_neighbors(self, tiles, **kwargs):
    for u in range(self.u_num):
      u_prev = (u - 1) % self.u_num
      u_next = (u + 1) % self.u_num
      for v in range(self.v_num):
        v_prev = (v - 1) % self.v_num
        v_next = (v + 1) % self.v_num
        tile = tiles[u][v]
        if not self.u_cyclic and u == 0:
          left = None
        else:
          left = tiles[u_prev][v]
        if not self.v_cyclic and v == 0:
          top = None
        else:
          top = tiles[u][v_prev]
        if not self.u_cyclic and u == self.u_num - 1:
          right = None
        else:
          if self.u_twist and u == self.u_num - 1:
            right = tiles[u_next][0]
          else:
            right = tiles[u_next][v]
        if not self.v_cyclic and v == self.v_num - 1:
          bottom = None
        else:
          if self.v_twist and v == self.v_num - 1:
            bottom = tiles[self.u_num - u - 1][v_next]
          else:
            bottom = tiles[u][v_next]
        tile.set_neighbors(left=left, right=right, top=top, bottom=bottom)
