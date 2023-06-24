from tessagon.core.value_blend import ValueBlend


class TileGenerator(ValueBlend):
    # This is intended to be an abstract class to generate tiles,
    # but it's quite tied to a grid structure, so it might make
    # sense to merge with GridTileGenerator
    def __init__(self, tessagon, **kwargs):
        self.tessagon = tessagon

        # Corners is list of tuples:
        #   [topleft, topright, bottomleft, bottomright]
        self.corners = None
        self._init_corners(**kwargs)

        self.u_num = kwargs.get('u_num')
        self.v_num = kwargs.get('v_num')
        if not self.u_num or not self.v_num:
            raise ValueError("Make sure u_num and v_num intervals are set")

        self.u_cyclic = kwargs.get('u_cyclic', True)
        self.v_cyclic = kwargs.get('v_cyclic', True)
        self.v_twist = kwargs.get('v_twist', False)
        self.u_twist = kwargs.get('u_twist', False)

        # TODO: delete these?
        self.u_phase = kwargs.get('u_phase', 0.0)
        self.v_phase = kwargs.get('v_phase', 0.0)
        self.u_shear = kwargs.get('u_shear', 0.0)
        self.v_shear = kwargs.get('v_shear', 0.0)

        # Note: id_prefix is not used for calculation, just debugging
        self.id_prefix = self.tessagon.__class__.__name__
        if 'id_prefix' in kwargs:
            self.id_prefix = kwargs['id_prefix']
        self.fingerprint_offset = kwargs.get('fingerprint_offset') or None

        self.color_pattern = kwargs.get('color_pattern') or None

    def create_tile(self, u, v, corners, **kwargs):
        extra_args = {'corners': corners,
                      'fingerprint': [u, v]}
        if self.fingerprint_offset:
            extra_args['fingerprint'][0] += self.fingerprint_offset[0]
            extra_args['fingerprint'][1] += self.fingerprint_offset[1]

        if self.id_prefix:
            extra_args['id'] = "%s[%d][%d]" % (self.id_prefix, u, v)

        if self.color_pattern:
            extra_args['color_pattern'] = self.color_pattern

        extra_parameters = self.tessagon.extra_parameters
        if extra_parameters:
            for parameter in extra_parameters:
                extra_args[parameter] = extra_parameters[parameter]

        tile_class = self.tessagon.__class__.tile_class
        return tile_class(self.tessagon,
                          **{**kwargs, **extra_args})

    def create_tiles(self):
        self.initialize_tiles()
        self.initialize_neighbors()
        tiles = self.get_tiles()
        for tile in tiles:
            tile.validate()

        return tiles
