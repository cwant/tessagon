from tessagon.types.tiles.weave_tiles import \
    WeaveTile1, WeaveTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Weave',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['quads', 'rectangles'],
                            sides=[4],
                            extra_parameters={
                                'square_ratio': {
                                    'type': 'float',
                                    'min': 0.0,
                                    'max': 1.0,
                                    'default': 0.5,
                                    'description':
                                    'Control the size of the squares'
                                }
                            })


class WeaveTessagon(AlternatingTessagon):
    tile_classes = [WeaveTile1, WeaveTile2]
    metadata = metadata
