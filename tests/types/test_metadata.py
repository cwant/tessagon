import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')
sys.path.append(this_dir + '/../core')

from core_tests_base import CoreTestsBase  # noqa: E402
from tessagon.core import class_to_method_name  # noqa: E402
from tessagon.core.tessagon_discovery import TessagonDiscovery  # noqa: E402
from tessagon.adaptors.list_adaptor import ListAdaptor  # noqa: E402


class TestMetadata(CoreTestsBase):
    pass


# We dynamically add methods to the test class (a bit janky).
tessagons = TessagonDiscovery().to_list()
for tessagon_class in tessagons:
    def metadata_test(self):
        tessagon = tessagon_class(simple_2d=True,
                                  u_num=1,
                                  v_num=1,
                                  u_range=[0.0, 1.0],
                                  v_range=[0.0, 1.0],
                                  adaptor_class=ListAdaptor)
        name = tessagon_class.__name__
        assert tessagon.metadata, '{} missing metadata'.format(name)
        assert tessagon.metadata.uv_ratio, \
            '{} missing uv_ratio'.format(name)

    setattr(TestMetadata,
            class_to_method_name(tessagon_class, 'test_metadata_'),
            metadata_test)
