from tessagon.types.tiles.octa_tile import OctaTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Octagons and Squares',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['octagons', 'squares'],
                            sides=[8, 4],
                            uv_ratio=1.0)


class OctaTessagon(Tessagon):
    tile_classes = [OctaTile]
    metadata = metadata
