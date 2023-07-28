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
        self._process_extra_parameters(**kwargs)

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

        if self.extra_parameters:
            for parameter in self.extra_parameters:
                extra_args[parameter] = self.extra_parameters[parameter]

        tile_class = self.tessagon.get_tile_class(extra_args['fingerprint'])
        return tile_class(self.tessagon,
                          **{**kwargs, **extra_args})

    def create_tiles(self):
        self.initialize_tiles()
        self.initialize_neighbors()
        tiles = self.get_tiles()
        for tile in tiles:
            tile.validate()

        return tiles

    def _process_extra_parameters(self, **kwargs):
        self.extra_parameters = {}
        if not self.tessagon.metadata:
            return

        parameters_info = self.tessagon.metadata.extra_parameters
        if not parameters_info:
            return

        for parameter in parameters_info:
            parameter_info = parameters_info[parameter]
            if parameter not in kwargs:
                continue
            value = kwargs.get(parameter)
            if parameter_info['type'] in ['float', 'int']:
                self._process_numerical_extra_parameter(parameter,
                                                        value,
                                                        parameter_info)

    def _process_numerical_extra_parameter(self, parameter, value,
                                           parameter_info):
        max_value = parameter_info.get('max')
        min_value = parameter_info.get('min')
        if max_value is not None and value > max_value:
            raise ValueError('Parameter {} ({}) exceeds maximum ({})'
                             .format(parameter, value, max_value))
        if min_value is not None and value < min_value:
            raise ValueError('Parameter {} ({}) below minimum ({})'
                             .format(parameter, value, min_value))
        self.extra_parameters[parameter] = value
