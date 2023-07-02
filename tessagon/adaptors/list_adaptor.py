from tessagon.adaptors.base_adaptor import BaseAdaptor


class ListAdaptor(BaseAdaptor):

    def __init__(self, **kwargs):
        self.vert_list = None
        self.face_list = None
        self.color_list = None

    def create_empty_mesh(self):
        self.vert_list = []
        self.face_list = []
        self.color_list = []

    def initialize_colors(self):
        self.color_list = [0]*len(self.face_list)

    def create_vert(self, coords):
        self.vert_list.append(coords)
        return (len(self.vert_list) - 1)

    def create_face(self, verts):
        self.face_list.append(verts)
        return (len(self.face_list) - 1)

    def color_face(self, face, color_index):
        self.color_list[face] = color_index

    def finish_mesh(self):
        pass

    def get_mesh(self):
        return {'vert_list': self.vert_list,
                'face_list': self.face_list,
                'color_list': self.color_list}
