from math import sqrt
from core_tests_base import CoreTestsBase, FakeTessagon
from tessagon.core.parallelogram_tile_generator \
    import ParallelogramTileGenerator


class TestParallelogramTileGenerator(CoreTestsBase):
    def find_fingerprint(self, tiles, fingerprint):
        for tile in tiles:
            if tile.fingerprint == fingerprint:
                return tile
        return None

    def test_non_cyclic(self):
        tessagon = FakeTessagon()
        tile_generator = \
            ParallelogramTileGenerator(tessagon,
                                       u_range=[0.0, 1.0], v_range=[0.0, 1.0],
                                       u_num=1, v_num=1,
                                       parallelogram_vectors=[[3, 1], [1, 2]],
                                       u_cyclic=False, v_cyclic=False)
        tiles = tile_generator.create_tiles()
        assert len(tiles) == 2

        # noqa: E741
        A = [1/5, 2/5]
        B = [3/5, 1/5]
        C = [0, 1]
        D = [2/5, 4/5]
        E = [1, 0]
        F = [4/5, 3/5]

        first_tile = self.find_fingerprint(tiles, [1, 1])
        assert first_tile is not None
        assert first_tile.fingerprint == [1, 1]
        assert first_tile.right is not None
        assert first_tile.left is None
        assert first_tile.top is None
        assert first_tile.bottom is None
        self.compare_corners(first_tile, [A, B, C, D])

        second_tile = first_tile.right
        assert second_tile.fingerprint == [2, 1]
        assert second_tile.left is not None
        assert second_tile.left == first_tile
        assert second_tile.right is None
        assert second_tile.top is None
        assert second_tile.bottom is None
        self.compare_corners(second_tile, [B, E, D, F])

    def test_u_v_cyclic(self):
        tessagon = FakeTessagon()
        tile_generator = \
            ParallelogramTileGenerator(tessagon,
                                       u_range=[0.0, 1.0], v_range=[0.0, 1.0],
                                       u_num=1, v_num=1,
                                       parallelogram_vectors=[[3, 1], [1, 2]],
                                       u_cyclic=True, v_cyclic=True)
        tiles = tile_generator.create_tiles()
        assert len(tiles) == 5

        O = [0, 0]  # noqa: E741
        A = [1/5, 2/5]
        A2 = [1/5 + 1, 2/5]
        A3 = [1/5, 2/5 + 1]
        B = [3/5, 1/5]
        B2 = [3/5, 1/5 + 1]
        C = [0, 1]
        D = [2/5, 4/5]
        D2 = [2/5, 4/5 - 1]
        E = [1, 0]
        F = [4/5, 3/5]
        F2 = [4/5 - 1, 3/5]
        I = [1, 1]  # noqa: E741

        first_tile = self.find_fingerprint(tiles, [0, 0])
        assert first_tile.fingerprint == [0, 0]
        assert first_tile.right.fingerprint == [2, 2]
        assert first_tile.left.fingerprint == [2, 1]
        assert first_tile.top.fingerprint == [3, 2]
        assert first_tile.bottom.fingerprint == [1, 1]
        self.compare_corners(first_tile, [O, D2, F2, A])

        second_tile = first_tile.right
        assert second_tile.fingerprint == [2, 2]
        assert second_tile.right.fingerprint == [3, 2]
        assert second_tile.left.fingerprint == [0, 0]
        assert second_tile.top.fingerprint == [1, 1]
        assert second_tile.bottom.fingerprint == [2, 1]
        self.compare_corners(second_tile, [D, F, A3, B2])

        third_tile = second_tile.right
        assert third_tile.fingerprint == [3, 2]
        assert third_tile.right.fingerprint == [1, 1]
        assert third_tile.left.fingerprint == [2, 2]
        assert third_tile.top.fingerprint == [2, 1]
        assert third_tile.bottom.fingerprint == [0, 0]
        self.compare_corners(third_tile, [F, A2, B2, I])

        fourth_tile = second_tile.top
        assert fourth_tile.fingerprint == [1, 1]
        assert fourth_tile.right.fingerprint == [2, 1]
        assert fourth_tile.left.fingerprint == [3, 2]
        assert fourth_tile.top.fingerprint == [0, 0]
        assert fourth_tile.bottom.fingerprint == [2, 2]
        self.compare_corners(fourth_tile, [A, B, C, D])

        fifth_tile = fourth_tile.right
        assert fifth_tile.fingerprint == [2, 1]
        assert fifth_tile.right.fingerprint == [0, 0]
        assert fifth_tile.left.fingerprint == [1, 1]
        assert fifth_tile.top.fingerprint == [2, 2]
        assert fifth_tile.bottom.fingerprint == [3, 2]
        self.compare_corners(fifth_tile, [B, E, D, F])

    def compare_corners(self, tile, corners):
        for i in range(len(corners)):
            self.compare_points(tile.corners[i], corners[i])

    def compare_points(self, point1, point2):
        TOLERANCE = 0.00001

        assert sqrt((point1[0] - point2[0])**2 +
                    (point1[1] - point2[1])**2) < TOLERANCE
