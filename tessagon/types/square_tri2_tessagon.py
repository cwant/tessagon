from tessagon.types.tiles.square_tri2_tiles import \
    SquareTri2Tile1, SquareTri2Tile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Other Squares and Triangles',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['squares', 'triangles'],
                            sides=[4, 3])


class SquareTri2Tessagon(AlternatingTessagon):
    tile_classes = [SquareTri2Tile1, SquareTri2Tile2]
    metadata = metadata
