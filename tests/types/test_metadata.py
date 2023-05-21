from core_tests_base import CoreTestsBase
from tessagon.core.tessagon_discovery import TessagonDiscovery
from tessagon.adaptors.list_adaptor import ListAdaptor


class TestMetadata(CoreTestsBase):
    def test_metadata(self):
        tessagons = TessagonDiscovery().to_list()
        for tessagon_class in tessagons:
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
