import bmesh


class BlenderAdaptor:
    def __init__(self, **kwargs):
        self.bm = None

    def create_empty_mesh(self):
        self.bm = bmesh.new()

    def initialize_colors(self):
        pass

    def create_vert(self, coords):
        return self.bm.verts.new(coords)

    def create_face(self, verts):
        return self.bm.faces.new(verts)

    def color_face(self, face, color_index):
        face.material_index = color_index

    def finish_mesh(self):
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)

    def get_mesh(self):
        return self.bm
