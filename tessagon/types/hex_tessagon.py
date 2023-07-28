from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.types.tiles.hex_tiles import HexTile1, HexTile2
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Regular Hexagons',
                            num_color_patterns=2,
                            classification='regular',
                            shapes=['hexagons'],
                            sides=[6])


class HexTessagon(AlternatingTessagon):
    tile_classes = [HexTile1, HexTile2]
    metadata = metadata
