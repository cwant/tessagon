class ValueBlend:

    def _init_corners(self, **kwargs):
        # Corners is list of tuples:
        #   [bottomleft, bottomright, topleft, topright]
        if 'corners' in kwargs:
            self.corners = kwargs['corners']
            if len(self.corners) != 4 or \
               any(len(v) != 2 for v in self.corners):
                raise ValueError("corner should be a list of four tuples, "
                                 "set either option 'corners' "
                                 "or options 'u_range' and 'v_range'")
        elif 'u_range' in kwargs and 'v_range' in kwargs:
            self.corners = [[kwargs['u_range'][0], kwargs['v_range'][0]],
                            [kwargs['u_range'][1], kwargs['v_range'][0]],
                            [kwargs['u_range'][0], kwargs['v_range'][1]],
                            [kwargs['u_range'][1], kwargs['v_range'][1]]]
        else:
            raise ValueError("Must set either option "
                             "'corners' or options 'u_range' and 'v_range'")

    def _blend_tuples(self, tuple1, tuple2, ratio):
        out = [None, None]
        for i in range(2):
            out[i] = (1 - ratio) * tuple1[i] + ratio * tuple2[i]
        return out

    def blend(self, ratio_u, ratio_v):
        uv0 = self._blend_tuples(self.corners[0],
                                 self.corners[1],
                                 ratio_u)
        uv1 = self._blend_tuples(self.corners[2],
                                 self.corners[3],
                                 ratio_u)
        return self._blend_tuples(uv0, uv1, ratio_v)
