from tessagon.types.tiles.dodeca_tiles import \
    DodecaTile1, DodecaTile2
from tessagon.core.alternating_tessagon import AlternatingTessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Dodecagons, Hexagons, and Squares',
                            num_color_patterns=1,
                            classification='archimedean',
                            shapes=['dodecagons', 'hexagons', 'squares'],
                            sides=[12, 6, 4])


class DodecaTessagon(AlternatingTessagon):
    tile_classes = [DodecaTile1, DodecaTile2]
    metadata = metadata
