import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')
sys.path.append(this_dir + '/../core')

from core_tests_base import CoreTestsBase  # noqa: E402
from tessagon.core import class_to_method_name  # noqa: E402
from tessagon.core.tessagon_discovery import TessagonDiscovery  # noqa: E402
from tessagon.adaptors.list_adaptor import ListAdaptor  # noqa: E402

test_classes = TessagonDiscovery().to_list()


def make_test_method(tessagon_class):

    def metadata_test(self):
        tessagon = tessagon_class(simple_2d=True,
                                  u_num=1,
                                  v_num=1,
                                  u_range=[0.0, 1.0],
                                  v_range=[0.0, 1.0],
                                  adaptor_class=ListAdaptor)
        name = tessagon_class.__name__
        assert tessagon.metadata, '{} missing metadata'.format(name)

        # TODO: This used to be in metadata, but is now stored in the class
        # Test it somewhere else?
        for tile_class in tessagon.tile_classes:
            # We want this less than one
            # ... to make the tiles more compatible/blendable/etc.
            assert tile_class.uv_ratio <= 1.0, \
                '{} invalid uv_ratio'.format(tile_class.__name__)
    return metadata_test


class TestMetadata(CoreTestsBase):
    pass


for tessagon_class in test_classes:
    setattr(TestMetadata,
            class_to_method_name(tessagon_class, 'test_metadata_'),
            make_test_method(tessagon_class))
