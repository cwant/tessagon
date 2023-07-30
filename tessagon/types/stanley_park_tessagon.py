from tessagon.core.tessagon import Tessagon
from tessagon.types.tiles.stanley_park_tile import StanleyParkTile
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Stanley Park',
                            num_color_patterns=2,
                            classification='non_convex',
                            sides=[12])


class StanleyParkTessagon(Tessagon):
    tile_classes = [StanleyParkTile]
    metadata = metadata
