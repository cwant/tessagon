from tessagon.types.tiles.square_tri_tiles import \
    SquareTriTile1, SquareTriTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Squares and Triangles',
                            num_color_patterns=2,
                            classification='archimedean',
                            shapes=['squares', 'triangles'],
                            sides=[4, 3])


class SquareTriTessagon(AlternatingTessagon):
    tile_classes = [SquareTriTile1, SquareTriTile2]
    metadata = metadata
