from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.types.tiles.tri_tiles import TriTile1, TriTile2
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Regular Triangles',
                            num_color_patterns=3,
                            classification='regular',
                            shapes=['triangles'],
                            sides=[3])


class TriTessagon(AlternatingTessagon):
    tile_classes = [TriTile1, TriTile2]
    metadata = metadata
