from tessagon.core.stamp14_tessagon \
    import Stamp14, Stamp14Tile, Stamp14Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Florets',
                            num_color_patterns=3,
                            classification='laves',
                            shapes=['pentagons'],
                            sides=[5])

# To get a sense of how Florets repeat over tiles, see:
#   https://github.com/cwant/tessagon/blob/master/documentation/images/florets_repeat.png
# To see how the Florets are arranged on a tile, see:
#   https://github.com/cwant/tessagon/blob/master/documentation/images/florets_tiles.png
# To see how Floret neighbors, verts and faces are arranged, see:
#   https://github.com/cwant/tessagon/blob/master/documentation/images/florets_neighbors_verts_faces.png


class Floret(Stamp14):
    def init_verts(self):
        return [None]*19

    def init_faces(self):
        return [None]*6

    def add_offset_vert(self, i, offset_u, offset_v):
        vert = super().add_offset_vert(i, offset_u, offset_v)
        if vert:
            if i == 18:
                self.tile.tessagon.vert_types['center'].append(vert)
            elif i % 3 == 2:
                self.tile.tessagon.vert_types['other'].append(vert)
            else:
                self.tile.tessagon.vert_types['edge_to_center'].append(vert)
        return True

    def calculate_verts(self):
        self.add_offset_vert(18, 0, 0)

        unit_u = 2.0 / 42.0
        unit_v = 1.0 / 14.0

        d_u = 2.0 * unit_u
        d_v = 2.0 * unit_v
        self.add_offset_vert(0, d_u, 0)
        self.add_offset_vert(9, -d_u, 0)

        self.add_offset_vert(2, d_u, d_v)
        self.add_offset_vert(16, d_u, -d_v)
        self.add_offset_vert(7, -d_u, d_v)
        self.add_offset_vert(11, -d_u, -d_v)
        d_u = unit_u
        self.add_offset_vert(3, d_u, d_v)
        self.add_offset_vert(15, d_u, -d_v)
        self.add_offset_vert(6, -d_u, d_v)
        self.add_offset_vert(12, -d_u, -d_v)
        d_u = 0.5 * unit_u
        d_v = 3 * unit_v
        self.add_offset_vert(4, d_u, d_v)
        self.add_offset_vert(14, d_u, -d_v)
        self.add_offset_vert(5, -d_u, d_v)
        self.add_offset_vert(13, -d_u, -d_v)
        d_u = 2.5 * unit_u
        d_v = unit_v
        self.add_offset_vert(1, d_u, d_v)
        self.add_offset_vert(17, d_u, -d_v)
        self.add_offset_vert(8, -d_u, d_v)
        self.add_offset_vert(10, -d_u, -d_v)

        # Making things non-manifold using mathemagics
        for neighbor in range(6):
            other_floret = self.neighbors[neighbor]
            if not other_floret:
                continue
            for i in range(4):
                src = (3 * neighbor + i - 1) % 18
                dest = (3 * neighbor - i + 11) % 18
                if self.verts[src]:
                    other_floret.verts[dest] = self.verts[src]

    def calculate_faces(self):
        for i in range(6):
            last = (3*i + 3) % 18
            verts = [self.verts[3*i], self.verts[3*i + 1],
                     self.verts[3*i + 2], self.verts[last],
                     self.verts[18]]
            self.faces[i] = self.tile.mesh_adaptor.create_face(verts)


class FloretTile(Stamp14Tile):

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, Floret, **kwargs)

    def color_pattern1(self):
        for i in range(14):
            if not self.stamps[i]:
                continue
            if (i - self.fingerprint[1]) % 3 == 0:
                self.stamps[i].color_stamp(1)
            else:
                self.stamps[i].color_stamp(0)

    def color_pattern2(self):
        for i in range(14):
            if not self.stamps[i]:
                continue
            color = (i - self.fingerprint[1]) % 3
            self.stamps[i].color_stamp(color)

    def set_default_color(self, color):
        for i in range(14):
            if not self.stamps[i]:
                continue
            self.stamps[i].color_stamp(color)

    def color_pattern3(self):
        for i in range(14):
            if ((i // 5) + self.fingerprint[0] + self.fingerprint[1]) % 2 > 0:
                continue
            if (i + 2 * self.fingerprint[1]) % 6 > 0:
                continue
            self.stamps[i].color_stamp(1)
            for stamp in self.stamps[i].neighbors:
                stamp.color_stamp(2)


class FloretTessagon(Stamp14Tessagon):
    tile_class = FloretTile
    metadata = metadata

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vert_types = {'center': [], 'edge_to_center': [], 'other': []}

    def _calculate_colors(self):
        self.mesh_adaptor.initialize_colors()
        if self.color_pattern == 3:
            for tile in self.tiles:
                tile.set_default_color(0)
        for tile in self.tiles:
            tile.calculate_colors()
