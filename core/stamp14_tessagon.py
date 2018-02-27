from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile


class Stamp14:
    def __init__(self, tile, i, reference_point):
        self.tile = tile
        self.neighbors = [None]*6
        self.verts = self.init_verts()
        self.faces = self.init_faces()
        self.reference_point = reference_point

    def set_neighbor(self, index, stamp):
        if self.neighbors[index]:
            return
        if not stamp:
            return
        self.neighbors[index] = stamp
        stamp.neighbors[(index + 3) % 6] = self

    def offset_point(self, offset_u, offset_v):
        uv = [self.reference_point[0] + offset_u,
              self.reference_point[1] + offset_v]
        return self.tile.f(*self.tile.blend(*uv))

    def offset_vert(self, offset_u, offset_v):
        point = self.offset_point(offset_u, offset_v)
        return self.tile.mesh_adaptor.create_vert(point)

    def add_offset_vert(self, i, offset_u, offset_v):
        if self.verts[i]:
            return None
        vert = self.verts[i] = self.offset_vert(offset_u, offset_v)
        return vert

    def color_stamp(self, color):
        for face in self.faces:
            self.tile.mesh_adaptor.color_face(face, color)


class Stamp14Tile(Tile):
    def __init__(self, tessagon, stamp_class, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.stamp_class = stamp_class
        # See comment at the top of file for arrangement
        self.stamps = [None] * 14

    def initialize_stamps(self):
        for i in range(14):
            self.initialize_stamp(i)

    def initialize_stamp(self, i):
        if self.stamps[i]:
            return

        if i in [0, 1, 2]:
            if not self.get_neighbor_tile(['bottom']):
                return
            if i == 0:
                if not self.get_neighbor_tile(['left']):
                    return
                if not self.get_neighbor_tile(['bottom', 'left']):
                    return

        if i == 5:
            if not self.get_neighbor_tile(['left']):
                return
        if i == 9:
            if not self.get_neighbor_tile(['right']):
                return

        if i in [12, 13]:
            if not self.get_neighbor_tile(['top']):
                return

        u = i * (3.0 / 14.0)
        v = u / 3.0
        while u > 1:
            u -= 1.0
        self.stamps[i] = self.stamp_class(self, i, [u, v])

    def initialize_stamps_neighbors(self):
        for i in range(14):
            self.initialize_stamp_neighbors(i)

    def initialize_stamp_neighbors(self, i):
        # All of this is to ensure the mesh is non-manifold
        if not self.stamps[i]:
            return
        stamp = self.stamps[i]
        row = i // 5  # must be integer division
        column = i % 5

        # neighbor 0:
        if column < 4 and i < 13:
            stamp.set_neighbor(0, self.stamps[i + 1])
        elif i == 13:
            stamp.set_neighbor(0, self.get_neighbor_stamp(['right', 'top'], 0))
        else:
            stamp.set_neighbor(0, self.get_neighbor_stamp(['right'], i + 1))

        # neighbor 1:
        if row < 2 and i < 9:
            stamp.set_neighbor(1, self.stamps[i + 5])
        elif i == 9:
            stamp.set_neighbor(1, self.get_neighbor_stamp(['right', 'top'], 0))
        else:
            stamp.set_neighbor(1, self.get_neighbor_stamp(['top'], i - 9))

        # neighbor 2:
        if row < 2 and column > 0:
            stamp.set_neighbor(2, self.stamps[i + 4])
        elif column == 0 and i != 10:
            stamp.set_neighbor(2, self.get_neighbor_stamp(['left'], i + 4))
        else:
            stamp.set_neighbor(2, self.get_neighbor_stamp(['top'], i - 10))

        # neighbor 3:
        if column > 1:
            stamp.set_neighbor(3, self.stamps[i - 1])
        elif i == 0:
            stamp.set_neighbor(3, self.get_neighbor_stamp(['left', 'bottom'],
                                                          13))
        else:
            stamp.set_neighbor(3, self.get_neighbor_stamp(['left'], i - 1))

        # neighbor 4:
        if row > 0:
            stamp.set_neighbor(4, self.stamps[i - 5])
        elif i == 0:
            stamp.set_neighbor(4, self.get_neighbor_stamp(['left', 'bottom'],
                                                          9))
        else:
            stamp.set_neighbor(4, self.get_neighbor_stamp(['bottom'], i + 9))

        # neighbor 5:
        if row > 0 and column < 4:
            stamp.set_neighbor(5, self.stamps[i - 4])
        elif column == 4:
            stamp.set_neighbor(5, self.get_neighbor_stamp(['right'], i - 4))
        else:
            stamp.set_neighbor(5, self.get_neighbor_stamp(['bottom'], i + 10))

    def get_neighbor_stamp(self, neighbor_keys, index):
        tile = self.get_neighbor_tile(neighbor_keys)
        if not tile:
            return None
        return tile.stamps[index]

    def init_verts(self):
        # The stamps handle the storage for the verts
        return None

    def calculate_verts(self):
        for stamp in self.stamps:
            if stamp:
                stamp.calculate_verts()

    def init_faces(self):
        # The stamps handle the storage for the faces
        return None

    def calculate_faces(self):
        for stamp in self.stamps:
            if stamp:
                stamp.calculate_faces()


class Stamp14Tessagon(Tessagon):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stamps = []

    def _initialize_tiles(self):
        super()._initialize_tiles()
        self._initialize_stamps()
        self._initialize_stamp_neighbors()

    def _initialize_stamps(self):
        for tile in self.tiles:
            tile.initialize_stamps()

    def _initialize_stamp_neighbors(self):
        for tile in self.tiles:
            tile.initialize_stamps_neighbors()
