from tessagon.core.tessagon import Tessagon


class AlternatingTessagon(Tessagon):

    def get_tile_class(self, fingerprint):
        # TODO: generalize to more than 2?
        return self.__class__.tile_classes[sum(fingerprint) % 2]

    def validate_tile(self, tile):
        # Do the tiles actually alternate?

        fingerprint = sum(tile.fingerprint) % 2
        other_class = self.__class__.tile_classes[(fingerprint + 1) % 2]
        for neighbor in tile.get_neighbor_tiles():
            if neighbor.__class__ != other_class:
                raise ValueError("{}: Tiles have bad parity "
                                 "(hint: maybe use an even number of tiles)".
                                 format(self.__class__.__name__))
