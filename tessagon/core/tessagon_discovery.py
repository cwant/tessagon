from tessagon.types.hex_tessagon import HexTessagon
from tessagon.types.tri_tessagon import TriTessagon
from tessagon.types.octo_tessagon import OctoTessagon
from tessagon.types.rhombus_tessagon import RhombusTessagon
from tessagon.types.hex_tri_tessagon import HexTriTessagon
from tessagon.types.hex_square_tri_tessagon import HexSquareTriTessagon
from tessagon.types.square_tessagon import SquareTessagon
from tessagon.types.pythagorean_tessagon import PythagoreanTessagon
from tessagon.types.brick_tessagon import BrickTessagon
from tessagon.types.dodeca_tessagon import DodecaTessagon
from tessagon.types.square_tri_tessagon import SquareTriTessagon
from tessagon.types.weave_tessagon import WeaveTessagon
from tessagon.types.floret_tessagon import FloretTessagon
from tessagon.types.hex_big_tri_tessagon import HexBigTriTessagon
from tessagon.types.zig_zag_tessagon import ZigZagTessagon
from tessagon.types.dissected_square_tessagon import DissectedSquareTessagon
from tessagon.types.square_tri2_tessagon import SquareTri2Tessagon
from tessagon.types.dodeca_tri_tessagon import DodecaTriTessagon
from tessagon.types.dissected_triangle_tessagon \
    import DissectedTriangleTessagon
from tessagon.types.dissected_hex_quad_tessagon \
    import DissectedHexQuadTessagon
from tessagon.types.dissected_hex_tri_tessagon \
    import DissectedHexTriTessagon
from tessagon.types.penta_tessagon import PentaTessagon
from tessagon.types.penta2_tessagon import Penta2Tessagon

ALL = [SquareTessagon,
       HexTessagon,
       TriTessagon,

       OctoTessagon,
       HexTriTessagon,
       HexSquareTriTessagon,
       DodecaTessagon,
       SquareTriTessagon,
       SquareTri2Tessagon,
       DodecaTriTessagon,

       RhombusTessagon,
       FloretTessagon,
       DissectedSquareTessagon,
       DissectedTriangleTessagon,
       DissectedHexQuadTessagon,
       DissectedHexTriTessagon,
       PentaTessagon,
       Penta2Tessagon,

       PythagoreanTessagon,
       BrickTessagon,
       WeaveTessagon,
       HexBigTriTessagon,
       ZigZagTessagon]


class TessagonDiscovery:
    def __init__(self, **kwargs):
        self.classes = kwargs.get('classes', ALL)

    def count(self):
        return len(self.classes)

    def to_list(self):
        return self.classes

    def inverse(self):
        other_classes = list(set(ALL) - set(self.classes))
        return TessagonDiscovery(classes=other_classes)

    def __add__(self, other):
        new_classes = list(set(self.classes) | set(other.classes))
        return TessagonDiscovery(classes=new_classes)

    def __sub__(self, other):
        new_classes = list(set(self.classes) - set(other.classes))
        return TessagonDiscovery(classes=new_classes)

    def with_color_patterns(self):
        results = []
        for klass in self.classes:
            if klass.metadata is None:
                continue
            if klass.metadata.has_color_patterns():
                results.append(klass)
        return TessagonDiscovery(classes=results)

    def with_classification(self, classification):
        results = []
        for klass in self.classes:
            if klass.metadata is None:
                continue
            if klass.metadata.has_classification(classification):
                results.append(klass)
        return TessagonDiscovery(classes=results)
