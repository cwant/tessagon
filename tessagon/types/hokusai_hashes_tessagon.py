from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import left_tile, right_tile, \
    bottom_left_tile, bottom_tile, bottom_right_tile, \
    top_left_tile, top_tile, top_right_tile

metadata = TessagonMetadata(name='Hashes by Hokusai',
                            num_color_patterns=2,
                            classification='non_manifold',
                            shapes=['quads', 'hashes'],
                            sides=[4, 28],
                            uv_ratio=1.0)


class HokusaiHashesTile(Tile):
    # From: https://gallica.bnf.fr/ark:/12148/btv1b105092395/f12.item
    # See the SVG for decomposition:
    # https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/hokusai_hashes.svg
    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False
        # self.rot_symmetric = 90

    def init_verts(self):
        verts = {}
        for i in ['rotate0', 'rotate90', 'rotate180', 'rotate270']:
            verts[i] = {'square': None, 1: None, 2: None, 3: None, 4: None}

        return verts

    def init_faces(self):
        return dict(hash=None, square=None)

    def transform_vert(self, x, y):
        # Switch from the axis aligned easy coords, to the
        # rotated non-easy coords
        # e.g, (4, 1) --> (1, 0)
        #      (-1, 4) --> (0, 1)
        return [x * 4/17 + y * 1/17, x * (-1/17) + y * 4/17]

    def calculate_verts(self):
        verts = [self.transform_vert(0, 2),
                 self.transform_vert(0, 1),
                 self.transform_vert(0, 0),
                 self.transform_vert(1, 1),
                 self.transform_vert(1, 2)]
        neighbors = [left_tile,
                     bottom_left_tile,
                     bottom_tile,
                     bottom_right_tile,
                     right_tile,
                     top_right_tile,
                     top_tile,
                     top_left_tile]
        rotations = ['rotate0', 'rotate90', 'rotate180', 'rotate270']
        for i in range(4):
            def rot(j): return rotations[(i + j) % 4]
            def neighb(j): return neighbors[(2*i + j) % 8]

            self.add_vert([rot(0), 1], *verts[0])
            self.add_vert([rot(0), 2], *verts[1])
            self.add_vert([rot(0), 3], *verts[2],
                          equivalent=[neighb(0)([rot(1), 3]),
                                      neighb(1)([rot(2), 3]),
                                      neighb(2)([rot(3), 3])])

            self.add_vert([rot(0), 4], *verts[3])
            self.add_vert([rot(0), 'square'], *verts[4])

            if (rot != 'rotate270'):
                verts = [self.rotate_90(*vert) for vert in verts]

    def calculate_faces(self):
        # Easy one first ...
        self.add_face('square',
                      [['rotate0', 'square'],
                       ['rotate90', 'square'],
                       ['rotate180', 'square'],
                       ['rotate270', 'square']],
                      face_type='square')

        # This one is less fun ... (28 verts total)
        neighbors = [left_tile, bottom_tile, right_tile, top_tile]
        rotations = ['rotate0', 'rotate90', 'rotate180', 'rotate270']
        verts = []
        for i in range(4):
            def rot(j): return rotations[(i + j) % 4]
            def neighb(j): return neighbors[(i + j) % 4]
            new_verts = [[rot(0), 1],
                         neighb(0)([rot(2), 1]),
                         neighb(0)([rot(1), 4]),
                         [rot(0), 2],
                         [rot(0), 3],
                         neighb(1)([rot(3), 2]),
                         [rot(0), 4]]
            verts += new_verts
        # Does anybody else smell burnt toast about now?
        self.add_face('hash', verts, face_type='hash')

    def color_pattern1(self):
        self.color_face('square', 1)

    def color_pattern2(self):
        if (self.fingerprint[0] + self.fingerprint[1]) % 2 == 0:
            self.color_face('square', 1)
        else:
            self.color_face('hash', 1)


class HokusaiHashesTessagon(Tessagon):
    tile_class = HokusaiHashesTile
    metadata = metadata
    face_order = ['hash', 'square']
