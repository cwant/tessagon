from tessagon.types.tiles.hokusai_hashes_tile import HokusaiHashesTile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Hashes by Hokusai',
                            num_color_patterns=2,
                            classification='non_manifold',
                            shapes=['quads', 'hashes'],
                            sides=[4, 28])


class HokusaiHashesTessagon(Tessagon):
    tile_classes = [HokusaiHashesTile]
    metadata = metadata
    face_order = ['hash', 'square']
