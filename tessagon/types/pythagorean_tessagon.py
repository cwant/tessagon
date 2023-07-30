from tessagon.types.tiles.pythagorean_tile import PythagoreanTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Pythagorean',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['squares'],
                            sides=[4],
                            extra_parameters={
                                'square_ratio': {
                                    'type': 'float',
                                    'min': 0.0,
                                    'max': 1.0,
                                    'default': 0.5,
                                    'description':
                                    'Control the size of the little squares'
                                }
                            })


class PythagoreanTessagon(Tessagon):
    tile_classes = [PythagoreanTile]
    metadata = metadata
