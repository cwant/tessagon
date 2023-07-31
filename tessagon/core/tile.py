from tessagon.core.abstract_tile import AbstractTile


class Tile(AbstractTile):

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)

        self.uv_mesh_maker = tessagon.uv_mesh_maker

        self.verts = self.init_verts()
        self.faces = self.init_faces()
        self.color_pattern = kwargs.get('color_pattern') or None
        if self.faces and self.color_pattern:
            self.face_paths = self.all_face_paths()

    @property
    def uv_ratio(self):
        return self.__class__.uv_ratio

    def validate(self):
        self.tessagon.validate_tile(self)

    def add_vert(self, index_keys, ratio_u, ratio_v, **kwargs):
        # Use the UVMeshMaker to create a vertex.
        # In reality, multiple vertices may get defined if symmetry is declared
        vert = self._get_vert(index_keys)
        if vert is None:
            uv = self.blend(ratio_u, ratio_v)
            vert = self.uv_mesh_maker.create_vert(uv)

            self._set_vert(index_keys, vert)
            if 'vert_type' in kwargs:
                if not kwargs['vert_type'] in self.tessagon.vert_types:
                    self.tessagon.vert_types[kwargs['vert_type']] = []
                self.tessagon.vert_types[kwargs['vert_type']].append(vert)

        if vert is not None:
            equivalent_verts = kwargs.get('equivalent', [])
            for equivalent_vert in equivalent_verts:
                self.set_equivalent_vert(*equivalent_vert, vert)

        # We add additional vertices by flipping 'left', 'right' etc
        # if the tile has some kind of symmetry defined
        self._create_symmetric_verts(index_keys, ratio_u, ratio_v, **kwargs)

        # On the boundary, make sure equivalent vertices are set on
        # neighbor tiles
        self._set_equivalent_neighbor_verts(index_keys, vert, **kwargs)

        return vert

    def set_equivalent_vert(self, neighbor_keys, index_keys, vert, **kwargs):
        # On boundary, the vert on a neighbor is equivalent to this vert
        # This is usually only called indirectly via add_vert, but check out
        # PythagoreanTile for an example of direct usage
        if vert is None:
            return None

        tile = self.get_neighbor_tile(neighbor_keys)
        if tile is None:
            return None

        tile._set_vert(self._index_path(index_keys, neighbor_keys), vert)

    def add_face(self, index_keys, vert_index_keys_list, **kwargs):
        # Use the UVMeshMaker to create a face.
        # In reality, multiple faces may get defined if symmetry is declared
        face = self._get_face(index_keys)

        if face is None:
            verts = self._get_verts_from_list(vert_index_keys_list)
            if verts is not None:
                face = \
                    self._make_face(index_keys, verts, **kwargs)

        if face is not None:
            equivalent_faces = kwargs.get('equivalent', [])
            for equivalent_face in equivalent_faces:
                self.set_equivalent_face(*equivalent_face, face)

        # We add additional faces by flipping 'left', 'right' etc
        # if the tile has some kind of symmetry defined
        self._create_symmetric_faces(index_keys, vert_index_keys_list,
                                     **kwargs)

        return face

    def _make_face(self, index_keys, verts, **kwargs):
        face = self.uv_mesh_maker.create_face(verts, **kwargs)
        self._set_face(index_keys, face)

        # On the boundary, make sure equivalent faces are set on neighbor tiles
        self._set_equivalent_neighbor_faces(index_keys, face, **kwargs)

        return face

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
        self.uv_mesh_maker.color_face(face, color_index)

    def set_equivalent_face(self, neighbor_keys, index_keys, face, **kwargs):
        # On boundary, the face on a neighbor is equivalent to this face
        # This is usually only called indirectly via add_face, but check out
        # PythagoreanTile for an example of direct usage
        tile = self.get_neighbor_tile(neighbor_keys)
        if tile is None:
            return None
        tile._set_face(self._index_path(index_keys, neighbor_keys), face)

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

    def rotate_90(self, u, v):
        # Rotating around (1/2, 1/2)
        return [1 - v, u]

    def rotate_180(self, u, v):
        # Rotating around (1/2, 1/2)
        return [1 - u, 1 - v]

    def _create_symmetric_verts(self, index_keys, ratio_u, ratio_v, **kwargs):
        # The 'symmetry' keyword is just to ensure we don't recurse forever
        if 'symmetry' not in kwargs:
            extra_args = {'symmetry': True}

            # This rotational stuff doesn't work yet ...
            # See HokusaiHashesTessagon for an example of something
            # that almost kinda works (not using this code though)
            if self.rot_symmetric == 180:
                rot_keys = self._rotate_index(index_keys)
                self.add_vert(*self.rotate_180(ratio_u, ratio_v),
                              **{**kwargs, **extra_args})

            elif self.rot_symmetric == 90:
                uv = [ratio_u, ratio_v]
                rot_keys = index_keys
                for i in range(3):
                    rot_keys = self._rotate_index(rot_keys)
                    uv = self.rotate_90(*uv)
                    self.add_vert(*rot_keys, uv, **{**kwargs, **extra_args})

            if self.u_symmetric:
                # Add reflection about u
                u_flip_keys = self._u_flip(index_keys)
                if 'equivalent' in kwargs:
                    u_flip_equivalent_keys = self._u_flip(kwargs['equivalent'])
                    extra_args['equivalent'] = u_flip_equivalent_keys
                self.add_vert(u_flip_keys, 1.0 - ratio_u, ratio_v,
                              **{**kwargs, **extra_args})
                if self.v_symmetric:
                    # Add diagonally across
                    uv_flip_keys = self._v_flip(u_flip_keys)
                    if 'equivalent' in kwargs:
                        uv_flip_equivalent_keys = \
                            self._v_flip(u_flip_equivalent_keys)
                        extra_args['equivalent'] = uv_flip_equivalent_keys
                    self.add_vert(uv_flip_keys, 1.0 - ratio_u, 1.0 - ratio_v,
                                  **{**kwargs, **extra_args})
            if self.v_symmetric:
                # Add reflection about v
                v_flip_keys = self._v_flip(index_keys)
                if 'equivalent' in kwargs:
                    v_flip_equivalent_keys = self._v_flip(kwargs['equivalent'])
                    extra_args['equivalent'] = v_flip_equivalent_keys
                self.add_vert(v_flip_keys, ratio_u, 1.0 - ratio_v,
                              **{**kwargs, **extra_args})

    def _set_equivalent_neighbor_verts(self, index_keys, vert, **kwargs):
        if 'u_boundary' in kwargs:
            self._set_u_equivalent_vert(index_keys, vert, **kwargs)
        if 'v_boundary' in kwargs:
            self._set_v_equivalent_vert(index_keys, vert, **kwargs)
        if 'corner' in kwargs:
            self._set_u_equivalent_vert(index_keys, vert, **kwargs)
            self._set_v_equivalent_vert(index_keys, vert, **kwargs)
            self._set_uv_equivalent_vert(index_keys, vert, **kwargs)

    # Handle vert on left/right boundary
    def _set_u_equivalent_vert(self, index_keys, vert, **kwargs):
        u_index = self._u_index(index_keys)
        u_flip_keys = self._u_flip(index_keys)
        self.set_equivalent_vert([u_index], u_flip_keys, vert, **kwargs)

    # Handle vert on top/bottom boundary
    def _set_v_equivalent_vert(self, index_keys, vert, **kwargs):
        v_index = self._v_index(index_keys)
        v_flip_keys = self._v_flip(index_keys)
        self.set_equivalent_vert([v_index], v_flip_keys, vert, **kwargs)

    # Handle vert on corner, equivalent to vert on diagonal tile
    def _set_uv_equivalent_vert(self, index_keys, vert, **kwargs):
        u_index = self._u_index(index_keys)
        v_index = self._v_index(index_keys)
        u_flip_keys = self._u_flip(index_keys)
        uv_flip_keys = self._v_flip(u_flip_keys)
        self.set_equivalent_vert([u_index, v_index], uv_flip_keys, vert,
                                 **kwargs)

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

    def _create_symmetric_faces(self, index_keys, vert_index_keys_list,
                                **kwargs):
        # The 'symmetry' keyword is just to ensure we don't recurse forever
        if 'symmetry' not in kwargs:
            extra_args = {'symmetry': True}
            if self.rot_symmetric == 180:
                rot_keys = self._rotate_index(index_keys)
                rot_vert_index_keys_list \
                    = self._rotate_index(vert_index_keys_list)
                if 'equivalent' in kwargs:
                    equivalent_faces = kwargs['equivalent']
                    kwargs = kwargs.copy()
                    kwargs['equivalent'] = \
                        [self._rotate_index(equivalent_face)
                         for equivalent_face in equivalent_faces]

                self.add_face(rot_keys, rot_vert_index_keys_list,
                              **{**kwargs, **extra_args})
            if self.u_symmetric:
                # Add reflection about u
                u_flip_keys = self._u_flip(index_keys)
                u_flip_vert_index_keys_list \
                    = self._u_flip(vert_index_keys_list)
                self.add_face(u_flip_keys,
                              list(reversed(u_flip_vert_index_keys_list)),
                              **{**kwargs, **extra_args})
                if self.v_symmetric:
                    # Add diagonally across
                    uv_flip_keys = self._v_flip(u_flip_keys)
                    uv_flip_vert_index_keys_list \
                        = self._v_flip(u_flip_vert_index_keys_list)
                    self.add_face(uv_flip_keys, uv_flip_vert_index_keys_list,
                                  **{**kwargs, **extra_args})
            if self.v_symmetric:
                # Add reflection about v
                v_flip_keys = self._v_flip(index_keys)
                v_flip_vert_index_keys_list \
                    = self._v_flip(vert_index_keys_list)
                self.add_face(v_flip_keys,
                              list(reversed(v_flip_vert_index_keys_list)),
                              **{**kwargs, **extra_args})

    def _set_equivalent_neighbor_faces(self, index_keys, face, **kwargs):
        if 'u_boundary' in kwargs:
            self._set_u_equivalent_face(index_keys, face, **kwargs)
        if 'v_boundary' in kwargs:
            self._set_v_equivalent_face(index_keys, face, **kwargs)
        if 'corner' in kwargs:
            self._set_u_equivalent_face(index_keys, face, **kwargs)
            self._set_v_equivalent_face(index_keys, face, **kwargs)
            self._set_uv_equivalent_face(index_keys, face, **kwargs)

    # Handle face on left/right boundary
    def _set_u_equivalent_face(self, index_keys, face, **kwargs):
        u_index = self._u_index(index_keys)
        u_flip_keys = self._u_flip(index_keys)
        self.set_equivalent_face([u_index], u_flip_keys, face, **kwargs)

    # Handle face on top/bottom boundary
    def _set_v_equivalent_face(self, index_keys, face, **kwargs):
        v_index = self._v_index(index_keys)
        v_flip_keys = self._v_flip(index_keys)
        self.set_equivalent_face([v_index], v_flip_keys, face, **kwargs)

    # Handle face on corner, equivalent to face on diagonal tile
    def _set_uv_equivalent_face(self, index_keys, face, **kwargs):
        u_index = self._u_index(index_keys)
        v_index = self._v_index(index_keys)
        u_flip_keys = self._u_flip(index_keys)
        uv_flip_keys = self._v_flip(u_flip_keys)
        self.set_equivalent_face([u_index, v_index], uv_flip_keys, face,
                                 **kwargs)
