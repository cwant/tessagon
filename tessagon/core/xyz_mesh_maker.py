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

    @property
    def uv_ratio(self):
        return self.tessagon.uv_ratio

    @property
    def u_num(self):
        return self.tessagon.u_num

    @property
    def v_num(self):
        return self.tessagon.v_num

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
        # multiplier_2d is the total width of the 2d output
        # We strive to maintain the correct aspect ratio

        if not self._initialize_bounding_box_2d(**kwargs):
            self.multiplier_2d = kwargs.get('multiplier_2d', 1.0)
            self.translate_2d = kwargs.get('translate_2d', (0, 0))

        total_width = self.multiplier_2d
        tile_width = total_width / self.u_num
        tile_height = tile_width / self.uv_ratio
        total_height = tile_height * self.v_num

        # Map to xy-plane
        return lambda u, v: (self.translate_2d[0] + total_width * u,
                             self.translate_2d[1] + total_height * v,
                             0.0)

    def _initialize_bounding_box_2d(self, **kwargs):
        # We try to fit the output in the bounding box, optionally centered
        bounding_box = kwargs.get('bounding_box_2d', None)
        center_bounding_box = kwargs.get('center_bounding_box_2d', False)

        if not bounding_box:
            return False

        (x_min, x_max) = bounding_box[0]
        (y_min, y_max) = bounding_box[1]

        if (x_min >= x_max) or (y_min >= y_max):
            raise ValueError("Malformed 2D bounding box, expecting: "
                             "[[x_min, x_max], [y_min, y_max]]")

        self.translate_2d = [x_min, y_min]

        width = x_max - x_min
        height = y_max - y_min

        tile_width = width / self.u_num
        tile_height = tile_width / self.uv_ratio
        total_height = tile_height * self.v_num
        if total_height > height:
            # Scale back to fit the y direction
            total_width = width * (height / total_height)
            self.multiplier_2d = total_width
            if center_bounding_box:
                self.translate_2d[0] += ((width - total_width) / 2)
        else:
            self.multiplier_2d = width
            if center_bounding_box:
                self.translate_2d[1] += ((height - total_height) / 2)

        return True

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
