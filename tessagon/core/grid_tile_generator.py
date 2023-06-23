from tessagon.core.tile_generator import TileGenerator


class GridTileGenerator(TileGenerator):
    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)

        self.tiles = None

    def initialize_tiles(self, **kwargs):
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

                tiles[u][v] = self.create_tile(u, v, corners, **kwargs)

        self.tiles = tiles
        return tiles

    def initialize_neighbors(self, **kwargs):
        tiles = self.tiles
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

    def get_tiles(self):
        return [j for i in self.tiles for j in i]
