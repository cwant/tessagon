from tessagon.core.tile_generator import TileGenerator


class GridTileGenerator(TileGenerator):
    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)

        self.tiles = None

    def create_tiles(self):
        self.tiles = self.initialize_tiles(self.tessagon.__class__.tile_class)
        self.initialize_neighbors(self.tiles)
        # Flatten the tiles
        return [j for i in self.tiles for j in i]
