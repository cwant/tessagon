from tessagon.types.tiles.floret_tiles import \
    FloretTile1, FloretTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Florets',
                            num_color_patterns=3,
                            classification='laves',
                            shapes=['pentagons'],
                            sides=[5])


class FloretTessagon(AlternatingTessagon):
    tile_classes = [FloretTile1, FloretTile2]
    metadata = metadata
