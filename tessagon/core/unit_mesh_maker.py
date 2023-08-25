from tessagon.core.grid_tile_generator import GridTileGenerator
from tessagon.core.parallelogram_tile_generator \
    import ParallelogramTileGenerator


class UnitMeshMaker:
    def __init__(self, tessagon, **kwargs):
        self.tessagon = tessagon
        self.tile_generator = self._get_tile_generator(**kwargs)
        self.color_pattern = kwargs.get('color_pattern') or None

        self.tiles = None

        # Output (TODO: another class?)
        self._initialize_output()

    @property
    def u_num(self):
        return self.tile_generator.u_num

    @property
    def v_num(self):
        return self.tile_generator.v_num

    @property
    def extra_parameters(self):
        return self.tile_generator.extra_parameters

    @property
    def uv_ratio(self):
        return self.tessagon.uv_ratio

    def create_vert(self, coords):
        self.verts.append(coords)
        return (len(self.verts) - 1)

    def create_face(self, verts, **kwargs):
        self.faces.append(verts)
        index = len(self.faces) - 1
        face_type = kwargs.get('face_type')
        if face_type:
            if face_type not in self.face_types:
                self.face_types[face_type] = []
            self.face_types[face_type].append(index)
        return (index)

    def color_face(self, face, color_index):
        self.color_faces[face] = color_index

    def create_unit_mesh(self):
        self._initialize_tiles()
        self._initialize_output()

        self._calculate_verts()
        self._calculate_faces()

        if self.color_pattern:
            self._calculate_colors()

        self._finish_mesh()

    def inspect(self):
        print("\n=== %s ===\n" % (self.__class__.__name__))
        for i in range(len(self.tiles)):
            self.tiles[i].inspect(tile_number=i)

    def _get_tile_generator(self, **kwargs):
        if 'tile_generator' in kwargs:
            return kwargs['tile_generator'](self.tessagon, **kwargs)
        elif 'rot_factor' in kwargs:
            # Deprecated?
            rot_factor = kwargs['rot_factor']
            extra_args = {'parallelogram_vectors':
                          [[rot_factor, -1], [1, rot_factor]]}

            return ParallelogramTileGenerator(self.tessagon,
                                              **{**kwargs, **extra_args})
        elif 'parallelogram_vectors' in kwargs:
            return ParallelogramTileGenerator(self.tessagon, **kwargs)
        else:
            return GridTileGenerator(self.tessagon, **kwargs)

    def _initialize_tiles(self):
        self.tiles = self.tile_generator.create_tiles()

    def _calculate_verts(self):
        for tile in self.tiles:
            tile.calculate_verts()

    def _calculate_faces(self):
        for tile in self.tiles:
            tile.calculate_faces()

    def _initialize_colors(self):
        self.color_faces = [0]*len(self.faces)

    def _calculate_colors(self):
        self._initialize_colors()
        for tile in self.tiles:
            tile.calculate_colors()

    def _initialize_output(self):
        self.verts = []
        self.faces = []
        self.color_faces = []
        self.face_types = {}
        self.vert_types = {}

    def _finish_mesh(self):
        self._reduce_unused_verts()
        self._reorder_faces()

    def _reduce_unused_verts(self):
        # TODO: vert_types?

        # flatten faces to get a list of verts
        incomprehension = [vert for face in self.faces for vert in face]
        used_verts = sorted(list(set(incomprehension)))
        if len(used_verts) == len(self.verts):
            # No verts to reduce
            return
        new_verts = [self.verts[i] for i in used_verts]
        vert_map = {used_verts[i]: i for i in range(len(used_verts))}
        new_faces = []
        for face in self.faces:
            new_face = [vert_map[i] for i in face]
            new_faces.append(new_face)
        self.verts = new_verts
        self.faces = new_faces

    def _reorder_faces(self):
        if not self.tessagon.face_order:
            return

        # Reorder them
        new_faces = []
        new_colors = []
        new_face_types = {}

        ordered_indices = []
        index = 0
        for face_type in self.tessagon.face_order:
            ordered_indices.extend(self.face_types[face_type])

            num_faces = len(self.face_types[face_type])
            new_face_types[face_type] = list(range(index, index + num_faces))
            index = index + num_faces

        for i in ordered_indices:
            new_faces.append(self.faces[i])
            if len(self.color_faces) > 0:
                new_colors.append(self.color_faces[i])

        self.faces = new_faces
        self.color_faces = new_colors
        self.face_types = new_face_types
