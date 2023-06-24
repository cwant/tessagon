from tessagon.core.tile import Tile


class AlternatingTile(Tile):
    def validate(self):
        this_tile_type = self.tile_type
        for name in self.neighbors:
            neighbor = self.neighbors[name]
            if neighbor and (neighbor.tile_type + this_tile_type != 1):
                raise ValueError("Tiles have bad parity "
                                 "(hint: maybe use an even number of tiles)")

    @property
    def tile_type(self):
        return sum(self.fingerprint) % 2
