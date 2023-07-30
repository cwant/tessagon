from tessagon.types.tiles.penta_tiles import \
    PentaTile1, PentaTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Pentagons',
                            num_color_patterns=1,
                            classification='laves',
                            shapes=['pentagons'],
                            sides=[5])


class PentaTessagon(AlternatingTessagon):
    tile_classes = [PentaTile1, PentaTile2]
    metadata = metadata
