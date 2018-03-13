from tessagon.core.value_blend import ValueBlend


class TileGenerator(ValueBlend):
    # This is intended to be an abstract class to generate tiles,
    # but it's quite tied to a grid structure, so it might make
    # sense to merge with GridTileGenerator
    def __init__(self, tessagon, **kwargs):
        self.tessagon = tessagon

        # Corners is list of tuples:
        #   [topleft, topright, bottomleft, bottomright]
        self.corners = None
        self._init_corners(**kwargs)

        self.u_num = self.v_num = None
        self.u_cyclic = True
        self.v_cyclic = True
        self.u_twist = False
        self.v_twist = False
        self.u_phase = 0.0
        self.v_phase = 0.0
        self.u_shear = 0.0
        self.v_shear = 0.0

        if 'u_num' in kwargs:
            self.u_num = kwargs['u_num']
        if 'v_num' in kwargs:
            self.v_num = kwargs['v_num']
        if not self.u_num or not self.v_num:
            raise ValueError("Make sure u_num and v_num intervals are set")

        if 'u_cyclic' in kwargs:
            self.u_cyclic = kwargs['u_cyclic']
        if 'u_phase' in kwargs and kwargs['u_phase']:
            self.u_phase = kwargs['u_phase']
        if 'u_shear' in kwargs and kwargs['u_shear']:
            self.u_shear = kwargs['u_shear']
        if 'v_twist' in kwargs:
            self.v_twist = kwargs['v_twist']

        if 'v_cyclic' in kwargs:
            self.v_cyclic = kwargs['v_cyclic']
        if 'v_phase' in kwargs and kwargs['v_phase']:
            self.v_phase = kwargs['v_phase']
        if 'v_shear' in kwargs and kwargs['v_shear']:
            self.v_shear = kwargs['v_shear']
        if 'u_twist' in kwargs:
            self.u_twist = kwargs['u_twist']

        # Note: id_prefix is not used for calculation, just debugging
        self.id_prefix = self.tessagon.__class__.__name__
        if 'id_prefix' in kwargs:
            self.id_prefix = kwargs['id_prefix']
        self.fingerprint_offset = kwargs.get('fingerprint_offset') or None

        self.color_pattern = kwargs.get('color_pattern') or None

    def initialize_tiles(self, tile_class, **kwargs):
        tiles = [[None for i in range(self.v_num)] for j in range(self.u_num)]

        for u in range(self.u_num):
            u_ratio0 = float(u) / self.u_num
            u_ratio1 = float(u + 1) / self.u_num
            v_shear0 = u * self.v_shear
            v_shear1 = (u + 1) * self.v_shear
            for v in range(self.v_num):
                v_ratio0 = float(v) / self.v_num
                v_ratio1 = float(v + 1) / self.v_num
                u_shear0 = v * self.u_shear
                u_shear1 = (v + 1) * self.u_shear
                corners = [self.blend(u_ratio0 + u_shear0 + self.u_phase,
                                      v_ratio0 + v_shear0 + self.v_phase),
                           self.blend(u_ratio1 + u_shear0 + self.u_phase,
                                      v_ratio0 + v_shear1 + self.v_phase),
                           self.blend(u_ratio0 + u_shear1 + self.u_phase,
                                      v_ratio1 + v_shear0 + self.v_phase),
                           self.blend(u_ratio1 + u_shear1 + self.u_phase,
                                      v_ratio1 + v_shear1 + self.v_phase)]
                extra_args = {'corners': corners,
                              'fingerprint': [u, v]}
                if self.fingerprint_offset:
                    extra_args['fingerprint'][0] += self.fingerprint_offset[0]
                    extra_args['fingerprint'][1] += self.fingerprint_offset[1]

                if self.id_prefix:
                    extra_args['id'] = "%s[%d][%d]" % (self.id_prefix, u, v)

                if self.color_pattern:
                    extra_args['color_pattern'] = self.color_pattern

                tiles[u][v] = tile_class(self.tessagon,
                                         **{**kwargs, **extra_args})
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
                elif self.v_twist and u == 0:
                    left = tiles[u_prev][self.v_num - v - 1]
                    tile.twist['left'] = True
                else:
                    left = tiles[u_prev][v]

                if not self.v_cyclic and v == self.v_num - 1:
                    top = None
                elif self.u_twist and v == self.v_num - 1:
                    top = tiles[self.u_num - u - 1][v_next]
                    tile.twist['top'] = True
                else:
                    top = tiles[u][v_next]

                if not self.u_cyclic and u == self.u_num - 1:
                    right = None
                elif self.v_twist and u == self.u_num - 1:
                    right = tiles[u_next][self.v_num - v - 1]
                    tile.twist['right'] = True
                else:
                    right = tiles[u_next][v]

                if not self.v_cyclic and v == 0:
                    bottom = None
                elif self.u_twist and v == 0:
                    bottom = tiles[self.u_num - u - 1][v_prev]
                    tile.twist['bottom'] = True
                else:
                    bottom = tiles[u][v_prev]

                tile.set_neighbors(left=left, right=right, top=top,
                                   bottom=bottom)
