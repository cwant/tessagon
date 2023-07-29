from tessagon.types.tiles.islamic_stars_crosses_tile import \
    IslamicStarsCrossesTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Islamic Stars and Crosses',
                            num_color_patterns=1,
                            classification='non_convex',
                            shapes=['stars', 'crosses'],
                            sides=[16])


class IslamicStarsCrossesTessagon(Tessagon):
    tile_classes = [IslamicStarsCrossesTile]
    metadata = metadata
