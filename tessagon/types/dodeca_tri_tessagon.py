from tessagon.types.tiles.dodeca_tri_tiles import \
    DodecaTriTile1, DodecaTriTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Dodecagons and Triangles',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['dodecagons', 'triangles'],
                            sides=[12, 3])


class DodecaTriTessagon(AlternatingTessagon):
    tile_classes = [DodecaTriTile1, DodecaTriTile2]
    metadata = metadata
