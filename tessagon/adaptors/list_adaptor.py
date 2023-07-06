from tessagon.adaptors.base_adaptor import BaseAdaptor


class ListAdaptor(BaseAdaptor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.vert_list = None
        self.face_list = None
        self.color_list = None
        self.face_types = None

    def create_empty_mesh(self):
        self.vert_list = []
        self.face_list = []
        self.color_list = []

        # Hash of lists
        self.face_types = {}

    def initialize_colors(self):
        self.color_list = [0]*len(self.face_list)

    def create_vert(self, coords):
        self.vert_list.append(coords)
        return (len(self.vert_list) - 1)

    def create_face(self, verts, **kwargs):
        self.face_list.append(verts)
        index = len(self.face_list) - 1
        face_type = kwargs.get('face_type')
        if face_type:
            if face_type not in self.face_types:
                self.face_types[face_type] = []
            self.face_types[face_type].append(index)
        return (index)

    def color_face(self, face, color_index):
        self.color_list[face] = color_index

    def finish_mesh(self):
        if not self.face_order:
            return

        # Reorder them
        new_faces = []
        new_colors = []
        new_face_types = {}

        ordered_indices = []
        index = 0
        for face_type in self.face_order:
            ordered_indices.extend(self.face_types[face_type])

            num_faces = len(self.face_types[face_type])
            new_face_types[face_type] = list(range(index, index + num_faces))
            index = index + num_faces

        for i in ordered_indices:
            new_faces.append(self.face_list[i])
            if len(self.color_list) > 0:
                new_colors.append(self.color_list[i])

        self.face_list = new_faces
        self.color_list = new_colors
        self.face_types = new_face_types

    def get_mesh(self):
        return {'vert_list': self.vert_list,
                'face_list': self.face_list,
                'color_list': self.color_list}
