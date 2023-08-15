from tessagon.core.tessagon import Tessagon


class RotatingTessagon(Tessagon):
    # Needs 4 tiles
    # (each a 90 degree counter-clockwise rotation of the previous one)

    def get_tile_class(self, fingerprint):
        #  Counter-clockwise
        #  3  2  3  2
        #  0  1  0  1
        #  3  2  3  2
        #  0  1  0  1
        tile_index = (fingerprint[0] % 2) + 3 * (fingerprint[1] % 2) \
            - 2*(fingerprint[0] % 2) * (fingerprint[1] % 2)
        return self.__class__.tile_classes[tile_index]

    def validate_tile(self, tile):
        # TODO: figure this out?
        pass
