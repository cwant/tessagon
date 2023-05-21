from tessagon.core.tile import Tile
from tessagon.core.tessagon import Tessagon
from tessagon.core.tessagon_metadata import TessagonMetadata
from tessagon.core.tile_utils import top_tile, bottom_tile, \
    left_tile, right_tile, left_bottom_tile, left_top_tile, \
    right_bottom_tile, right_top_tile

metadata = TessagonMetadata(name='Pythagorean',
                            num_color_patterns=1,
                            classification='non_edge',
                            shapes=['squares'],
                            sides=[4],
                            uv_ratio=1.0)


class PythagoreanTile(Tile):
    # 29 verts in six rows, six columns
    # 12 faces (2 sets shared with neighbors)
    #
    #    o...o-o-o-o  row6  o.1.o-o-o-o
    #    |...|.|...|        |...|2|...|
    #    o-o-o-o...o  row5  o-o-o-o.3.o
    # ^  |.|...|...|        |4|...|...|
    # |  o-o...o-o-o  row4  o-o.5.o-o-o
    # |  ..|...|.|..        ..|...|7|..
    # |  ..o-o-o-o..  row3  6.o-o-o-o.8
    #    ..|.|...|..        ..|9|...|..
    # V  o-o-o...o-o  row2  o-o-o10.o-o
    #    |...|...|.|        |...|...12|
    #    o...o-o-o-o  row1  o11.o-o-o-o
    #
    #    1 2 3 4 5 6 <-cols
    #
    #      U ------>

    def init_verts(self):
        # [col, row], these read like columns
        return {1: {1: None, 2: None, 4: None, 5: None, 6: None},
                2: {2: None, 3: None, 4: None, 5: None},
                3: {1: None, 2: None, 3: None, 5: None, 6: None},
                4: {1: None, 3: None, 4: None, 5: None, 6: None},
                5: {1: None, 2: None, 3: None, 4: None, 6: None},
                6: {1: None, 2: None, 4: None, 5: None, 6: None}}

    def calculate_verts(self):
        c = {1: 0.0,
             2: 1/5.0,
             3: 2/5.0,
             4: 3/5.0,
             5: 4/5.0,
             6: 1.0}
        for col in self.verts.keys():
            for row in self.verts[col].keys():
                # Some verts only get created if neighbors exist
                if col == 1:
                    if not self.get_neighbor_tile(['left']):
                        if row == 6 and not self.get_neighbor_tile(['top']):
                            continue
                        if not self.get_neighbor_tile(['bottom']):
                            if row == 1 or row == 2:
                                continue

                vert = self.add_vert([col, row], c[col], c[row])
                if col == 1:
                    self.set_equivalent_vert(*left_tile([6, row]), vert)
                    if row == 6:
                        self.set_equivalent_vert(*left_top_tile([6, 1]), vert)
                    elif row == 1:
                        self.set_equivalent_vert(*left_bottom_tile([6, 6]),
                                                 vert)
                elif col == 6:
                    self.set_equivalent_vert(*right_tile([1, row]), vert)
                    if row == 6:
                        self.set_equivalent_vert(*right_top_tile([1, 1]),
                                                 vert)
                    elif row == 1:
                        self.set_equivalent_vert(*right_bottom_tile([1, 6]),
                                                 vert)
                if row == 6:
                    self.set_equivalent_vert(*top_tile([col, 1]), vert)
                elif row == 1:
                    self.set_equivalent_vert(*bottom_tile([col, 6]), vert)

    def init_faces(self):
        return {1: None, 2: None, 3: None, 4: None, 5: None, 6: None,
                7: None, 8: None, 9: None, 10: None, 11: None, 12: None}

    def calculate_faces(self):
        face = self.add_face(1, [[1, 6],
                                 [1, 5],
                                 [2, 5],
                                 [3, 5],
                                 [3, 6],
                                 top_tile([3, 2]),
                                 top_tile([2, 2]),
                                 top_tile([1, 2])])
        self.set_equivalent_face(*top_tile(11), face)

        self.add_face(2, [[3, 6],
                          [4, 6],
                          [4, 5],
                          [3, 5]])

        self.add_face(3, [[4, 6],
                          [5, 6],
                          [6, 6],
                          [6, 5],
                          [6, 4],
                          [5, 4],
                          [4, 4],
                          [4, 5]])

        self.add_face(4, [[1, 5],
                          [2, 5],
                          [2, 4],
                          [1, 4]])

        self.add_face(5, [[2, 5],
                          [3, 5],
                          [4, 5],
                          [4, 4],
                          [4, 3],
                          [3, 3],
                          [2, 3],
                          [2, 4]])

        face = self.add_face(6, [[1, 4],
                                 [2, 4],
                                 [2, 3],
                                 [2, 2],
                                 [1, 2],
                                 left_tile([5, 2]),
                                 left_tile([5, 3]),
                                 left_tile([5, 4])])
        self.set_equivalent_face(*left_tile(8), face)

        self.add_face(7, [[4, 4],
                          [5, 4],
                          [5, 3],
                          [4, 3]])

        face = self.add_face(8, [[6, 4],
                                 [5, 4],
                                 [5, 3],
                                 [5, 2],
                                 [6, 2],
                                 right_tile([2, 2]),
                                 right_tile([2, 3]),
                                 right_tile([2, 4])])
        self.set_equivalent_face(*right_tile(6), face)

        self.add_face(9, [[2, 3],
                          [3, 3],
                          [3, 2],
                          [2, 2]])

        self.add_face(10, [[3, 3],
                           [4, 3],
                           [5, 3],
                           [5, 2],
                           [5, 1],
                           [4, 1],
                           [3, 1],
                           [3, 2]])

        face = self.add_face(11, [[1, 1],
                                  [1, 2],
                                  [2, 2],
                                  [3, 2],
                                  [3, 1],
                                  bottom_tile([3, 5]),
                                  bottom_tile([2, 5]),
                                  bottom_tile([1, 5])])
        self.set_equivalent_face(*bottom_tile(1), face)

        self.add_face(12, [[5, 2],
                           [6, 2],
                           [6, 1],
                           [5, 1]])

    def color_pattern1(self):
        # Color the big ones
        self.color_face([1], 1)
        self.color_face([3], 1)
        self.color_face([5], 1)
        self.color_face([6], 1)
        self.color_face([8], 1)
        self.color_face([10], 1)
        self.color_face([11], 1)


class PythagoreanTessagon(Tessagon):
    tile_class = PythagoreanTile
    metadata = metadata
