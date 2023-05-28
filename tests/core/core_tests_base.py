import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.core.tile import Tile  # noqa: E402


class CoreTestsBase:
    pass


class FakeTessagon:
    def __init__(self):
        self.mesh_adaptor = FakeAdaptor()
        self.extra_parameters = {}

    def f(self, u, v):
        return [u, u*v, v]


class FakeAdaptor:
    def __init__(self):
        self.verts = []
        self.faces = []

    def create_vert(self, coords):
        self.verts.append(coords)
        return coords


class FakeTileSubClass(Tile):
    def init_verts(self):
        return {'top': {'left': None,
                        'right': None},
                'bottom': {'left': None,
                           'right': None}}

    def init_faces(self):
        return {'top': {'left': None,
                        'right': None},
                'bottom': {'left': None,
                           'right': None}}
