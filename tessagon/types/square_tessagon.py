from tessagon.types.tiles.square_tile import SquareTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Regular Squares',
                            num_color_patterns=8,
                            classification='regular',
                            shapes=['squares'],
                            sides=[4])


class SquareTessagon(Tessagon):
    tile_classes = [SquareTile]
    metadata = metadata
