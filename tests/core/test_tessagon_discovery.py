import os
import glob
from core_tests_base import CoreTestsBase
from tessagon.core.tessagon_discovery import TessagonDiscovery
from tessagon.types.hex_tessagon import HexTessagon
from tessagon.types.tri_tessagon import TriTessagon
from tessagon.types.square_tessagon import SquareTessagon


class TestTessagonDiscovery(CoreTestsBase):
    def test_find_all(self):
        # We want to be able to find everything in the types folder
        find_all = TessagonDiscovery()
        wildcard = os.path.realpath(os.path.dirname(__file__) +
                                    '/../../tessagon/types/*_tessagon.py')
        all_type_py = glob.glob(wildcard)
        count_all_classes = len(find_all.to_list())
        assert count_all_classes > 20
        assert count_all_classes == len(all_type_py)

    def test_find_regular(self):
        find_all = TessagonDiscovery()
        regular = find_all.with_classification('regular')
        assert set(regular.to_list()) == set([HexTessagon,
                                              TriTessagon,
                                              SquareTessagon])
        assert regular.count() == 3

    def test_inverse(self):
        find_all = TessagonDiscovery()
        regular = find_all.with_classification('regular')
        inverse = regular.inverse()

        find_all_count = find_all.count()
        assert find_all_count >= 23
        regular_count = regular.count()
        assert regular_count == 3
        assert inverse.count() + regular_count == find_all_count

        assert set(regular.to_list()) | set(inverse.to_list()) == \
            set(find_all.to_list())

    def test_addition(self):
        find_all = TessagonDiscovery()
        regular = find_all.with_classification('regular')
        inverse = regular.inverse()

        assert set((regular + inverse).to_list()) == set(find_all.to_list())

    def test_subtraction(self):
        find_all = TessagonDiscovery()
        regular = find_all.with_classification('regular')
        inverse = regular.inverse()

        assert set((find_all - regular).to_list()) == set(inverse.to_list())
        assert (find_all - find_all).to_list() == []

    def test_with_color_pattern(self):
        color = TessagonDiscovery().with_color_patterns()
        non_color = color.inverse()
        for tessagon in color.to_list():
            assert tessagon.metadata.num_color_patterns > 0
        for tessagon in non_color.to_list():
            assert tessagon.metadata.num_color_patterns == 0
