from tessagon.types.tiles.hex_tri_tiles import \
    HexTriTile1, HexTriTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Hexagons and Triangles',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['hexagons', 'triangles'],
                            sides=[6, 3])


class HexTriTessagon(AlternatingTessagon):
    tile_classes = [HexTriTile1, HexTriTile2]
    metadata = metadata
