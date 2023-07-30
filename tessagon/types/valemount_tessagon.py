from tessagon.types.tiles.valemount_tile import ValemountTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Valemount',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['rectangles', 'squares'],
                            sides=[4])


class ValemountTessagon(Tessagon):
    tile_classes = [ValemountTile]
    metadata = metadata
