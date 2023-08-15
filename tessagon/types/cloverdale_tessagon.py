from tessagon.types.tiles.cloverdale_tiles import \
    CloverdaleTile1, CloverdaleTile2, CloverdaleTile3, CloverdaleTile4
from tessagon.core.rotating_tessagon import RotatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Cloverdale',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['squares', 'pentagons'],
                            sides=[4, 5])


class CloverdaleTessagon(RotatingTessagon):
    tile_classes = [CloverdaleTile1, CloverdaleTile2,
                    CloverdaleTile3, CloverdaleTile4]
    metadata = metadata
