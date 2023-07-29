from math import sqrt, pi, asin
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.types.tiles.hokusai_parallelograms_tiles import \
    HokusaiParallelogramsTile1, HokusaiParallelogramsTile2
from tessagon.core.tessagon_metadata import TessagonMetadata

# The default makes pattern fit on grid of regular triangles
# Solve triangle a = sqrt(7), b = 2, c = 3, angle A = pi/3
# Use sin law gives B = asin(sqrt(3)/sqrt(7))
# The rest comes from inverting theta_offset definition below
default_triangle_ratio = (asin(sqrt(3)/sqrt(7)) - pi/6) / (pi/6)

metadata = TessagonMetadata(name='Hokusai Parallelograms and Triangles',
                            num_color_patterns=3,
                            classification='non_edge',
                            shapes=['parallelograms', 'triangles'],
                            sides=[6, 3],
                            extra_parameters={
                                'triangle_ratio': {
                                    'type': 'float',
                                    'min': 0.0,
                                    'max': 1.0,
                                    'default': default_triangle_ratio,
                                    'description':
                                    'Control the size of the triangles'
                                }
                            })


class HokusaiParallelogramsTessagon(AlternatingTessagon):
    tile_classes = [HokusaiParallelogramsTile1, HokusaiParallelogramsTile2]
    metadata = metadata
