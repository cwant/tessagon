from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.types.tiles.big_hex_tri_tiles import \
    BigHexTriTile1, BigHexTriTile2

metadata = TessagonMetadata(name='Big Hexagons and Triangles',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['hexagons', 'triangles'],
                            sides=[6, 3],
                            extra_parameters={
                                'hexagon_ratio': {
                                    'type': 'float',
                                    'min': 0.0,
                                    # Any higher than 0.70, and verts are
                                    # pushed to neighboring tiles
                                    'max': 0.70,
                                    'default': 0.5,
                                    'description':
                                    'Control the size of the Hexagons'
                                }
                            })


class BigHexTriTessagon(AlternatingTessagon):
    tile_classes = [BigHexTriTile1, BigHexTriTile2]
    metadata = metadata
