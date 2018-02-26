from core_tests_base import CoreTestsBase, FakeTessagon, FakeTileSubClass
from tessagon.core.tile_generator import TileGenerator


class TestTileGenerator(CoreTestsBase):
    def test_non_cyclic(self):
        tessagon = FakeTessagon()
        tile_generator = TileGenerator(tessagon,
                                       u_range=[0.5, 1.0], v_range=[2.5, 4.0],
                                       u_num=2, v_num=3,
                                       u_cyclic=False, v_cyclic=False)
        tiles = tile_generator.initialize_tiles(FakeTileSubClass)
        assert len(tiles) == 2
        assert len(tiles[0]) == 3
        assert len(tiles[1]) == 3

        tile_generator.initialize_neighbors(tiles)
        assert(tiles[0][0].get_neighbor_tile(['left']) is None)
        assert(tiles[0][0].get_neighbor_tile(['bottom']) is None)
        assert(tiles[0][0].get_neighbor_tile(['right']) is tiles[1][0])
        assert(tiles[0][0].get_neighbor_tile(['top']) is tiles[0][1])

        assert(tiles[1][2].get_neighbor_tile(['left']) is tiles[0][2])
        assert(tiles[1][2].get_neighbor_tile(['bottom']) is tiles[1][1])
        assert(tiles[1][2].get_neighbor_tile(['right']) is None)
        assert(tiles[1][2].get_neighbor_tile(['top']) is None)

    def test_u_cyclic(self):
        tessagon = FakeTessagon()
        tile_generator = TileGenerator(tessagon,
                                       u_range=[0.5, 1.0], v_range=[2.5, 4.0],
                                       u_num=2, v_num=3,
                                       u_cyclic=True, v_cyclic=False)
        tiles = tile_generator.initialize_tiles(FakeTileSubClass)
        assert len(tiles) == 2
        assert len(tiles[0]) == 3
        assert len(tiles[1]) == 3

        tile_generator.initialize_neighbors(tiles)
        assert(tiles[0][0].get_neighbor_tile(['left']) is tiles[1][0])
        assert(tiles[0][0].get_neighbor_tile(['bottom']) is None)
        assert(tiles[0][0].get_neighbor_tile(['right']) is tiles[1][0])
        assert(tiles[0][0].get_neighbor_tile(['top']) is tiles[0][1])

        assert(tiles[1][2].get_neighbor_tile(['left']) is tiles[0][2])
        assert(tiles[1][2].get_neighbor_tile(['bottom']) is tiles[1][1])
        assert(tiles[1][2].get_neighbor_tile(['right']) is tiles[0][2])
        assert(tiles[1][2].get_neighbor_tile(['top']) is None)

    def test_v_cyclic(self):
        tessagon = FakeTessagon()
        tile_generator = TileGenerator(tessagon,
                                       u_range=[0.5, 1.0], v_range=[2.5, 4.0],
                                       u_num=2, v_num=3,
                                       u_cyclic=False, v_cyclic=True)
        tiles = tile_generator.initialize_tiles(FakeTileSubClass)
        assert len(tiles) == 2
        assert len(tiles[0]) == 3
        assert len(tiles[1]) == 3

        tile_generator.initialize_neighbors(tiles)
        assert(tiles[0][0].get_neighbor_tile(['left']) is None)
        assert(tiles[0][0].get_neighbor_tile(['bottom']) is tiles[0][2])
        assert(tiles[0][0].get_neighbor_tile(['right']) is tiles[1][0])
        assert(tiles[0][0].get_neighbor_tile(['top']) is tiles[0][1])

        assert(tiles[1][2].get_neighbor_tile(['left']) is tiles[0][2])
        assert(tiles[1][2].get_neighbor_tile(['bottom']) is tiles[1][1])
        assert(tiles[1][2].get_neighbor_tile(['right']) is None)
        assert(tiles[1][2].get_neighbor_tile(['top']) is tiles[1][0])

    def test_u_v_cyclic(self):
        tessagon = FakeTessagon()
        tile_generator = TileGenerator(tessagon,
                                       u_range=[0.5, 1.0], v_range=[2.5, 4.0],
                                       u_num=2, v_num=3,
                                       u_cyclic=True, v_cyclic=True)
        tiles = tile_generator.initialize_tiles(FakeTileSubClass)
        assert len(tiles) == 2
        assert len(tiles[0]) == 3
        assert len(tiles[1]) == 3

        tile_generator.initialize_neighbors(tiles)
        assert(tiles[0][0].get_neighbor_tile(['left']) is tiles[1][0])
        assert(tiles[0][0].get_neighbor_tile(['bottom']) is tiles[0][2])
        assert(tiles[0][0].get_neighbor_tile(['right']) is tiles[1][0])
        assert(tiles[0][0].get_neighbor_tile(['top']) is tiles[0][1])

        assert(tiles[1][2].get_neighbor_tile(['left']) is tiles[0][2])
        assert(tiles[1][2].get_neighbor_tile(['bottom']) is tiles[1][1])
        assert(tiles[1][2].get_neighbor_tile(['right']) is tiles[0][2])
        assert(tiles[1][2].get_neighbor_tile(['top']) is tiles[1][0])
