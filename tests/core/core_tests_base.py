import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.core.tile import Tile  # noqa: E402


class CoreTestsBase:
    pass


class FakeUnitMeshMaker:
    def __init__(self):
        self.verts = []
        self.faces = []

    def create_vert(self, coords):
        self.verts.append(coords)
        return coords


class FakeUVMeshMaker:
    def __init__(self):
        self.unit_mesh_maker = FakeUnitMeshMaker()


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


class FakeTessagon:
    tile_classes = [FakeTileSubClass]
    metadata = None

    def __init__(self):
        self.uv_mesh_maker = FakeUVMeshMaker()
        self.unit_mesh_maker = self.uv_mesh_maker.unit_mesh_maker
        self.extra_parameters = {}

    def f(self, u, v):
        return [u, u*v, v]

    def get_tile_class(self, fingerprint):
        return FakeTileSubClass

    def validate_tile(self, tile):
        pass
