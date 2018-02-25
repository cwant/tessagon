import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../../..')


class CoreTestsBase:
    pass


class FakeTessagon:
    def __init__(self):
        self.mesh_adaptor = FakeAdaptor()

    def f(self, u, v):
        return [u, u*v, v]


class FakeAdaptor:
    def __init__(self):
        self.verts = []
        self.faces = []

    def create_vert(self, coords):
        self.verts.append(coords)
        return coords
