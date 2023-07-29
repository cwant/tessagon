from tessagon.types.tiles.penta_tile import PentaTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Pentagons',
                            num_color_patterns=1,
                            classification='laves',
                            shapes=['pentagons'],
                            sides=[5])


class PentaTessagon(Tessagon):
    tile_classes = [PentaTile]
    metadata = metadata
