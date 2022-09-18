# from core_tests_base import CoreTestsBase
import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')
sys.path.append(this_dir + '/../../demo')

from tessagon.adaptors.list_adaptor import ListAdaptor  # noqa: E402
from tessagon_common_demo import TessagonCommonDemo  # noqa: E402


class ListDemo(TessagonCommonDemo):
    def tessellate(self, f, tessagon_class, **kwargs):
        extra_args = {'function': f,
                      'adaptor_class': ListAdaptor}
        tessagon = tessagon_class(**{**kwargs, **extra_args})
        return tessagon.create_mesh()

    def main(self):
        return self.create_objects()


class TestDemo:

    def test_demo_works(self):
        list_demo = ListDemo()
        meshes = list_demo.main()
        assert len(meshes) == 24
