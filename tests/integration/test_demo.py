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


# Create the demo meshes for testing
list_demo = ListDemo()
meshes = list_demo.main()


class TestDemo:

    @property
    def meshes(self):
        return meshes

    def vert_list_length(self, tessagon):
        return len(self.meshes[tessagon]['regular']['vert_list'])

    def face_list_length(self, tessagon):
        return len(self.meshes[tessagon]['regular']['face_list'])

    def color_pattern_count(self, tessagon):
        return len(self.meshes[tessagon]['color_patterns'])

    def color_count(self, tessagon, pattern, color):
        colors = self.meshes[tessagon]['color_patterns'][pattern]['color_list']
        return len([c for c in colors if c == color])

    def test_demo_works(self):
        assert len(self.meshes) == 32

    def test_big_hex_tri_tessagon(self):
        tessagon = 'BigHexTriTessagon'
        assert self.vert_list_length(tessagon) == 1344
        assert self.face_list_length(tessagon) == 2016

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 896
        assert self.color_count(tessagon, 1, 1) == 896
        assert self.color_count(tessagon, 1, 2) == 224

    def test_brick_tessagon(self):
        tessagon = 'BrickTessagon'
        assert self.vert_list_length(tessagon) == 1800
        assert self.face_list_length(tessagon) == 900

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 450
        assert self.color_count(tessagon, 1, 1) == 450

    def test_dissected_hex_quad_tessagon(self):
        tessagon = 'DissectedHexQuadTessagon'
        assert self.vert_list_length(tessagon) == 3456
        assert self.face_list_length(tessagon) == 3456

        assert self.color_pattern_count(tessagon) == 2

        assert self.color_count(tessagon, 1, 0) == 1728
        assert self.color_count(tessagon, 1, 1) == 1728

        assert self.color_count(tessagon, 2, 0) == 2304
        assert self.color_count(tessagon, 2, 1) == 1152

    def test_dissected_hex_tri_tessagon(self):
        tessagon = 'DissectedHexTriTessagon'
        assert self.vert_list_length(tessagon) == 2400
        assert self.face_list_length(tessagon) == 4800

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 2400
        assert self.color_count(tessagon, 1, 1) == 2400

    def test_dissected_square_tessagon(self):
        tessagon = 'DissectedSquareTessagon'

        assert self.vert_list_length(tessagon) == 576
        assert self.face_list_length(tessagon) == 1024

        assert self.color_pattern_count(tessagon) == 2

        assert self.color_count(tessagon, 1, 0) == 512
        assert self.color_count(tessagon, 1, 1) == 512

        assert self.color_count(tessagon, 2, 0) == 512
        assert self.color_count(tessagon, 2, 1) == 512

    def test_dissected_triangle_tessagon(self):
        tessagon = 'DissectedTriangleTessagon'

        assert self.vert_list_length(tessagon) == 336
        assert self.face_list_length(tessagon) == 544

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 352
        assert self.color_count(tessagon, 1, 1) == 192

    def test_dodeca_tessagon(self):
        tessagon = 'DodecaTessagon'
        assert self.vert_list_length(tessagon) == 960
        assert self.face_list_length(tessagon) == 440

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 230
        assert self.color_count(tessagon, 1, 1) == 70
        assert self.color_count(tessagon, 1, 2) == 140

    def test_dodeca_tri_tessagon(self):
        tessagon = 'DodecaTriTessagon'
        assert self.vert_list_length(tessagon) == 930
        assert self.face_list_length(tessagon) == 405

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 270
        assert self.color_count(tessagon, 1, 1) == 135

    def test_floret_tessagon(self):
        tessagon = 'FloretTessagon'
        assert self.vert_list_length(tessagon) == 3024
        assert self.face_list_length(tessagon) == 2016

        assert self.color_pattern_count(tessagon) == 3

        assert self.color_count(tessagon, 1, 0) == 1344
        assert self.color_count(tessagon, 1, 1) == 672

        assert self.color_count(tessagon, 2, 0) == 672
        assert self.color_count(tessagon, 2, 1) == 672
        assert self.color_count(tessagon, 2, 2) == 672

        assert self.color_count(tessagon, 3, 0) == 840
        assert self.color_count(tessagon, 3, 1) == 168
        assert self.color_count(tessagon, 3, 2) == 1008

    def test_hex_big_tri_tessagon(self):
        tessagon = 'HexBigTriTessagon'
        assert self.vert_list_length(tessagon) == 840
        assert self.face_list_length(tessagon) == 420

        assert self.color_pattern_count(tessagon) == 2

        assert self.color_count(tessagon, 1, 0) == 280
        assert self.color_count(tessagon, 1, 1) == 140

        assert self.color_count(tessagon, 2, 0) == 140
        assert self.color_count(tessagon, 2, 1) == 140
        assert self.color_count(tessagon, 2, 2) == 140

    def test_hex_square_tri_tessagon(self):
        tessagon = 'HexSquareTriTessagon'
        assert self.vert_list_length(tessagon) == 2700
        assert self.face_list_length(tessagon) == 2700

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 900
        assert self.color_count(tessagon, 1, 1) == 450
        assert self.color_count(tessagon, 1, 2) == 1350

    def test_hex_tessagon(self):
        tessagon = 'HexTessagon'
        assert self.vert_list_length(tessagon) == 540
        assert self.face_list_length(tessagon) == 225

        assert self.color_pattern_count(tessagon) == 2

        assert self.color_count(tessagon, 1, 0) == 150
        assert self.color_count(tessagon, 1, 1) == 75

        assert self.color_count(tessagon, 2, 0) == 75
        assert self.color_count(tessagon, 2, 1) == 75
        assert self.color_count(tessagon, 2, 2) == 75

    def test_hex_tri_tessagon(self):
        tessagon = 'HexTriTessagon'
        assert self.vert_list_length(tessagon) == 925
        assert self.face_list_length(tessagon) == 856

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 580
        assert self.color_count(tessagon, 1, 1) == 276

    def test_octa_tessagon(self):
        # Mobius strip ...
        tessagon = 'OctaTessagon'
        assert self.vert_list_length(tessagon) == 720
        assert self.face_list_length(tessagon) == 280

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 120
        assert self.color_count(tessagon, 1, 1) == 160

    def test_penta2_tessagon(self):
        tessagon = 'Penta2Tessagon'
        assert self.vert_list_length(tessagon) == 1200
        assert self.face_list_length(tessagon) == 800

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 400
        assert self.color_count(tessagon, 1, 1) == 400

    def test_penta_tessagon(self):
        tessagon = 'PentaTessagon'
        assert self.vert_list_length(tessagon) == 960
        assert self.face_list_length(tessagon) == 640

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 320
        assert self.color_count(tessagon, 1, 1) == 320

    def test_pythagorean_tessagon(self):
        tessagon = 'PythagoreanTessagon'
        assert self.vert_list_length(tessagon) == 3000
        assert self.face_list_length(tessagon) == 1500

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 750
        assert self.color_count(tessagon, 1, 1) == 750

    def test_rhombus_tessagon(self):
        # Klein bottle ...
        tessagon = 'RhombusTessagon'
        assert self.vert_list_length(tessagon) == 1440
        assert self.face_list_length(tessagon) == 1440

        assert self.color_pattern_count(tessagon) == 2

        assert self.color_count(tessagon, 1, 0) == 480
        assert self.color_count(tessagon, 1, 1) == 480
        assert self.color_count(tessagon, 1, 2) == 480

        assert self.color_count(tessagon, 2, 0) == 480
        assert self.color_count(tessagon, 2, 1) == 480
        assert self.color_count(tessagon, 2, 2) == 480

    def test_square_tessagon(self):
        # Torus with rot_factor ...
        tessagon = 'SquareTessagon'
        assert self.vert_list_length(tessagon) == 720
        assert self.face_list_length(tessagon) == 720

        assert self.color_pattern_count(tessagon) == 8

        assert self.color_count(tessagon, 1, 0) == 360
        assert self.color_count(tessagon, 1, 1) == 360

        assert self.color_count(tessagon, 2, 0) == 360
        assert self.color_count(tessagon, 2, 1) == 180
        assert self.color_count(tessagon, 2, 2) == 180

        assert self.color_count(tessagon, 3, 0) == 540
        assert self.color_count(tessagon, 3, 1) == 180

        assert self.color_count(tessagon, 4, 0) == 540
        assert self.color_count(tessagon, 4, 1) == 180

        assert self.color_count(tessagon, 5, 0) == 360
        assert self.color_count(tessagon, 5, 1) == 360

        assert self.color_count(tessagon, 6, 0) == 360
        assert self.color_count(tessagon, 6, 1) == 180
        assert self.color_count(tessagon, 6, 2) == 180

        assert self.color_count(tessagon, 7, 0) == 360
        assert self.color_count(tessagon, 7, 1) == 180
        assert self.color_count(tessagon, 7, 2) == 180

        assert self.color_count(tessagon, 8, 0) == 180
        assert self.color_count(tessagon, 8, 1) == 180
        assert self.color_count(tessagon, 8, 2) == 180
        assert self.color_count(tessagon, 8, 3) == 180

    def test_square_tri2_tessagon(self):
        tessagon = 'SquareTri2Tessagon'
        assert self.vert_list_length(tessagon) == 420
        assert self.face_list_length(tessagon) == 595

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 420
        assert self.color_count(tessagon, 1, 1) == 175

    def test_square_tri_tessagon(self):
        tessagon = 'SquareTriTessagon'
        assert self.vert_list_length(tessagon) == 640
        assert self.face_list_length(tessagon) == 960

        assert self.color_pattern_count(tessagon) == 2

        assert self.color_count(tessagon, 1, 0) == 640
        assert self.color_count(tessagon, 1, 1) == 320

        assert self.color_count(tessagon, 2, 0) == 320
        assert self.color_count(tessagon, 2, 1) == 320
        assert self.color_count(tessagon, 2, 2) == 320

    def test_tri_tessagon(self):
        tessagon = 'TriTessagon'
        assert self.vert_list_length(tessagon) == 864
        assert self.face_list_length(tessagon) == 1728

        assert self.color_pattern_count(tessagon) == 3

        assert self.color_count(tessagon, 1, 0) == 864
        assert self.color_count(tessagon, 1, 1) == 864

        assert self.color_count(tessagon, 2, 0) == 864
        assert self.color_count(tessagon, 2, 1) == 864

        assert self.color_count(tessagon, 3, 0) == 1152
        assert self.color_count(tessagon, 3, 1) == 576

    def test_weave_tessagon(self):
        tessagon = 'WeaveTessagon'
        assert self.vert_list_length(tessagon) == 1472
        assert self.face_list_length(tessagon) == 704

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 368
        assert self.color_count(tessagon, 1, 1) == 160
        assert self.color_count(tessagon, 1, 2) == 176

    def test_zig_zag_tessagon(self):
        tessagon = 'ZigZagTessagon'
        assert self.vert_list_length(tessagon) == 1600
        assert self.face_list_length(tessagon) == 800

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 400
        assert self.color_count(tessagon, 1, 1) == 400

    def test_stanley_park_tessagon(self):
        tessagon = 'StanleyParkTessagon'
        assert self.vert_list_length(tessagon) == 2500
        assert self.face_list_length(tessagon) == 500

        assert self.color_pattern_count(tessagon) == 2

        assert self.color_count(tessagon, 1, 0) == 250
        assert self.color_count(tessagon, 1, 1) == 250

        assert self.color_count(tessagon, 2, 0) == 250
        assert self.color_count(tessagon, 2, 1) == 250

    def test_valemount_tessagon(self):
        tessagon = 'ValemountTessagon'
        assert self.vert_list_length(tessagon) == 2880
        assert self.face_list_length(tessagon) == 1600

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 1280
        assert self.color_count(tessagon, 1, 1) == 320

    def test_islamic_hex_stars_tessagon(self):
        tessagon = 'IslamicHexStarsTessagon'
        assert self.vert_list_length(tessagon) == 1872
        assert self.face_list_length(tessagon) == 624

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 416
        assert self.color_count(tessagon, 1, 1) == 208

    def test_islamic_stars_crosses_tessagon(self):
        tessagon = 'IslamicStarsCrossesTessagon'
        assert self.vert_list_length(tessagon) == 2775
        assert self.face_list_length(tessagon) == 345

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 195
        assert self.color_count(tessagon, 1, 1) == 150

    def test_cloverdale_tessagon(self):
        tessagon = 'CloverdaleTessagon'
        assert self.vert_list_length(tessagon) == 3766
        assert self.face_list_length(tessagon) == 2534

        assert self.color_pattern_count(tessagon) == 1

        assert self.color_count(tessagon, 1, 0) == 1568
        assert self.color_count(tessagon, 1, 1) == 966

    def test_hokusai_hashes_tessagon(self):
        tessagon = 'HokusaiHashesTessagon'
        assert self.vert_list_length(tessagon) == 3066
        assert self.face_list_length(tessagon) == 364

        assert self.color_pattern_count(tessagon) == 2

        # There are 14x2 more squares due v_cyclic = False
        assert self.color_count(tessagon, 1, 0) == 168
        assert self.color_count(tessagon, 1, 1) == 196

        assert self.color_count(tessagon, 2, 0) == 182
        assert self.color_count(tessagon, 2, 1) == 182

    def test_hokusai_hashes_parallelograms(self):
        tessagon = 'HokusaiParallelogramsTessagon'
        assert self.vert_list_length(tessagon) == 1512
        assert self.face_list_length(tessagon) == 1080

        assert self.color_pattern_count(tessagon) == 3

        assert self.color_count(tessagon, 1, 0) == 648
        assert self.color_count(tessagon, 1, 1) == 432

        assert self.color_count(tessagon, 2, 0) == 216
        assert self.color_count(tessagon, 2, 1) == 216
        assert self.color_count(tessagon, 2, 2) == 216
        assert self.color_count(tessagon, 2, 3) == 432

        assert self.color_count(tessagon, 3, 0) == 216
        assert self.color_count(tessagon, 3, 1) == 216
        assert self.color_count(tessagon, 3, 2) == 216
        assert self.color_count(tessagon, 3, 3) == 432

    def test_slats(self):
        tessagon = 'SlatsTessagon'
        assert self.vert_list_length(tessagon) == 2880
        assert self.face_list_length(tessagon) == 1728

        assert self.color_pattern_count(tessagon) == 2

        assert self.color_count(tessagon, 1, 0) == 864
        assert self.color_count(tessagon, 1, 1) == 864

        assert self.color_count(tessagon, 2, 0) == 864
        assert self.color_count(tessagon, 2, 1) == 864
