from tessagon.core.abstract_tile import AbstractTile
from tessagon.core.tile_boundary import \
    TileBoundary, SharedVert, SharedFace


class Tile(AbstractTile):
    TOLERANCE = 0.0000001
    rotate = None

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)

        self.unit_mesh_maker = tessagon.unit_mesh_maker

        self.verts = self.init_verts()
        self.faces = self.init_faces()
        self.color_pattern = kwargs.get('color_pattern') or None
        if self.faces and self.color_pattern:
            self.face_paths = self.all_face_paths()
        self.init_boundary()

    def init_boundary(self):
        # Subclass might override (e.g., SlatsTessagon has dynamic boundary)

        self.boundary = TileBoundary(self, **self.__class__.BOUNDARY,
                                     rotate=self.rotate)

    def validate(self):
        self.tessagon.validate_tile(self)
        self.boundary.validate()

    @property
    def uv_ratio(self):
        return self.__class__.uv_ratio

    def is_boundary(self, u_or_v):
        if abs(u_or_v) < self.TOLERANCE:
            return True
        if abs(u_or_v - 1) < self.TOLERANCE:
            return True
        return False

    def add_vert(self, index_keys, ratio_u, ratio_v, **kwargs):
        vert = self._get_vert(index_keys)
        if vert is None:
            uv = self.blend(ratio_u, ratio_v, rotate=self.rotate)

            if self.is_boundary(ratio_u):
                kwargs['u_boundary'] = True
            if self.is_boundary(ratio_v):
                kwargs['v_boundary'] = True

            shared_vert = \
                self.get_shared_vert(index_keys, uv, **kwargs)
            if shared_vert:
                # We calculate this later when we have more information
                return

            vert = self.make_vert(index_keys, uv)

            if 'vert_type' in kwargs:
                if not kwargs['vert_type'] in self.tessagon.vert_types:
                    self.tessagon.vert_types[kwargs['vert_type']] = []
                self.tessagon.vert_types[kwargs['vert_type']].append(vert)

        return vert

    def make_vert(self, index_keys, uv):
        vert = self.unit_mesh_maker.create_vert(uv)
        self._set_vert(index_keys, vert)

        return vert

    def get_shared_vert(self, index_keys, uv, **kwargs):
        for side in TileBoundary.SIDES:
            arg = '{}_boundary'.format(side)
            if arg in kwargs:
                feature = kwargs[arg]
                return SharedVert(self, side, feature, index_keys,
                                  uv, **kwargs)

        return None

    def calculate_shared_verts(self):
        for shared_vert in self.boundary.get_shared_verts():
            shared_vert.calculate_vert()

    def set_equivalent_vert(self, index_keys, vert, **kwargs):
        # On boundary, the vert on a neighbor is equivalent to this vert
        if vert is None:
            return None

        self._set_vert(index_keys, vert)

    def add_face(self, index_keys, vert_index_keys_list, **kwargs):
        # Use the UVMeshMaker to create a face.

        # Does it exist already?
        face = self._get_face(index_keys)

        if face is None:
            shared_face = \
                self.get_shared_face(index_keys,
                                     vert_index_keys_list,
                                     **kwargs)

            if shared_face:
                # We calculate this later when we have more information
                return None

            verts = self._get_verts_from_list(vert_index_keys_list)
            if verts is not None:
                face = \
                    self.make_face(index_keys, verts, **kwargs)

        return face

    def make_face(self, index_keys, verts, **kwargs):
        face = self.unit_mesh_maker.create_face(verts, **kwargs)
        self._set_face(index_keys, face)

        return face

    def get_shared_face(self, index_keys, vert_index_keys_list,
                        **kwargs):
        shared_faces = []
        vert_index_buffer = []
        args = kwargs.copy()
        for key in vert_index_keys_list:
            vert_index_buffer.append(key)
            if type(key) == list and key[0] == ['boundary']:
                side = key[1]
                feature = key[2]
                if len(shared_faces) > 0:
                    args['indirect'] = True
                shared_faces.append(SharedFace(self, side, feature, index_keys,
                                               vert_index_buffer, **args))
                vert_index_buffer = []

        for i in range(len(shared_faces)):
            if len(shared_faces) < 2:
                break
            i_next = (i + 1) % len(shared_faces)
            shared_faces[i].next_shared_face = shared_faces[i_next]

        if len(shared_faces) > 0:
            return shared_faces[0]

        return None

    def calculate_shared_faces(self):
        for shared_face in self.boundary.get_shared_faces():
            shared_face.calculate_face()

    def num_color_patterns(self):
        return self.tessagon.num_color_patterns()

    def calculate_colors(self):
        if self.color_pattern > self.num_color_patterns():
            raise ValueError("color_pattern must be below %d" %
                             (self.num_color_patterns()))
        method_name = "color_pattern%d" % (self.color_pattern)
        method = getattr(self, method_name)
        if not callable(method):
            raise ValueError("%s is not a callable color pattern" %
                             (method_name))
        method()

    def color_face(self, index_keys, color_index):
        face = self._get_face(index_keys)
        if face is None:
            return
        self.unit_mesh_maker.color_face(face, color_index)

    def set_equivalent_face(self, index_keys, face, **kwargs):
        # On boundary, the face on a neighbor is equivalent to this face
        # This is usually only called indirectly via add_face, but check out
        # PythagoreanTile for an example of direct usage
        self._set_face(index_keys, face)

    def all_face_paths(self, faces=None, base_path=None):
        if faces is None:
            faces = self.faces
        if base_path is None:
            base_path = []

        paths = []
        for index in faces:
            new_base_path = base_path + [index]
            if type(faces[index]) is dict:
                paths += self.all_face_paths(faces[index], new_base_path)
            else:
                paths.append(new_base_path)
        return paths

    def color_paths(self, paths, color, color_other=None):
        for path in self.face_paths:
            if path in paths:
                self.color_face(path, color)
            elif color_other:
                self.color_face(path, color_other)

    def color_paths_hash(self, hash, color_other=None):
        for path in self.face_paths:
            for color in hash:
                done = False
                if path in hash[color]:
                    self.color_face(path, color)
                    done = True
                    break
            if color_other and not done:
                self.color_face(path, color_other)

    # Below are protected

    def _get_vert(self, index_keys):
        return self._get_nested_list_value(self.verts, index_keys)

    def _set_vert(self, index_keys, value):
        self._set_nested_list_value(self.verts, index_keys, value)

    def _get_face(self, index_keys):
        return self._get_nested_list_value(self.faces, index_keys)

    def _set_face(self, index_keys, value):
        self._set_nested_list_value(self.faces, index_keys, value)

    def _get_neighbor_vert(self, neighbor_keys, index_keys):
        # See comment about neighbors in AbstractTile
        tile = self.get_neighbor_tile(neighbor_keys)
        if tile is None:
            return None
        return tile._get_vert(self._index_path(index_keys, neighbor_keys))

    def _get_verts_from_list(self, vert_index_keys_list):
        verts = []
        for vert_index_keys in vert_index_keys_list:
            if isinstance(vert_index_keys, list) \
               and isinstance(vert_index_keys[0], list):
                vert = self._get_neighbor_vert(vert_index_keys[0],
                                               vert_index_keys[1])
            else:
                vert = self._get_vert(vert_index_keys)

            if vert is None:
                return None
            verts.append(vert)

        return verts
