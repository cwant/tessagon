from core_tests_base import CoreTestsBase, FakeTessagon, FakeTileSubClass


class TestTile(CoreTestsBase):
    # Note: these tests are highly dependent on the behavior of
    #   FakeTessagon and FakeAdaptor

    def test_add_vert(self):
        tessagon = FakeTessagon()
        tile = FakeTileSubClass(tessagon, u_range=[0.5, 1.0],
                                v_range=[2.5, 3.0])
        tile.add_vert(['top', 'left'], 0.25, 0.75)
        assert tile.blend(0.25, 0.75) == [0.625, 2.875]

        # One vert added
        assert tile.verts['top']['left'] == tile.f(0.625, 2.875)
        assert tile.verts['top']['right'] is None
        assert tile.verts['bottom']['left'] is None
        assert tile.verts['bottom']['right'] is None

    def test_add_vert_u_symmetric(self):
        tessagon = FakeTessagon()
        tile = FakeTileSubClass(tessagon, u_range=[0.5, 1.0],
                                v_range=[2.5, 3.0],
                                u_symmetric=True)
        tile.add_vert(['top', 'left'], 0.25, 0.75)
        # [0.75, 0.75] is reflection of [0.25, 0.75] in U direction
        assert tile.blend(0.75, 0.75) == [0.875, 2.875]

        # Two verts added
        assert tile.verts['top']['left'] == tile.f(0.625, 2.875)
        assert tile.verts['top']['right'] == tile.f(0.875, 2.875)
        assert tile.verts['bottom']['left'] is None
        assert tile.verts['bottom']['right'] is None

    def test_add_vert_v_symmetric(self):
        tessagon = FakeTessagon()
        tile = FakeTileSubClass(tessagon, u_range=[0.5, 1.0],
                                v_range=[2.5, 3.0],
                                v_symmetric=True)
        tile.add_vert(['top', 'left'], 0.25, 0.75)
        # [0.25, 0.25] is reflection of [0.25, 0.75] in V direction
        assert tile.blend(0.25, 0.25) == [0.625, 2.625]

        # Two verts added
        assert tile.verts['top']['left'] == tile.f(0.625, 2.875)
        assert tile.verts['top']['right'] is None
        assert tile.verts['bottom']['left'] == tile.f(0.625, 2.625)
        assert tile.verts['bottom']['right'] is None

    def test_add_vert_u_v_symmetric(self):
        tessagon = FakeTessagon()
        tile = FakeTileSubClass(tessagon, u_range=[0.5, 1.0],
                                v_range=[2.5, 3.0],
                                u_symmetric=True, v_symmetric=True)
        tile.add_vert(['top', 'left'], 0.25, 0.75)
        # [0.75, 0.25] is reflection of [0.25, 0.75] in U and V directions
        assert tile.blend(0.75, 0.25) == [0.875, 2.625]

        # Four verts added
        assert tile.verts['top']['left'] == tile.f(0.625, 2.875)
        assert tile.verts['top']['right'] == tile.f(0.875, 2.875)
        assert tile.verts['bottom']['left'] == tile.f(0.625, 2.625)
        assert tile.verts['bottom']['right'] == tile.f(0.875, 2.625)
