from tessagon.core.tile_generator import TileGenerator


class ParallelogramTileGenerator(TileGenerator):
    # This generates tiles that are rotated and combined
    # with a sheer transformation
    # (Turning a collection of tiles into a parallelogram.)
    # This is done so that the tile patterns can still be cyclic.

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)

        # parallelogram_vectors is a pair of pairs, e.g, [[9,1], [-1, 3]]
        # This means:
        #  * For one side of the paralellogram go 9 tiles across, 1 tile up
        #  * From there, the next side you get by going -1 tiles across,
        #    3 tiles up
        # (Other sides are obvious. It's a parallelogram.)
        self.p = kwargs['parallelogram_vectors']
        self.determinant = \
            self.p[0][0] * self.p[1][1] - self.p[1][0] * self.p[0][1]
        self.validate_parallelogram()

        # Rows
        self.inverse = [[self.p[1][1] / (self.determinant * self.u_num),
                         -self.p[1][0] / (self.determinant * self.u_num)],
                        [-self.p[0][1] / (self.determinant * self.v_num),
                         self.p[0][0] / (self.determinant * self.v_num)]]

        self.color_pattern = kwargs.get('color_pattern') or None

        self.id_prefix = 'parallelogram_tiles'

        # Mapped via a fingerprint
        self.tiles = {}

    def validate_parallelogram(self):
        error = None
        if self.p[0][0] <= 0:
            error = "First parallelogram vector can't have negative u"
        elif self.p[1][1] <= 0:
            error = "Second parallelogram vector can't have negative v"
        if self.determinant == 0:
            error = "Parallelogram vector are colinear"
        elif self.determinant < 0:
            error = "First parallelogram vector is to the left of second"
        if error:
            raise ValueError(error)

    def initialize_tiles(self):
        tiles = {}
        fingerprint_range = self.fingerprint_range()
        for u in fingerprint_range[0]:
            for v in fingerprint_range[1]:
                fingerprint = self.normalize_fingerprint(u, v)
                fingerprint_str = str(fingerprint)
                if fingerprint_str not in tiles:
                    if self.valid_fingerprint(*fingerprint):
                        tiles[fingerprint_str] = self.make_tile(*fingerprint)
        self.tiles = tiles
        return tiles

    def initialize_neighbors(self):
        for tile in self.get_tiles():
            u = tile.fingerprint[0]
            v = tile.fingerprint[1]

            fingerprint = self.normalize_fingerprint(u - 1, v)
            fingerprint_str = str(fingerprint)
            left = self.tiles.get(fingerprint_str)

            fingerprint = self.normalize_fingerprint(u + 1, v)
            fingerprint_str = str(fingerprint)
            right = self.tiles.get(fingerprint_str)

            fingerprint = self.normalize_fingerprint(u, v - 1)
            fingerprint_str = str(fingerprint)
            bottom = self.tiles.get(fingerprint_str)

            fingerprint = self.normalize_fingerprint(u, v + 1)
            fingerprint_str = str(fingerprint)
            top = self.tiles.get(fingerprint_str)

            tile.set_neighbors(left=left, right=right, top=top,
                               bottom=bottom)

    def get_tiles(self):
        return self.tiles.values()

    def make_tile(self, *fingerprint):
        corners = self.make_corners(*fingerprint)
        return self.create_tile(fingerprint[0],
                                fingerprint[1],
                                corners)

    def make_corners(self, *fingerprint):
        u = fingerprint[0]
        v = fingerprint[1]

        return [
            self.make_corner(u, v),
            self.make_corner(u + 1, v),
            self.make_corner(u, v + 1),
            self.make_corner(u + 1, v + 1),
        ]

    def make_corner(self, u, v):
        c0 = self.inverse[0][0] * u + self.inverse[0][1] * v
        c1 = self.inverse[1][0] * u + self.inverse[1][1] * v
        return self.blend(c0, c1)

    def valid_fingerprint(self, u, v):
        # Valid = all corners of tile with this fingerprint
        #         are in the parallelogram (may be wrapped if cyclic)

        # Assume u, v have been normalized already
        if not self.point_in_parallelogram(u, v):
            return False

        fingerprint = self.normalize_fingerprint(u + 1, v)
        if not self.point_in_parallelogram(*fingerprint):
            return False

        fingerprint = self.normalize_fingerprint(u, v + 1)
        if not self.point_in_parallelogram(*fingerprint):
            return False

        fingerprint = self.normalize_fingerprint(u + 1, v + 1)
        if not self.point_in_parallelogram(*fingerprint):
            return False

        return True

    def parallelogram_coord(self, u, v):
        # Convert to be in [0, self.u_num] x [0, self.v_num]
        # (ideally if in the parallelogram)

        u_coord = (u * self.p[1][1] - v * self.p[1][0]) / self.determinant
        v_coord = (v * self.p[0][0] - u * self.p[0][1]) / self.determinant

        return (u_coord, v_coord)

    def point_in_parallelogram(self, u, v):
        parallelogram_uv = self.parallelogram_coord(u, v)

        if 0.0 <= parallelogram_uv[0] <= self.u_num:
            if 0.0 <= parallelogram_uv[1] <= self.v_num:
                return True
        return False

    def normalize_fingerprint(self, u, v):
        # Return a canonical fingerprint for tile with this fingerprint
        # Tiles that are essentually the same (due to cyclic/wrapping)
        # will have the same fingerprint.
        # The goal is to not create such tiles more than once
        while (True):
            u_old = u
            v_old = v
            parallelogram_uv = self.parallelogram_coord(u, v)
            if (self.u_cyclic):
                if parallelogram_uv[0] >= self.u_num:
                    u -= (self.u_num * self.p[0][0])
                    v -= (self.u_num * self.p[0][1])
                elif parallelogram_uv[0] < 0.0:
                    u += (self.u_num * self.p[0][0])
                    v += (self.u_num * self.p[0][1])

            if (self.v_cyclic):
                if parallelogram_uv[1] >= self.v_num:
                    u -= (self.v_num * self.p[1][0])
                    v -= (self.v_num * self.p[1][1])
                elif parallelogram_uv[1] < 0.0:
                    u += (self.v_num * self.p[1][0])
                    v += (self.v_num * self.p[1][1])
            if u == u_old and v == v_old:
                return (u, v)

    def fingerprint_range(self):
        # Maximum extents of what the ranges can be ...
        # (Then we can loop over these ranges and see if tiles
        #  with these fingerprints are valid.)
        u_min = min(0,
                    self.u_num * self.p[0][0],
                    self.v_num * self.p[1][0],
                    self.u_num * self.p[0][0] + self.v_num * self.p[1][0])
        u_max = max(0,
                    self.u_num * self.p[0][0],
                    self.v_num * self.p[1][0],
                    self.u_num * self.p[0][0] + self.v_num * self.p[1][0])
        v_min = min(0,
                    self.u_num * self.p[0][1],
                    self.v_num * self.p[1][1],
                    self.u_num * self.p[0][1] + self.v_num * self.p[1][1])
        v_max = max(0,
                    self.u_num * self.p[0][1],
                    self.v_num * self.p[1][1],
                    self.u_num * self.p[0][1] + self.v_num * self.p[1][1])
        return (range(u_min, u_max), range(v_min, v_max))
