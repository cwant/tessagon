from tessagon.core.tessagon import Tessagon


class AlternatingTessagon(Tessagon):

    def get_tile_class(self, fingerprint):
        # TODO: generalize to more than 2?
        return self.__class__.tile_classes[sum(fingerprint) % 2]
