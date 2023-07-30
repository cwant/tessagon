from tessagon.types.tiles.slats_tiles import \
    SlatsTile1, SlatsTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Alternating Slats',
                            num_color_patterns=2,
                            classification='non_edge',
                            shapes=['quads', 'rectangles'],
                            sides=[4],
                            extra_parameters={
                                'num_slats': {
                                    'type': 'int',
                                    'min': 2,
                                    'default': 3,
                                    'demo_min': 2,
                                    'demo_max': 5,
                                    'description':
                                    'Control the number of slats'
                                }
                            })


class SlatsTessagon(AlternatingTessagon):
    tile_classes = [SlatsTile1, SlatsTile2]
    metadata = metadata
