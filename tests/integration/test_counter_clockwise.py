# from core_tests_base import CoreTestsBase
import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.adaptors.list_adaptor import ListAdaptor  # noqa: E402
from tessagon.core.tessagon_discovery import TessagonDiscovery  # noqa: E402
from tessagon.core import class_name_to_method_name  # noqa: E402

find_all = TessagonDiscovery()
test_class_names = find_all.names


class CounterClockwiseTester():
    # Test (in the plane) if generated faces are all ordered
    # in a counter-clockwise manner:
    # https://en.wikipedia.org/wiki/Curve_orientation

    TOLERANCE = 0.0000001

    def __init__(self, tessagon_class):
        self.tessagon_class = tessagon_class
        self.mesh = None

    def run(self):
        self.create_mesh()
        self.test_faces()

    def create_mesh(self):
        kwargs = {'simple_2d': True,
                  'adaptor_class': ListAdaptor,
                  'u_range': [0.0, 1.0],
                  'v_range': [0.0, 1.0],
                  'u_num': 6,
                  'v_num': 6,
                  'u_cyclic': False,
                  'v_cyclic': False}
        tessagon = self.tessagon_class(**kwargs)
        self.mesh = tessagon.create_mesh()

    def test_faces(self):
        clockwise = 0
        counter_clockwise = 0
        for face in self.mesh['face_list']:
            if self.test_face(face):
                counter_clockwise += 1
            else:
                clockwise += 1
        assert clockwise == 0, \
            "{} faces passed, {} failed".format(counter_clockwise, clockwise)

    def vert_face_index_to_vert(self, face, vert_face_index):
        vert_index = face[vert_face_index]
        return self.mesh['vert_list'][vert_index]

    def test_face(self, face):
        vert_face_index = self.vert_face_index_on_convex_hull(face)
        vert = self.vert_face_index_to_vert(face, vert_face_index)
        prev_vert = \
            self.vert_face_index_to_vert(face,
                                         (vert_face_index - 1) % len(face))
        next_vert = \
            self.vert_face_index_to_vert(face,
                                         (vert_face_index + 1) % len(face))

        return (self.cross_determinant(prev_vert, vert, next_vert) > 0)

    def vert_face_index_on_convex_hull(self, face):
        min_y_index = None
        vert = None
        for i in range(len(face)):
            vert_index = face[i]
            this_vert = self.mesh['vert_list'][vert_index]
            if min_y_index is None:
                min_y_index = i
                vert = this_vert
            else:
                if this_vert[1] <= vert[1] + self.TOLERANCE:
                    if this_vert[1] < vert[1] - self.TOLERANCE:
                        min_y_index = i
                        vert = this_vert
                    elif this_vert[0] > vert[0]:
                        # Treat the y as if they are equal
                        min_y_index = i
                        vert = this_vert

        return min_y_index

    def cross_determinant(self, prev_vert, vert, next_vert):
        return ((vert[0] * next_vert[1] +
                 prev_vert[0] * vert[1] +
                 prev_vert[1] * next_vert[0]) -
                (prev_vert[1] * vert[0] +
                 vert[1] * next_vert[0] +
                 prev_vert[0] * next_vert[1]))


class TestCounterClockwise:
    # Each edge should have exactly two neighboring faces
    pass


def make_test_method(tessagon_class_name):
    tessagon_class = TessagonDiscovery.get_class(tessagon_class_name)
    def make_and_test_tessagon(self):
        CounterClockwiseTester(tessagon_class).run()
    return make_and_test_tessagon


for tessagon_class_name in test_class_names:
    name = class_name_to_method_name(tessagon_class_name,
                                     prefix='test_counter_clockwise_')

    setattr(TestCounterClockwise, name, make_test_method(tessagon_class_name))
