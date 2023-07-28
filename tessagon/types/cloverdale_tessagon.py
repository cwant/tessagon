from tessagon.types.tiles.cloverdale_tile import CloverdaleTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Cloverdale',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['squares', 'pentagons'],
                            sides=[4, 5])


class CloverdaleTessagon(Tessagon):
    tile_classes = [CloverdaleTile]
    metadata = metadata
