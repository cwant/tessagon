# from core_tests_base import CoreTestsBase
import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.adaptors.list_adaptor import ListAdaptor  # noqa: E402
from tessagon.core.tessagon_discovery import TessagonDiscovery  # noqa: E402
from tessagon.misc.shapes import torus  # noqa: E402
from tessagon.core import class_to_method_name  # noqa: E402

find_all = TessagonDiscovery()
non_manifold = find_all.with_classification('non_manifold')
test_classes = (find_all - non_manifold).to_list()


class EdgeBuilder():
    def __init__(self, tessagon_class):
        self.tessagon_class = tessagon_class
        self.mesh = None

    def create_mesh(self):
        kwargs = {'function': torus,
                  'adaptor_class': ListAdaptor,
                  'u_range': [0.0, 1.0],
                  'v_range': [0.0, 1.0],
                  'u_num': 6,
                  'v_num': 6,
                  'u_cyclic': True,
                  'v_cyclic': True}
        tessagon = tessagon_class(**kwargs)
        self.mesh = tessagon.create_mesh()

    def create_edge_faces(self):
        # Each key represents an edge
        # The values are a list of faces bordering that edge
        edges_hash = {}
        for face in self.mesh['face_list']:
            for i in range(len(face)):
                j = (i + 1) % len(face)
                v1 = min(face[i], face[j])
                v2 = max(face[i], face[j])
                key = "{}-{}".format(v1, v2)
                if key not in edges_hash:
                    edges_hash[key] = []
                edges_hash[key].append(face)

        return edges_hash

    def run(self):
        self.create_mesh()
        return self.create_edge_faces()


class TestManifold:
    # Each edge should have exactly two neighboring faces
    pass


def make_test_method(tessagon_class):
    def make_and_test_tessagon(self):
        edge_faces = EdgeBuilder(tessagon_class).run()
        assert len(edge_faces) > 0
        for edge in edge_faces:
            faces = edge_faces[edge]
            assert len(faces) == 2
    return make_and_test_tessagon


for tessagon_class in test_classes:
    name = class_to_method_name(tessagon_class,
                                prefix='test_manifold_')

    setattr(TestManifold, name, make_test_method(tessagon_class))
