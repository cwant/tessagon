from tessagon.types.tiles.brick_tile import BrickTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Bricks',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['rectangles'],
                            sides=[4])


class BrickTessagon(Tessagon):
    tile_classes = [BrickTile]
    metadata = metadata
