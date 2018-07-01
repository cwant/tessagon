from tessagon.core.tessagon import Tessagon
from tessagon.core.tile import Tile
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Regular Triangles',
                            num_color_patterns=3,
                            classification='regular',
                            shapes=['triangles'],
                            sides=[3])


class TriTile(Tile):

    #  ^  0.|.1   This is the topology of the tile.
    #  |  |\|/|   (Not a Dead Kennedy's logo ...).
    #  |  |.2.|
    #  |  |/|\|
    #  V  3.|.4
    #
    #  U ----->

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = True
        self.v_symmetric = True

    def init_verts(self):
        return {'left': {'top': None, 'bottom': None},
                'middle': None,
                'right': {'top': None, 'bottom': None}}

    def init_faces(self):
        return {'left': {'top': None, 'middle': None, 'bottom': None},
                'right': {'top': None, 'middle': None, 'bottom': None}}

    def calculate_verts(self):
        # Four corners, via symmetry
        self.add_vert(['left', 'top'], 0, 1, corner=True)
        # The middle vert
        self.add_vert('middle', 0.5, 0.5)

    def calculate_faces(self):
        # Four corners, via symmetry
        self.add_face(['left', 'top'],
                      [['left', 'top'],
                       ['middle'],
                       # Vert on neighboring tile
                       [['top'], ['middle']]], v_boundary=True)
        # Two interior faces, via symmetry
        self.add_face(['left', 'middle'],
                      [['left', 'top'],
                       ['left', 'bottom'],
                       ['middle']])

    def color_pattern1(self):
        # two colors for triangles pointing in different directions
        self.color_face(['left', 'top'], 0)
        self.color_face(['right', 'top'], 1)
        self.color_face(['left', 'middle'], 1)
        self.color_face(['right', 'middle'], 0)
        self.color_face(['left', 'bottom'], 0)
        self.color_face(['right', 'bottom'], 1)

    def color_pattern2(self):
        # Two colors, this one is awesome, but complicated
        if not self.fingerprint:
            return
        if self.fingerprint[1] % 3 == 0:
            if self.fingerprint[0] % 3 == 0:
                self.color_0_0()
            elif self.fingerprint[0] % 3 == 1:
                self.color_0_1()
        elif self.fingerprint[1] % 3 == 1:
            if self.fingerprint[0] % 3 == 0:
                self.color_1_0()
            elif self.fingerprint[0] % 3 == 1:
                self.color_1_1()
            else:
                self.color_1_2()
        else:
            if self.fingerprint[0] % 3 == 0:
                self.color_2_0()
            elif self.fingerprint[0] % 3 == 1:
                self.color_2_1()
            else:
                self.color_2_2()

    def color_pattern3(self):
        if not self.fingerprint:
            return
        if self.fingerprint[1] % 3 == 2:
            self.color_paths([['left', 'middle'],
                              ['right', 'bottom']], 1, 0)
        elif self.fingerprint[1] % 3 == 1:
            self.color_paths([['right', 'top'],
                              ['right', 'bottom']], 1, 0)
        else:
            self.color_paths([['left', 'middle'],
                              ['right', 'top']], 1, 0)

    def color_0_0(self):
        self.color_paths([], 0, 1)

    def color_0_1(self):
        paths = [['left', 'top'],
                 ['left', 'bottom'],
                 ['right', 'middle']]
        self.color_paths(paths, 1, 0)

    def color_1_0(self):
        paths = [['left', 'top'],
                 ['left', 'bottom'],
                 ['right', 'bottom']]
        self.color_paths(paths, 1, 0)

    def color_1_1(self):
        paths = [['left', 'bottom'],
                 ['right', 'top'],
                 ['right', 'middle']]
        self.color_paths(paths, 1, 0)

    def color_1_2(self):
        paths = [['left', 'top'],
                 ['left', 'middle'],
                 ['right', 'middle']]
        self.color_paths(paths, 1, 0)

    def color_2_0(self):
        paths = [['left', 'top'],
                 ['left', 'bottom'],
                 ['right', 'top']]
        self.color_paths(paths, 1, 0)

    def color_2_1(self):
        paths = [['left', 'top'],
                 ['right', 'middle'],
                 ['right', 'bottom']]
        self.color_paths(paths, 1, 0)

    def color_2_2(self):
        paths = [['left', 'middle'],
                 ['left', 'bottom'],
                 ['right', 'middle']]
        self.color_paths(paths, 1, 0)


class TriTessagon(Tessagon):
    tile_class = TriTile
    metadata = metadata
