from tessagon.types.tiles.zig_zag_tiles import \
    ZigZagTile1, ZigZagTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Zig-Zag',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['rectangles'],
                            sides=[4])


class ZigZagTessagon(AlternatingTessagon):
    tile_classes = [ZigZagTile1, ZigZagTile2]
    metadata = metadata
