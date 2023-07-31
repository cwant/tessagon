import random
from tessagon.core.uv_mesh_maker import UVMeshMaker
from tessagon.core.xyz_mesh_maker import XYZMeshMaker


class Tessagon:
    tile_classes = None
    metadata = None
    # The adaptor decides if it wants to honor this
    face_order = None

    def __init__(self, **kwargs):
        self._initialize_randomness(**kwargs)
        self.uv_mesh_maker = UVMeshMaker(self, **kwargs)
        self.xyz_mesh_maker = XYZMeshMaker(self, **kwargs)

    def create_mesh(self):
        return self.xyz_mesh_maker.create_mesh()

    # Note, would like these to be a class properties,
    # but the designers of Python flip-flop about
    # how to implement it.
    @classmethod
    def num_color_patterns(cls):
        if cls.metadata is None:
            return 0
        return cls.metadata.num_color_patterns

    @classmethod
    def num_extra_parameters(cls):
        if cls.metadata is None:
            return 0
        return len(cls.metadata.extra_parameters)

    @property
    def color_pattern(self):
        return self.uv_mesh_maker.color_pattern

    @property
    def extra_parameters(self):
        return self.uv_mesh_maker.extra_parameters

    @property
    def f(self):
        return self.xyz_mesh_maker.f

    @property
    def u_num(self):
        return self.uv_mesh_maker.u_num

    @property
    def v_num(self):
        return self.uv_mesh_maker.v_num

    @property
    def corners(self):
        return self.uv_mesh_maker.corners

    @property
    def metadata(self):
        return self.__class__.metadata

    @property
    def uv_ratio(self):
        return self.tile_classes[0].uv_ratio

    def get_tile_class(self, fingerprint):
        # Perhaps overridden in subclass ...
        return self.__class__.tile_classes[0]

    def validate_tile(self, tile):
        # Subclass might want to do tests
        pass

    def _initialize_randomness(self, **kwargs):
        seed = kwargs.get('random_seed', -1)
        if seed < 0:
            return

        random.seed(seed)
