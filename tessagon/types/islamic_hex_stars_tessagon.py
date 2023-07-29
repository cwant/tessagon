from tessagon.types.tiles.islamic_hex_stars_tiles import \
    IslamicHexStarsTile1, IslamicHexStarsTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Islamic Hexagons and Stars',
                            num_color_patterns=1,
                            classification='non_convex',
                            shapes=['hexagons', 'stars'],
                            sides=[6, 12])


class IslamicHexStarsTessagon(AlternatingTessagon):
    tile_classes = [IslamicHexStarsTile1, IslamicHexStarsTile2]
    metadata = metadata
