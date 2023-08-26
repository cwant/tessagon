import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.core.tile import Tile  # noqa: E402


class CoreTestsBase:
    pass

# TODO: What follows is basically crap ...


class FakeUnitMeshMaker:
    def __init__(self):
        self.verts = []
        self.faces = []
        self.tile_generator = FakeTileGenerator()

    def create_vert(self, coords):
        self.verts.append(coords)
        return coords


class FakeTileGenerator:
    def __init__(self, **kwargs):
        self.u_cyclic = False
        self.v_cyclic = False

    def on_u_boundary(self, ratio_u, ratio_v):
        return False

    def on_v_boundary(self, ratio_u, ratio_v):
        return False


class FakeUVMeshMaker:
    def __init__(self):
        self.unit_mesh_maker = FakeUnitMeshMaker()


class FakeTileSubClass(Tile):
    BOUNDARY = {'top': ['face-1', 'split', 'face-2'],
                'left': ['face-1', 'vert-1', 'edge', 'vert-2', 'face-2'],
                'bottom': ['face-1', 'split', 'face-2'],
                'right': ['face-1', 'vert-1', 'edge', 'vert-2', 'face-2']}

    def init_verts(self):
        return {0: None,
                1: None,
                2: None,
                3: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None}


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
