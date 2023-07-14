from tessagon.core.tile import Tile


class AlternatingTile(Tile):
    def validate(self):
        this_tile_type = self.tile_type
        for name in self.neighbors:
            neighbor = self.neighbors[name]
            if neighbor and (neighbor.tile_type + this_tile_type != 1):
                raise ValueError("Tiles have bad parity "
                                 "(hint: maybe use an even number of tiles)")

    def calculate_verts(self):
        if self.tile_type == 0:
            self.calculate_verts_type_0()
        else:
            self.calculate_verts_type_1()

    def calculate_faces(self):
        if self.tile_type == 0:
            self.calculate_faces_type_0()
        else:
            self.calculate_faces_type_1()

    @property
    def tile_type(self):
        return sum(self.fingerprint) % 2
