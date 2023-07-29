from tessagon.types.tiles.rhombus_tiles import \
    RhombusTile1, RhombusTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Rhombuses',
                            num_color_patterns=2,
                            classification='laves',
                            shapes=['rhombuses'],
                            sides=[4])


class RhombusTessagon(AlternatingTessagon):
    tile_classes = [RhombusTile1, RhombusTile2]
    metadata = metadata
