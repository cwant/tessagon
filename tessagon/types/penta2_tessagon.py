from tessagon.types.tiles.penta2_tiles import \
    Penta2Tile1, Penta2Tile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Other Pentagons',
                            num_color_patterns=1,
                            classification='laves',
                            shapes=['pentagons'],
                            sides=[5])


class Penta2Tessagon(AlternatingTessagon):
    tile_classes = [Penta2Tile1, Penta2Tile2]
    metadata = metadata
