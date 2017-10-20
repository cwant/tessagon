from tessagon.core.value_blend import ValueBlend

class AbstractTile(ValueBlend):
  def __init__(self, tessagon, **kwargs):
    self.tessagon = tessagon
    self.f = tessagon.f

    # Verts/faces indexed with 'left', 'right', 'center'
    self.u_symmetric = False
    # Verts/faces indexed with 'bottom', 'middle', 'top'
    self.v_symmetric = False

    if 'u_symmetric' in kwargs:
      self.u_symmetric = kwargs['u_symmetric']
    if 'v_symmetric' in kwargs:
      self.u_symmetric = kwargs['u_symmetric']

    self.id = None
    # This is not necessary to any of the calculations, just
    # makes debugging easier
    if 'id' in kwargs:
      self.id = kwargs['id']

    # Corners is list of tuples [bottomleft, bottomright, topleft, topright]
    self.corners = None
    self.init_corners(**kwargs)

    self.neighbors = { 'top': None,
                       'bottom': None,
                       'left': None,
                       'right': None }

    self.twist = {
      'top': False,
      'bottom': False,
      'left': False,
      'right': False
    }

  def set_neighbors(self, **kwargs):
    if 'top' in kwargs:
      self.neighbors['top'] = kwargs['top']
    if 'bottom' in kwargs:
      self.neighbors['bottom'] = kwargs['bottom']
    if 'left' in kwargs:
      self.neighbors['left'] = kwargs['left']
    if 'right' in kwargs:
      self.neighbors['right'] = kwargs['right']

  def get_nested_list_value(self, nested_list, index_path):
    if not isinstance(index_path, list):
      return nested_list[index_path]
    value = nested_list
    for index in index_path:
      value = value[index]
    return value

  def set_nested_list_value(self, nested_list, index_path, value):
    if not isinstance(index_path, list):
      nested_list[index_path] = value
      return
    reference = nested_list
    for index in index_path[0:-1]:
      reference = reference[index]
    reference[index_path[-1]] = value

  def neighbor_path(self, neighbor_keys):
    # Note: it is assumed that len(neighbor_keys) <= 2
    if len(neighbor_keys) < 2: return neighbor_keys
    if self.should_twist_u(neighbor_keys):
      if (neighbor_keys[0] in ['top', 'bottom']):
        return [neighbor_keys[1], neighbor_keys[0]]
    elif self.should_twist_v(neighbor_keys):
      if (neighbor_keys[0] in ['left', 'right']):
        return [neighbor_keys[1], neighbor_keys[0]]
    return neighbor_keys

  def get_neighbor_tile(self, neighbor_keys):
    tile = self
    for key in self.neighbor_path(neighbor_keys):
      if not tile.neighbors[key]:
        return None
      tile = tile.neighbors[key]
    return tile

  def swap_value(self, index_path, val1, val2):
    if isinstance(index_path, list):
      return [self.swap_value(u, val1, val2) for u in index_path]
    if index_path == val1: return val2
    if index_path == val2: return val1
    return index_path

  def u_flip(self, index_path):
    if not self.u_symmetric: return index_path
    return self.swap_value(index_path, 'left', 'right')

  def v_flip(self, index_path):
    if not self.v_symmetric: return index_path
    return self.swap_value(index_path, 'bottom', 'top')

  def v_index(self, index_path):
    if ('bottom' in index_path): return 'bottom'
    if ('top' in index_path): return 'top'
    raise ValueError("no v_index found in %s" % (index_path))

  def u_index(self, index_path):
    if ('left' in index_path): return 'left'
    if ('right' in index_path): return 'right'
    raise ValueError("no u_index found in %s" % (index_path))

  def should_twist_u(self, neighbor_keys):
    for twist in ['top', 'bottom']:
      if self.twist[twist] and twist in neighbor_keys: return True
    return False

  def should_twist_v(self, neighbor_keys):
    for twist in ['left', 'right']:
      if self.twist[twist] and twist in neighbor_keys: return True
    return False

  def inspect(self, **kwargs):
    # For debugging topology
    if not self.id: return
    prefix = 'Tile'
    if 'tile_number' in kwargs:
      prefix += " #%s" % (kwargs['tile_number'])
    print("%s (%s):" % (prefix, self.__class__.__name__))
    print("  - self:      %s" % (self.id))
    print('  - neighbors:')
    for key in ['top', 'left', 'right', 'bottom']:
      if self.neighbors[key]:
        tile = self.neighbors[key]
        if tile.id:
          print("    - %s" % (self.neighbor_str(key)))
    print("  - corners: (%2.4f, %2.4f)  (%2.4f, %2.4f)" %
          tuple(self.corners[2] + self.corners[3]))
    print("             (%2.4f, %2.4f)  (%2.4f, %2.4f)" %
          tuple(self.corners[0] + self.corners[1]))
    print("  - twist:", self.twist)
    print('')

  def neighbor_str(self, key):
    tile = self.neighbors[key]
    if tile:
      return "%-9s%s" % ("%s:" % (key), tile.id)
    return "%s: None" % (key)
