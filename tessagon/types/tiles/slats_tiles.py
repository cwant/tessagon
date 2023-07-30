from tessagon.core.tile import Tile
from tessagon.core.tile_utils import left_tile, right_tile, \
    top_tile, bottom_tile, top_left_tile, top_right_tile, \
    bottom_left_tile, bottom_right_tile


class SlatsTile(Tile):
    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        self.u_symmetric = False
        self.v_symmetric = False
        self.num_slats = kwargs.get('num_slats', 3)
        # Why does this only work if this line is the last one?
        super().__init__(tessagon, **kwargs)

    def init_verts(self):
        verts = {'corner': {}}

        # corner verts, and a bunch of verts around each edge
        for top_bottom in ['top', 'bottom']:
            verts['corner'][top_bottom] = {}
            for left_right in ['left', 'right']:
                verts['corner'][top_bottom][left_right] = None
        for direction in ['top', 'bottom', 'left', 'right']:
            verts[direction] = {i: None for i in range(1, self.num_slats)}

        return verts

    def init_faces(self):
        # These are either vertical or horizontal, depending on tile_type
        faces = {i: None for i in range(self.num_slats)}
        return faces

    def calculate_verts(self):
        for i in range(1, self.num_slats):
            ratio = i / self.num_slats
            self.add_vert(['bottom', i], ratio, 0,
                          equivalent=[bottom_tile(['top', i])])
            self.add_vert(['top', i], ratio, 1,
                          equivalent=[top_tile(['bottom', i])])
            self.add_vert(['left', i], 0, ratio,
                          equivalent=[left_tile(['right', i])])
            self.add_vert(['right', i], 1, ratio,
                          equivalent=[right_tile(['left', i])])

        self.add_vert(['corner', 'bottom', 'left'], 0, 0,
                      equivalent=[left_tile(['corner', 'bottom', 'right']),
                                  bottom_left_tile(['corner', 'top', 'right']),
                                  bottom_tile(['corner', 'top', 'left'])])
        self.add_vert(['corner', 'bottom', 'right'], 1, 0,
                      equivalent=[right_tile(['corner', 'bottom', 'left']),
                                  bottom_right_tile(['corner', 'top', 'left']),
                                  bottom_tile(['corner', 'top', 'right'])])
        self.add_vert(['corner', 'top', 'left'], 0, 1,
                      equivalent=[left_tile(['corner', 'top', 'right']),
                                  top_left_tile(['corner', 'bottom', 'right']),
                                  top_tile(['corner', 'bottom', 'left'])])
        self.add_vert(['corner', 'top', 'right'], 1, 1,
                      equivalent=[right_tile(['corner', 'top', 'left']),
                                  top_right_tile(['corner', 'bottom', 'left']),
                                  top_tile(['corner', 'bottom', 'right'])])


class SlatsTile1(SlatsTile):

    def calculate_faces(self):
        # horizontal
        for i in range(1, self.num_slats - 1):
            self.add_face(i,
                          [['left', i],
                           ['right', i],
                           ['right', i + 1],
                           ['left', i + 1]])

        bottom_verts = [['corner', 'bottom', 'left']]
        top_verts = [['corner', 'top', 'left']]
        for i in range(1, self.num_slats):
            bottom_verts.append(['bottom', i])
            top_verts.append(['top', i])

        bottom_verts.extend([['corner', 'bottom', 'right'],
                             ['right', 1],
                             ['left', 1]])
        top_verts.extend([['corner', 'top', 'right'],
                          ['right', self.num_slats - 1],
                          ['left', self.num_slats - 1]])
        self.add_face(0, bottom_verts)
        self.add_face(self.num_slats - 1, list(reversed(top_verts)))

    def color_pattern1(self):
        pass

    def color_pattern2(self):
        for face in self.faces:
            if face % 2 == 0:
                self.color_face(face, 1)


class SlatsTile2(SlatsTile):

    def calculate_faces(self):
        # vertical
        for i in range(1, self.num_slats - 1):
            self.add_face(i,
                          [['top', i],
                           ['bottom', i],
                           ['bottom', i + 1],
                           ['top', i + 1]])

        left_verts = [['corner', 'bottom', 'left']]
        right_verts = [['corner', 'bottom', 'right']]
        for i in range(1, self.num_slats):
            left_verts.append(['left', i])
            right_verts.append(['right', i])

        left_verts.extend([['corner', 'top', 'left'],
                           ['top', 1],
                           ['bottom', 1]])
        right_verts.extend([['corner', 'top', 'right'],
                            ['top', self.num_slats - 1],
                            ['bottom', self.num_slats - 1]])
        self.add_face(0, list(reversed(left_verts)))
        self.add_face(self.num_slats - 1, right_verts)

    def color_pattern1(self):
        for face in self.faces:
            self.color_face(face, 1)

    def color_pattern2(self):
        for face in self.faces:
            if face % 2 == 1:
                self.color_face(face, 1)
