import pytest
from core_tests_base import CoreTestsBase
from tessagon.core.abstract_tile import AbstractTile

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
      tile = AbstractTile(tessagon)
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

class FakeTessagon:
  def f(self, u, v):
    return [u, u*v, v]
