from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.types.tiles.dissected_square_tiles import \
    DissectedSquareTile1, DissectedSquareTile2
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Dissected Square',
                            num_color_patterns=2,
                            classification='laves',
                            shapes=['triangles'],
                            sides=[3])


class DissectedSquareTessagon(AlternatingTessagon):
    tile_classes = [DissectedSquareTile1, DissectedSquareTile2]
    metadata = metadata
