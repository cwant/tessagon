from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.types.tiles.dissected_hex_tri_tiles import \
    DissectedHexTriTile1, DissectedHexTriTile2

metadata = TessagonMetadata(name='Hexagons Dissected with Triangles',
                            num_color_patterns=1,
                            classification='laves',
                            shapes=['triangles'],
                            sides=[3])


class DissectedHexTriTessagon(AlternatingTessagon):
    tile_classes = [DissectedHexTriTile1, DissectedHexTriTile2]
    metadata = metadata
