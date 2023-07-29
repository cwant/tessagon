from tessagon.types.tiles.dissected_triangle_tiles import \
    DissectedTriangleTile1, DissectedTriangleTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Dissected Triangle',
                            num_color_patterns=1,
                            classification='laves',
                            shapes=['triangles'],
                            sides=[3])


class DissectedTriangleTessagon(AlternatingTessagon):
    tile_classes = [DissectedTriangleTile1, DissectedTriangleTile2]
    metadata = metadata
