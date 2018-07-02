from tessagon.core.stamp14_tessagon \
    import Stamp14, Stamp14Tile, Stamp14Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Hexagons and Big Triangles',
                            classification='non_edge',
                            shapes=['hexagons', 'triangles'],
                            sides=[6, 3])

# To get a sense of how Thingies repeat over tiles, see:
#   https://github.com/cwant/tessagon/blob/master/documentation/images/thingies_repeat.png
# To see how the Thingies are arranged on a tile, see:
#   https://github.com/cwant/tessagon/blob/master/documentation/images/thingies_tiles.png
# To see how Thingy neighbors, verts and faces are arranged, see:
#   https://github.com/cwant/tessagon/blob/master/documentation/images/thingies_neighbors_verts_faces.png


class Thingy(Stamp14):
    def init_verts(self):
        return [None]*13

    def init_faces(self):
        return [None]*3

    def calculate_verts(self):
        unit_u = 1.0 / 14.0
        unit_v = 1.0 / 14.0

        # Hexagon (face 0)
        d_u = unit_u
        d_v = unit_v
        self.add_offset_vert(0, d_u, d_v)
        self.add_offset_vert(2, -d_u, d_v)
        self.add_offset_vert(3, -d_u, -d_v)
        self.add_offset_vert(5, d_u, -d_v)
        d_v = 2 * unit_v
        self.add_offset_vert(1, 0, d_v)
        self.add_offset_vert(4, 0, -d_v)

        # Rest of upper triangle (face 1)
        d_u = 2 * unit_u
        self.add_offset_vert(6, d_u, 0)
        self.add_offset_vert(7, d_u, 2 * unit_v)
        self.add_offset_vert(8, d_u, 4 * unit_v)
        self.add_offset_vert(9, unit_u, 3 * unit_v)

        # Rest of lower triangle (face 2)
        self.add_offset_vert(10, unit_u, -3 * unit_v)
        self.add_offset_vert(11, 2 * unit_u, -2 * unit_v)
        self.add_offset_vert(12, 3 * unit_u, -1 * unit_v)

        # Uggh, this is brutal, be thankful you didn't have to figure this out
        neighbor = self.neighbors[0]
        if neighbor:
            self.set_equivalent_vert(neighbor, 12, 4)
            self.set_equivalent_vert(neighbor, 6, 3)
            self.set_equivalent_vert(neighbor, 7, 2)

        neighbor = self.neighbors[1]
        if neighbor:
            self.set_equivalent_vert(neighbor, 7, 10)
            self.set_equivalent_vert(neighbor, 8, 5)
            self.set_equivalent_vert(neighbor, 9, 4)

        neighbor = self.neighbors[2]
        if neighbor:
            self.set_equivalent_vert(neighbor, 9, 12)
            self.set_equivalent_vert(neighbor, 1, 11)
            self.set_equivalent_vert(neighbor, 2, 10)

        neighbor = self.neighbors[3]
        if neighbor:
            self.set_equivalent_vert(neighbor, 2, 7)
            self.set_equivalent_vert(neighbor, 3, 6)
            self.set_equivalent_vert(neighbor, 4, 12)

        neighbor = self.neighbors[4]
        if neighbor:
            self.set_equivalent_vert(neighbor, 4, 9)
            self.set_equivalent_vert(neighbor, 5, 8)
            self.set_equivalent_vert(neighbor, 10, 7)

        neighbor = self.neighbors[5]
        if neighbor:
            self.set_equivalent_vert(neighbor, 10, 2)
            self.set_equivalent_vert(neighbor, 11, 1)
            self.set_equivalent_vert(neighbor, 12, 9)

    def set_equivalent_vert(self, neighbor, src, dest):
        if not self.verts[src]:
            return
        neighbor.verts[dest] = self.verts[src]

    def calculate_faces(self):
        self.faces[0] = self.tile.mesh_adaptor.create_face(self.verts[0:6])
        verts = [self.verts[i] for i in [6, 7, 8, 9, 1, 0]]
        self.faces[1] = self.tile.mesh_adaptor.create_face(verts)
        verts = [self.verts[i] for i in [10, 11, 12, 6, 0, 5]]
        self.faces[2] = self.tile.mesh_adaptor.create_face(verts)


class HexBigTriTile(Stamp14Tile):
    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, Thingy, **kwargs)


class HexBigTriTessagon(Stamp14Tessagon):
    tile_class = HexBigTriTile
    metadata = metadata
