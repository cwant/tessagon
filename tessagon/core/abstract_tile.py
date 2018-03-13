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
            self.v_symmetric = kwargs['v_symmetric']

        self.id = None
        # This is not necessary to any of the calculations, just
        # makes debugging easier
        if 'id' in kwargs:
            self.id = kwargs['id']

        # This is an identifier that is set by the generator (a tuple)
        # Really this should be merged with the id thingy above
        self.fingerprint = kwargs.get('fingerprint') or None

        # Corners is list of tuples:
        #   [bottomleft, bottomright, topleft, topright]
        self.corners = None
        self._init_corners(**kwargs)

        self.neighbors = {
            'top': None,
            'bottom': None,
            'left': None,
            'right': None
        }

        # Are the neighbors ordered backwards?
        # e.g., a tile with twist['right'] set to True:
        #  self tile: right edge has v=0 at the bottom and v=1 at the top
        #  right neighbor: left edge has v=1 at the bottom and v=0 at the top
        #  (the right tile has twist['left'] true
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

    def get_neighbor_tile(self, neighbor_keys):
        tile = self
        for key in self._neighbor_path(neighbor_keys):
            if not tile.neighbors[key]:
                return None
            tile = tile.neighbors[key]
        return tile

    def inspect(self, **kwargs):
        # For debugging topology
        if not self.id:
            return
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
                    print("    - %s" % (self._neighbor_str(key)))
        print("  - corners: (%2.4f, %2.4f)  (%2.4f, %2.4f)" %
              tuple(self.corners[2] + self.corners[3]))
        print("             (%2.4f, %2.4f)  (%2.4f, %2.4f)" %
              tuple(self.corners[0] + self.corners[1]))
        print("  - twist:", self.twist)
        if self.fingerprint:
            print("  - fingerprint:", self.fingerprint)
        print('')

    # Below are protected

    # A couple of abstract methods that will be useful for finding
    # and setting the vertices and faces on a tile
    def _get_nested_list_value(self, nested_list, index_keys):
        if not isinstance(index_keys, list):
            return nested_list[index_keys]
        value = nested_list
        for index in index_keys:
            value = value[index]
        return value

    def _set_nested_list_value(self, nested_list, index_keys, value):
        if not isinstance(index_keys, list):
            nested_list[index_keys] = value
            return
        reference = nested_list
        for index in index_keys[0:-1]:
            reference = reference[index]
        reference[index_keys[-1]] = value

    def _neighbor_path(self, neighbor_keys):
        # Note: it is assumed that len(neighbor_keys) in [1, 2]
        # if len(neighbor_keys) == 1, the neighbor meets on an edge
        # if len(neighbor_keys) == 2, the neighbor meets at a corner,
        #     and are diagonal for each other, e.g., ['left', 'top']
        # If the boundary is twisted, need to be careful because
        # left and become right, or top can become bottom on the
        # other side of the twisted boundary: try to traverse the
        # non-twisted boundary first to make the math easier
        if len(neighbor_keys) < 2:
            return neighbor_keys
        if self._should_twist_u(neighbor_keys):
            if (neighbor_keys[0] in ['top', 'bottom']):
                return [neighbor_keys[1], neighbor_keys[0]]
        elif self._should_twist_v(neighbor_keys):
            if (neighbor_keys[0] in ['left', 'right']):
                return [neighbor_keys[1], neighbor_keys[0]]
        return neighbor_keys

    def _index_path(self, index_keys, neighbor_keys):
        path = index_keys
        if self._should_twist_u(neighbor_keys):
            path = self._u_flip(path)
        if self._should_twist_v(neighbor_keys):
            path = self._v_flip(path)
        return path

    def _swap_value(self, index_keys, val1, val2):
        # abstract function to swap two values in a list
        # e.g., 'left' and 'right' in u_flip below
        if isinstance(index_keys, list):
            return [self._swap_value(u, val1, val2) for u in index_keys]
        if index_keys == val1:
            return val2
        if index_keys == val2:
            return val1
        return index_keys

    def _u_flip(self, index_keys):
        # swap each left with right (and vice versa) in list
        if not self.u_symmetric:
            return index_keys
        return self._swap_value(index_keys, 'left', 'right')

    def _v_flip(self, index_keys):
        # swap each top with bottom (and vice versa) in list
        if not self.v_symmetric:
            return index_keys
        return self._swap_value(index_keys, 'bottom', 'top')

    def _v_index(self, index_keys):
        # find either 'top' or 'bottom' in the list
        if ('bottom' in index_keys):
            return 'bottom'
        if ('top' in index_keys):
            return 'top'
        raise ValueError("no v_index found in %s" % (index_keys))

    def _u_index(self, index_keys):
        # find either 'right' or 'left' in the list
        if ('left' in index_keys):
            return 'left'
        if ('right' in index_keys):
            return 'right'
        raise ValueError("no u_index found in %s" % (index_keys))

    def _should_twist_u(self, neighbor_keys):
        # e.g., twist['bottom'] is True, and neigbor_keys has 'bottom' in it
        for twist in ['top', 'bottom']:
            if self.twist[twist] and twist in neighbor_keys:
                return True
        return False

    def _should_twist_v(self, neighbor_keys):
        # e.g., twist['left'] is True, and neigbor_keys has 'left' in it
        for twist in ['left', 'right']:
            if self.twist[twist] and twist in neighbor_keys:
                return True
        return False

    def _neighbor_str(self, key):
        tile = self.neighbors[key]
        if tile:
            return "%-9s%s" % ("%s:" % (key), tile.id)
        return "%s: None" % (key)
