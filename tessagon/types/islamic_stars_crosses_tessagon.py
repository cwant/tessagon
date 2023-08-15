from tessagon.types.tiles.islamic_stars_crosses_tiles import \
    IslamicStarsCrossesTile1, IslamicStarsCrossesTile2, \
    IslamicStarsCrossesTile3, IslamicStarsCrossesTile4
from tessagon.core.rotating_tessagon import RotatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Islamic Stars and Crosses',
                            num_color_patterns=1,
                            classification='non_convex',
                            shapes=['stars', 'crosses'],
                            sides=[16])


class IslamicStarsCrossesTessagon(RotatingTessagon):
    tile_classes = [IslamicStarsCrossesTile1, IslamicStarsCrossesTile2,
                    IslamicStarsCrossesTile3, IslamicStarsCrossesTile4]
    metadata = metadata
