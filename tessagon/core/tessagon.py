from tessagon.core.grid_tile_generator import GridTileGenerator
from tessagon.core.rotate_tile_generator import RotateTileGenerator


class Tessagon:
    tile_class = None
    metadata = None

    def __init__(self, **kwargs):
        if 'tile_generator' in kwargs:
            self.tile_generator = kwargs['tile_generator'](self, **kwargs)
        elif 'rot_factor' in kwargs:
            self.tile_generator = RotateTileGenerator(self, **kwargs)
        else:
            self.tile_generator = GridTileGenerator(self, **kwargs)

        self.initialize_function(**kwargs)

        # Optional post processing function
        self.post_process = None
        if 'post_process' in kwargs:
            self.post_process = kwargs['post_process']

        if 'adaptor_class' in kwargs:
            adaptor_class = kwargs['adaptor_class']
            self.mesh_adaptor = adaptor_class(**kwargs)
        else:
            raise ValueError('Must provide a mesh adaptor class')

        self.color_pattern = kwargs.get('color_pattern') or None

        self.tiles = None
        self.face_types = {}
        self.vert_types = {}

    def initialize_function(self, **kwargs):
        self.f = None

        if 'simple_2d' in kwargs:
            u_multiplier_2d = 1.0
            if self.metadata and self.metadata.uv_ratio:
                v_multiplier_2d = 1.0 / self.metadata.uv_ratio
            else:
                v_multiplier_2d = 1.0

            tile_aspect = self.tile_generator.v_num / self.tile_generator.u_num
            multiplier_2d = kwargs.get('multiplier_2d', 1.0)
            u_multiplier_2d *= multiplier_2d
            v_multiplier_2d *= multiplier_2d * tile_aspect

            translate_2d = kwargs.get('translate_2d', (0, 0))
            # Simple xy-plane
            self.f = lambda u, v: (translate_2d[0] + u_multiplier_2d * u,
                                   translate_2d[1] + v_multiplier_2d * v,
                                   0.0)

            # Just to test how the corners are going to map ...
            # top_left = self.tile_generator.corners[0]
            # bottom_right = self.tile_generator.corners[3]
            # print(self.f(*top_left), self.f(*bottom_right))
        elif 'function' in kwargs:
            self.f = kwargs['function']
        else:
            raise ValueError('Must specify a function')

    def create_mesh(self):
        self._initialize_tiles()

        self.mesh_adaptor.create_empty_mesh()

        self._calculate_verts()
        self._calculate_faces()

        if self.color_pattern:
            self._calculate_colors()

        self.mesh_adaptor.finish_mesh()

        if self.post_process:
            # Run user defined post-processing code
            # Need to pass self here (this could be designed better)
            self.post_process(self)

        return self.mesh_adaptor.get_mesh()

    def inspect(self):
        print("\n=== %s ===\n" % (self.__class__.__name__))
        for i in range(len(self.tiles)):
            self.tiles[i].inspect(tile_number=i)

    @classmethod
    def num_color_patterns(cls):
        if cls.metadata is None:
            return 0
        return cls.metadata.num_color_patterns()

    # Below are protected

    def _initialize_tiles(self):
        self.tiles = self.tile_generator.create_tiles()

    def _calculate_verts(self):
        for tile in self.tiles:
            tile.calculate_verts()

    def _calculate_faces(self):
        for tile in self.tiles:
            tile.calculate_faces()

    def _calculate_colors(self):
        self.mesh_adaptor.initialize_colors()
        for tile in self.tiles:
            tile.calculate_colors()
