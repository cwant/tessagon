class XYZMeshMaker:

    def __init__(self, tessagon, **kwargs):
        self.tessagon = tessagon
        self.uv_mesh_maker = tessagon.uv_mesh_maker
        self.mesh_adaptor = self.get_mesh_adaptor(**kwargs)

        # Optional post processing function
        self.post_process = None
        if 'post_process' in kwargs:
            self.post_process = kwargs['post_process']

        self._initialize_function(**kwargs)
        self._initialize_output()

    def get_mesh_adaptor(self, **kwargs):
        if 'adaptor_class' in kwargs:
            adaptor_class = kwargs['adaptor_class']

            # Get options that are specific to this adaptor
            adaptor_options = {}
            for option in adaptor_class.ADAPTOR_OPTIONS:
                if option in kwargs:
                    adaptor_options[option] = kwargs[option]

            return adaptor_class(**adaptor_options)
        else:
            raise ValueError('Must provide a mesh adaptor class')

    def create_mesh(self):
        self.uv_mesh_maker.create_uv_mesh()

        self._initialize_output()
        self.mesh_adaptor.create_empty_mesh()

        self._calculate_verts()
        self._calculate_faces()

        if self.uv_mesh_maker.color_pattern:
            self._calculate_colors()

        self.mesh_adaptor.finish_mesh()

        if self.post_process:
            # Run user defined post-processing code
            # Need to pass self here (this could be designed better)
            self.post_process(self)

        return self.mesh_adaptor.get_mesh()

    def _initialize_function(self, **kwargs):
        self.f = None

        if 'simple_2d' in kwargs:
            self.f = self._initialize_simple_2d_function(**kwargs)
        elif 'function' in kwargs:
            self.f = kwargs['function']
        else:
            raise ValueError('Must specify a function')

    def _initialize_simple_2d_function(self, **kwargs):
        metadata = self.tessagon.metadata

        u_multiplier_2d = 1.0
        if metadata and metadata.uv_ratio:
            v_multiplier_2d = 1.0 / metadata.uv_ratio
        else:
            v_multiplier_2d = 1.0

        tile_aspect = self.uv_mesh_maker.v_num / self.uv_mesh_maker.u_num
        multiplier_2d = kwargs.get('multiplier_2d', 1.0)
        u_multiplier_2d *= multiplier_2d
        v_multiplier_2d *= multiplier_2d * tile_aspect

        translate_2d = kwargs.get('translate_2d', (0, 0))
        # Simple xy-plane
        return lambda u, v: (translate_2d[0] + u_multiplier_2d * u,
                             translate_2d[1] + v_multiplier_2d * v,
                             0.0)

        # Just to test how the corners are going to map ...
        # top_left = self.tile_generator.corners[0]
        # bottom_right = self.tile_generator.corners[3]
        # print(self.f(*top_left), self.f(*bottom_right))

    def _initialize_output(self):
        self.verts = []
        self.faces = []

    def _calculate_verts(self):
        for vert in self.uv_mesh_maker.verts:
            coords = self.f(*vert)
            vert = self.mesh_adaptor.create_vert(coords)
            self.verts.append(vert)

    def _calculate_faces(self):
        for face in self.uv_mesh_maker.faces:
            verts = [self.verts[i] for i in face]
            face = self.mesh_adaptor.create_face(verts)
            self.faces.append(face)

    def _calculate_colors(self):
        self.mesh_adaptor.initialize_colors()

        for i in range(len(self.faces)):
            face = self.faces[i]
            color_index = self.uv_mesh_maker.color_faces[i]
            self.mesh_adaptor.color_face(face, color_index)
