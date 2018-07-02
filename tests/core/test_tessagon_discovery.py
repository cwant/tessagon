from core_tests_base import CoreTestsBase
from tessagon.core.tessagon_discovery import TessagonDiscovery
from tessagon.types.hex_tessagon import HexTessagon
from tessagon.types.tri_tessagon import TriTessagon
from tessagon.types.square_tessagon import SquareTessagon


class TestTessagonDiscovery(CoreTestsBase):
    def test_find_regular(self):
        all = TessagonDiscovery()
        regular = all.with_classification('regular')
        assert set(regular.to_list()) == set([HexTessagon,
                                              TriTessagon,
                                              SquareTessagon])
        assert regular.count() == 3

    def test_inverse(self):
        all = TessagonDiscovery()
        regular = all.with_classification('regular')
        inverse = regular.inverse()

        all_count = all.count()
        assert all_count >= 23
        regular_count = regular.count()
        assert regular_count == 3
        assert inverse.count() + regular_count == all_count

        assert set(regular.to_list()) | set(inverse.to_list()) == \
            set(all.to_list())

    def test_addition(self):
        all = TessagonDiscovery()
        regular = all.with_classification('regular')
        inverse = regular.inverse()

        assert set((regular + inverse).to_list()) == set(all.to_list())

    def test_subtraction(self):
        all = TessagonDiscovery()
        regular = all.with_classification('regular')
        inverse = regular.inverse()

        assert set((all - regular).to_list()) == set(inverse.to_list())
        assert (all - all).to_list() == []

    def test_with_color_pattern(self):
        color = TessagonDiscovery().with_color_patterns()
        non_color = color.inverse()
        for tessagon in color.to_list():
            assert tessagon.metadata.num_color_patterns() > 0
        for tessagon in non_color.to_list():
            assert tessagon.metadata.num_color_patterns() == 0
