from value_blend import ValueBlend

class AbstractTile(ValueBlend):
  def __init__(self, tessagon, **kwargs):
    self.tessagon = tessagon
    self.f = tessagon.f
    self.mesh_adaptor = tessagon.mesh_adaptor
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

  def get_neighbor_path(self, neighbor_keys):
    tile = self
    for key in neighbor_keys:
      if not tile.neighbors[key]:
        return None
      tile = tile.neighbors[key]
    return tile

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
    print('')

  def neighbor_str(self, key):
    tile = self.neighbors[key]
    if tile:
      return "%-9s%s" % ("%s:" % (key), tile.id)
    return "%s: None" % (key)
