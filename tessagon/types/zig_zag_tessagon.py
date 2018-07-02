from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata

metadata = TessagonMetadata(name='Zig-Zag',
                            classification='non_edge',
                            shapes=['rectangles'],
                            sides=[4])


class ZigZagTile(Tile):
    # 25 verts in five rows, five columns
    # 10 faces (2 sets shared with neighbors)
    #
    #    o-o-o-o.o  row5  o-o-o-o.o
    # ^  |...|.|.|        |.1.|.|3|
    # |  o-o-o.o-o  row4  o-o-o2o-o
    # |  ..|.|.|..        4.|.|.|.6
    # |  o-o.o-o-o  row3  o-o5o-o-o
    #    |.|.|...|        |.|.|.8.|
    # V  o.o-o-o-o  row2  o7o-o-o-o
    #    |.|.|.|.|        |.|.9.|10
    #    o-o-o-o.o  row5  o-o-o-o.o
    #
    #    1 2 3 4 5 <-cols
    #
    #      U ------>

    def init_verts(self):
        # [col, row], these read like columns
        return {1: {1: None, 2: None, 3: None, 4: None, 5: None},
                2: {1: None, 2: None, 3: None, 4: None, 5: None},
                3: {1: None, 2: None, 3: None, 4: None, 5: None},
                4: {1: None, 2: None, 3: None, 4: None, 5: None},
                5: {1: None, 2: None, 3: None, 4: None, 5: None}}

    def init_faces(self):
        return {1: None, 2: None, 3: None, 4: None, 5: None, 6: None,
                7: None, 8: None, 9: None, 10: None}

    def calculate_verts(self):
        c = {1: 0.0,
             2: 1/4.0,
             3: 2/4.0,
             4: 3/4.0,
             5: 1.0}
        for col in self.verts.keys():
            for row in self.verts[col].keys():
                # Some verts only get created if neighbors exist
                if col == 5:
                    if not self.get_neighbor_tile(['right']):
                        if not self.get_neighbor_tile(['top']):
                            if row == 5:
                                continue
                            if row == 4:
                                continue
                        if not self.get_neighbor_tile(['bottom']):
                            if row == 1:
                                continue
                vert = self.add_vert([col, row], c[col], c[row])
                if col == 1:
                    self.set_equivalent_vert(['left'], [5, row], vert)
                    if row == 5:
                        self.set_equivalent_vert(['left', 'top'], [5, 1],
                                                 vert)
                    elif row == 1:
                        self.set_equivalent_vert(['left', 'bottom'], [5, 5],
                                                 vert)
                elif col == 5:
                    self.set_equivalent_vert(['right'], [1, row], vert)
                    if row == 5:
                        self.set_equivalent_vert(['right', 'top'], [1, 1],
                                                 vert)
                    elif row == 1:
                        self.set_equivalent_vert(['right', 'bottom'], [1, 5],
                                                 vert)
                if row == 5:
                    self.set_equivalent_vert(['top'], [col, 1], vert)
                elif row == 1:
                    self.set_equivalent_vert(['bottom'], [col, 5], vert)

    def calculate_faces(self):
        self.add_face(1, [[1, 5],
                          [1, 4],
                          [2, 4],
                          [3, 4],
                          [3, 5],
                          [2, 5]])

        self.add_face(2, [[3, 5],
                          [3, 4],
                          [3, 3],
                          [4, 3],
                          [4, 4],
                          [4, 5]])

        face = self.add_face(3, [[4, 5],
                                 [4, 4],
                                 [5, 4],
                                 [5, 5],
                                 [['top'], [5, 2]],
                                 [['top'], [4, 2]]])
        self.set_equivalent_face(['top'], 10, face)

        face = self.add_face(4, [[1, 3],
                                 [2, 3],
                                 [2, 4],
                                 [1, 4],
                                 [['left'], [4, 4]],
                                 [['left'], [4, 3]]])
        self.set_equivalent_face(['left'], 6, face)

        self.add_face(5, [[3, 2],
                          [3, 3],
                          [3, 4],
                          [2, 4],
                          [2, 3],
                          [2, 2]])

        face = self.add_face(6, [[5, 4],
                                 [4, 4],
                                 [4, 3],
                                 [5, 3],
                                 [['right'], [2, 3]],
                                 [['right'], [2, 4]]])
        self.set_equivalent_face(['right'], 4, face)

        self.add_face(7, [[2, 1],
                          [2, 2],
                          [2, 3],
                          [1, 3],
                          [1, 2],
                          [1, 1]])

        self.add_face(8, [[5, 2],
                          [5, 3],
                          [4, 3],
                          [3, 3],
                          [3, 2],
                          [4, 2]])

        self.add_face(9, [[4, 1],
                          [4, 2],
                          [3, 2],
                          [2, 2],
                          [2, 1],
                          [3, 1]])

        face = self.add_face(10, [[5, 1],
                                  [5, 2],
                                  [4, 2],
                                  [4, 1],
                                  [['bottom'], [4, 4]],
                                  [['bottom'], [5, 4]]])
        self.set_equivalent_face(['bottom'], 3, face)


class ZigZagTessagon(Tessagon):
    tile_class = ZigZagTile
    metadata = metadata
