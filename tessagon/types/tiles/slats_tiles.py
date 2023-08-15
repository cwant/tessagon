from tessagon.core.tile import Tile
from tessagon.core.tile_boundary import TileBoundary


class SlatsTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        self.u_symmetric = False
        self.v_symmetric = False
        self.num_slats = kwargs.get('num_slats', 3)
        # Why does this only work if this line is the last one?
        super().__init__(tessagon, **kwargs)

    def init_boundary(self):
        side = []
        for i in range(1, self.num_slats + 1):
            side.extend(['vert-{}'.format(i), 'edge'])
        side.append('vert-{}'.format(self.num_slats + 1))
        boundary = {'top': side,
                    'left': side,
                    'bottom': side,
                    'right': side}
        self.boundary = TileBoundary(self, **boundary)

    def init_verts(self):
        # Start at [0, 0], go counter-clockwise around boundary
        return {k: None for k in range(4 * self.num_slats)}

    def init_faces(self):
        # These are either vertical or horizontal, depending on tile_type
        return {i: None for i in range(self.num_slats)}

    def calculate_verts(self):
        last_feature = 'vert-{}'.format(self.num_slats + 1)
        self.add_vert(0,
                      0, 0,
                      left_boundary=last_feature)

        self.add_vert(self.num_slats,
                      1, 0,
                      bottom_boundary=last_feature)

        self.add_vert(2 * self.num_slats,
                      1, 1,
                      right_boundary=last_feature)

        self.add_vert(3 * self.num_slats,
                      0, 1,
                      top_boundary=last_feature)

        for i in range(1, self.num_slats):
            ratio = i / self.num_slats
            feature = 'vert-{}'.format(i + 1)

            bottom_index = i
            right_index = bottom_index + self.num_slats
            top_index = right_index + self.num_slats
            left_index = top_index + self.num_slats

            self.add_vert(bottom_index,
                          ratio, 0,
                          bottom_boundary=feature)

            self.add_vert(right_index,
                          1, ratio,
                          right_boundary=feature)

            self.add_vert(top_index,
                          1 - ratio, 1,
                          top_boundary=feature)

            self.add_vert(left_index,
                          0, 1 - ratio,
                          left_boundary=feature)


class SlatsTile1(SlatsTile):
    def calculate_faces(self):
        # horizontal

        # First and last slats are tricky, because they have
        # a lot of verts on what looks like a straight line
        # self.num_slats + 3 verts on each boundary slat.

        bottom_vert_indices = [4 * self.num_slats - 1]
        top_vert_indices = [2 * self.num_slats - 1]
        for i in range(self.num_slats + 2):
            bottom_vert_indices.append(i)
            top_vert_indices.append(i + 2 * self.num_slats)
        self.add_face(0, bottom_vert_indices)
        self.add_face(self.num_slats - 1, top_vert_indices)

        # Interior slats
        for i in range(1, self.num_slats - 1):
            left_index = 4 * self.num_slats - i
            right_index = i + self.num_slats
            self.add_face(i,
                          [left_index,
                           right_index,
                           right_index + 1,
                           left_index - 1])

    def color_pattern1(self):
        pass

    def color_pattern2(self):
        for face in self.faces:
            if face % 2 == 0:
                self.color_face(face, 1)


class SlatsTile2(SlatsTile):

    def calculate_faces(self):
        # vertical

        # First and last slats are tricky, because they have
        # a lot of verts on what looks like a straight line
        # self.num_slats + 3 verts on each boundary slat.

        left_vert_indices = [0, 1]
        right_vert_indices = [self.num_slats - 1, self.num_slats]
        for i in range(self.num_slats + 1):
            left_vert_indices.append(i + 3 * self.num_slats - 1)
            right_vert_indices.append(i + self.num_slats + 1)
        self.add_face(0, left_vert_indices)
        self.add_face(self.num_slats - 1, right_vert_indices)

        # Interior slats
        for i in range(1, self.num_slats - 1):
            bottom_index = i
            top_index = 3 * self.num_slats - i
            self.add_face(i,
                          [bottom_index,
                           bottom_index + 1,
                           top_index - 1,
                           top_index])

    def color_pattern1(self):
        for face in self.faces:
            self.color_face(face, 1)

    def color_pattern2(self):
        for face in self.faces:
            if face % 2 == 1:
                self.color_face(face, 1)
