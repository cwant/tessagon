from tessagon.types.tiles.brick_tiles import BrickTile1, BrickTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Bricks',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['rectangles'],
                            sides=[4])


class BrickTessagon(AlternatingTessagon):
    tile_classes = [BrickTile1, BrickTile2]
    metadata = metadata
