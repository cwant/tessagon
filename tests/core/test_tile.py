from core_tests_base import CoreTestsBase, FakeTessagon, FakeTileSubClass


class TestTile(CoreTestsBase):
    # Note: these tests are highly dependent on the behavior of
    #   FakeTessagon and FakeUVMeshMaker

    def test_add_vert(self):
        tessagon = FakeTessagon()
        tile = FakeTileSubClass(tessagon, u_range=[0.5, 1.0],
                                v_range=[2.5, 3.0])
        tile.add_vert(0, 0.25, 0.75)
        assert tile.blend(0.25, 0.75) == [0.625, 2.875]

        # One vert added
        assert tile.verts[0] == [0.625, 2.875]
        assert tile.verts[1] is None
        assert tile.verts[2] is None
        assert tile.verts[3] is None
