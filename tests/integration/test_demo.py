# from core_tests_base import CoreTestsBase
import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')
sys.path.append(this_dir + '/../../demo')

from tessagon.adaptors.list_adaptor import ListAdaptor  # noqa: E402
from tessagon_common_demo import TessagonCommonDemo  # noqa: E402


class ListDemo(TessagonCommonDemo):
    def tessellate(self, f, tessagon_class, **kwargs):
        extra_args = {'function': f,
                      'adaptor_class': ListAdaptor}
        tessagon = tessagon_class(**{**kwargs, **extra_args})
        return tessagon.create_mesh()

    def main(self):
        return self.create_objects()


class TestDemo:

    def __init(self):
        self.meshes = None

    def vert_list_length(self, tessagon):
        return len(self.meshes[tessagon]['regular']['vert_list'])

    def face_list_length(self, tessagon):
        return len(self.meshes[tessagon]['regular']['face_list'])

    def test_demo_works(self):
        list_demo = ListDemo()
        self.meshes = list_demo.main()
        assert len(self.meshes) == 24

        assert self.vert_list_length('BigHexTriTessagon') == 1344
        assert self.face_list_length('BigHexTriTessagon') == 2016

        assert self.vert_list_length('BrickTessagon') == 1800
        assert self.face_list_length('BrickTessagon') == 900

        assert self.vert_list_length('DissectedHexQuadTessagon') == 3456
        assert self.face_list_length('DissectedHexQuadTessagon') == 3456

        assert self.vert_list_length('DissectedHexTriTessagon') == 2400
        assert self.face_list_length('DissectedHexTriTessagon') == 4800

        assert self.vert_list_length('DissectedTriangleTessagon') == 336
        assert self.face_list_length('DissectedTriangleTessagon') == 544

        assert self.vert_list_length('DodecaTessagon') == 960
        assert self.face_list_length('DodecaTessagon') == 440

        assert self.vert_list_length('DodecaTriTessagon') == 720
        assert self.face_list_length('DodecaTriTessagon') == 340

        assert self.vert_list_length('FloretTessagon') == 3024
        assert self.face_list_length('FloretTessagon') == 2016

        assert self.vert_list_length('HexBigTriTessagon') == 840
        assert self.face_list_length('HexBigTriTessagon') == 420

        assert self.vert_list_length('HexSquareTriTessagon') == 2700
        assert self.face_list_length('HexSquareTriTessagon') == 2700

        assert self.vert_list_length('HexTessagon') == 540
        assert self.face_list_length('HexTessagon') == 225

        assert self.vert_list_length('HexTriTessagon') == 925
        assert self.face_list_length('HexTriTessagon') == 856

        # Mobius strip ...
        assert self.vert_list_length('OctoTessagon') == 720
        assert self.face_list_length('OctoTessagon') == 280

        assert self.vert_list_length('Penta2Tessagon') == 1200
        assert self.face_list_length('Penta2Tessagon') == 800

        assert self.vert_list_length('PentaTessagon') == 960
        assert self.face_list_length('PentaTessagon') == 640

        assert self.vert_list_length('PythagoreanTessagon') == 3000
        assert self.face_list_length('PythagoreanTessagon') == 1500

        # Klein bottle ...
        assert self.vert_list_length('RhombusTessagon') == 1440
        assert self.face_list_length('RhombusTessagon') == 1440

        # Torus with rot_factor ...
        assert self.vert_list_length('SquareTessagon') == 720
        assert self.face_list_length('SquareTessagon') == 720

        assert self.vert_list_length('TriTessagon') == 864
        assert self.face_list_length('TriTessagon') == 1728

        assert self.vert_list_length('WeaveTessagon') == 1408
        assert self.face_list_length('WeaveTessagon') == 672

        assert self.vert_list_length('ZigZagTessagon') == 1600
        assert self.face_list_length('ZigZagTessagon') == 800
