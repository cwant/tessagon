from tessagon.types.tiles.hex_big_tri_tiles import \
    HexBigTriTile1, HexBigTriTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Hexagons and Big Triangles',
                            num_color_patterns=2,
                            classification='non_edge',
                            shapes=['hexagons', 'triangles'],
                            sides=[6, 3])


class HexBigTriTessagon(AlternatingTessagon):
    tile_classes = [HexBigTriTile1, HexBigTriTile2]
    metadata = metadata
