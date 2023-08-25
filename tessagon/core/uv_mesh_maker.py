from tessagon.core.value_blend import ValueBlend
from tessagon.core.unit_mesh_maker import UnitMeshMaker
from tessagon.core.uv_post_process import UVPostProcess


class UVMeshMaker(ValueBlend):
    def __init__(self, tessagon, **kwargs):
        self.tessagon = tessagon

        # Corners is list of tuples:
        #   [bottom-left, bottom-right, top-left, top-right]
        self.corners = None
        self._init_corners(**kwargs)

        self.unit_mesh_maker = UnitMeshMaker(tessagon, **kwargs)
        self.post_process = UVPostProcess(**kwargs)

        self.verts = []

    @ property
    def color_pattern(self):
        return self.unit_mesh_maker.color_pattern

    @property
    def faces(self):
        return self.unit_mesh_maker.faces

    @property
    def color_faces(self):
        return self.unit_mesh_maker.color_faces

    @property
    def face_types(self):
        return self.unit_mesh_maker.face_types

    @property
    def vert_types(self):
        return self.unit_mesh_maker.vert_types

    @property
    def u_num(self):
        return self.unit_mesh_maker.u_num

    @property
    def v_num(self):
        return self.unit_mesh_maker.v_num

    @property
    def extra_parameters(self):
        return self.unit_mesh_maker.extra_parameters

    @property
    def uv_ratio(self):
        return self.tessagon.uv_ratio

    def create_uv_mesh(self):
        self.unit_mesh_maker.create_unit_mesh()
        self._create_verts()

        self.post_process.run(self)

    def _create_verts(self):
        for vert in self.unit_mesh_maker.verts:
            self.verts.append(self.blend(vert[0], vert[1]))

    def inspect(self):
        print("\n=== %s ===\n" % (self.__class__.__name__))
        for i in range(len(self.tiles)):
            self.tiles[i].inspect(tile_number=i)
