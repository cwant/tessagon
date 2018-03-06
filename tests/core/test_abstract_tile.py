import pytest
from core_tests_base import CoreTestsBase, FakeTessagon
from tessagon.core.abstract_tile import AbstractTile

# Testing ValueBlend too ...


class TestAbstractTile(CoreTestsBase):
    def test_u_range_v_range_params(self):
        tessagon = FakeTessagon()
        tile = AbstractTile(tessagon, u_range=[0.5, 1.0], v_range=[2.5, 4.0])
        assert (tile.corners == [[0.5, 2.5],
                                 [1, 2.5],
                                 [0.5, 4.0],
                                 [1.0, 4.0]])

    def test_corner_params(self):
        tessagon = FakeTessagon()
        tile = AbstractTile(tessagon, corners=[[0.5, 2.5],
                                               [1, 2.5],
                                               [0.5, 4.0],
                                               [1.0, 4.0]])
        assert (tile.corners == [[0.5, 2.5],
                                 [1, 2.5],
                                 [0.5, 4.0],
                                 [1.0, 4.0]])

    def test_that_it_fails_on_undefined_domain(self):
        tessagon = FakeTessagon()
        # No u_range, v_range, corner options passed
        with pytest.raises(ValueError) as exception_info:
            AbstractTile(tessagon)
        assert "Must set either option 'corners' or "\
            "options 'u_range' and 'v_range'" in str(exception_info.value)

    def test_neighbors(self):
        tessagon = FakeTessagon()
        tile = AbstractTile(tessagon, u_range=[0.5, 1.0], v_range=[2.5, 4.0])
        tiles = []
        for i in range(5):
            tiles.append(AbstractTile(tessagon, u_range=[0.5, 1.0],
                                      v_range=[2.5, 4.0]))
        tile.set_neighbors(top=tiles[0],
                           bottom=tiles[1],
                           right=tiles[2],
                           left=tiles[3])
        tiles[3].set_neighbors(top=tiles[4])

        assert tile.get_neighbor_tile(['left']) == tiles[3]
        assert tile.get_neighbor_tile(['right']) == tiles[2]
        assert tile.get_neighbor_tile(['top']) == tiles[0]
        assert tile.get_neighbor_tile(['bottom']) == tiles[1]
        assert tile.get_neighbor_tile(['left', 'top']) == tiles[4]

    def test_blend_when_initialized_with_ranges(self):
        tessagon = FakeTessagon()
        tile = AbstractTile(tessagon, u_range=[0.5, 1.0], v_range=[2.5, 4.5])

        assert tile.blend(0, 0) == [0.5, 2.5]
        assert tile.blend(1, 0) == [1.0, 2.5]
        assert tile.blend(0, 1) == [0.5, 4.5]
        assert tile.blend(1, 1) == [1.0, 4.5]
        assert tile.blend(0.5, 0.25) == [0.75, 3.0]
        assert tile.blend(0.75, 0.5) == [0.875, 3.5]

    def test_blend_when_initialized_with_corners(self):
        tessagon = FakeTessagon()
        tile = AbstractTile(tessagon, corners=[[0.5, 2.5],
                                               [1.5, 4.5],
                                               [1.5, 4.5],
                                               [2.5, 6.5]])

        assert tile.blend(0, 0) == [0.5, 2.5]
        assert tile.blend(1, 0) == [1.5, 4.5]
        assert tile.blend(0, 1) == [1.5, 4.5]
        assert tile.blend(1, 1) == [2.5, 6.5]
        assert tile.blend(0.5, 0.5) == [1.5, 4.5]
