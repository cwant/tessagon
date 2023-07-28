from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.types.tiles.dissected_hex_quad_tiles import \
    DissectedHexQuadTile1, DissectedHexQuadTile2

metadata = TessagonMetadata(name='Hexagons Dissected with Quads',
                            num_color_patterns=2,
                            classification='laves',
                            shapes=['quads'],
                            sides=[4])


class DissectedHexQuadTessagon(AlternatingTessagon):
    tile_classes = [DissectedHexQuadTile1, DissectedHexQuadTile2]
    metadata = metadata
