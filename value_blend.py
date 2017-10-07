class ValueBlend:

  def blend_tuples(self, tuple1, tuple2, ratio):
    out = [None, None]
    for i in range(2):
      out[i] = (1 - ratio) * tuple1[i] + ratio * tuple2[i]
    return out

  def blend(self, ratio_u, ratio_v):
    uv0 = self.blend_tuples(self.corners[0],
                           self.corners[1],
                           ratio_u)
    uv1 = self.blend_tuples(self.corners[2],
                           self.corners[3],
                           ratio_u)
    return self.blend_tuples(uv0, uv1, ratio_v)
