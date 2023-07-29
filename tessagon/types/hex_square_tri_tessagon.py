from tessagon.types.tiles.hex_square_tri_tiles import \
    HexSquareTriTile1, HexSquareTriTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Hexagons, Squares, and Triangles',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['hexagons', 'squares', 'triangles'],
                            sides=[6, 4, 3])


class HexSquareTriTessagon(AlternatingTessagon):
    tile_classes = [HexSquareTriTile1, HexSquareTriTile2]
    metadata = metadata
