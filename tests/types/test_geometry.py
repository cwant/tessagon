import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')
sys.path.append(this_dir + '/../core')

from core_tests_base import CoreTestsBase  # noqa: E402
from tessagon.core import class_to_method_name  # noqa: E402
from tessagon.core.tessagon_discovery import TessagonDiscovery  # noqa: E402
from tessagon.adaptors.list_adaptor import ListAdaptor  # noqa: E402


class TestGeometry(CoreTestsBase):
    pass


# We dynamically add methods to the test class (a bit janky).
# Sides of regular and archimedean should be the same for all
# for 2D undistorted mesh.
find_all = TessagonDiscovery()
regular = find_all.with_classification('regular')
archimedean = find_all.with_classification('archimedean')
tessagons = (regular + archimedean).to_list()

for tessagon_class in tessagons:
    def side_lengths_test(self):
        # This is the test method, renamed and added to class down below
        TOLERANCE = 0.000001

        tessagon = tessagon_class(simple_2d=True,
                                  u_num=3,
                                  v_num=3,
                                  u_range=[0.0, 1.0],
                                  v_range=[0.0, 1.0],
                                  u_cyclic=False,
                                  v_cyclic=False,
                                  adaptor_class=ListAdaptor)
        mesh = tessagon.create_mesh()
        name = tessagon_class.__name__
        # testing square of length is sufficient
        common_length_sq = None
        edge_count = 0
        for face in mesh['face_list']:
            verts = [mesh['vert_list'][i] for i in face]
            for i in range(len(face)):
                edge_count += 1
                j = (i + 1) % len(face)
                verti = verts[i]
                vertj = verts[j]
                length_sq = \
                    (verti[0] - vertj[0]) ** 2 + (verti[1] - vertj[1]) ** 2
                if not common_length_sq:
                    common_length_sq = length_sq
                    next
                assert abs(length_sq - common_length_sq) < TOLERANCE, \
                    '{} has bad length {} {}'.format(name, face,
                                                     edge_count)

    # Now add this method to test class with a name like
    # 'test_side_length_dodeca_tri_tessagon', for example
    setattr(TestGeometry,
            class_to_method_name(tessagon_class, 'test_side_length_'),
            side_lengths_test)
