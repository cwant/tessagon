import inspect
import re
from tessagon import TessagonDiscovery

from tessagon.misc.shapes import cylinder, torus, one_sheet_hyperboloid, \
    klein, mobius, sphere, paraboloid, general_torus, warp_var

class TessagonCommonDemo:
    # This is an abstract class that handles common code for the
    # demos. Each subclass needs to implement the 'tessellate' method
    # which instantiates each tessagon class, creates a mesh, and puts it
    # in the scene for the particular software package.

    def class_to_method(self, cls):
        # We have rendering functions like self.hex_tessagon,
        # self.square_tessagon, etc, and we would like to get these
        # function when passed the tessagon class cls, e.g., HexTessagon,
        # SquareTessagon, etc.

        # Class to snake case, e.g. HexTessagon -> hex_tessagon
        method_name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        # Return alias to method, e.g. self.hex_tessagon
        return getattr(self, method_name)

    def method_to_class(self):
        # When called from a method name like 'square_tessagon' we want to return
        # the Tessagon class SquareTessagon
        method_name = inspect.stack()[1][3]
        # Convert from snake_case to CamelCase
        class_name = ''.join(word.title() for word in method_name.split('_'))
        return TessagonDiscovery.get_class(class_name)

    def create_objects(self):
        find_all = TessagonDiscovery()
        classes = find_all.with_classification('regular').to_list() \
            + find_all.with_classification('archimedean').to_list() \
            + find_all.with_classification('laves').to_list() \
            + find_all.with_classification('non_edge').to_list() \
            + find_all.with_classification('non_convex').to_list() \
            + find_all.with_classification('non_manifold').to_list()
        
        # A long row of each tiling pattern, with color patterns underneath
        offset = 15

        column = 0

        # Output meshes for potential inspection (e.g. test suite)
        meshes = {}

        for cls in classes:
            key = cls.__name__
            meshes[key] = {'color_patterns': {},
                           'extra_parameters': {}}

            method = self.class_to_method(cls)

            row = 0

            # Non-color pattern object
            meshes[key]['regular'] = method([column, 0, row])

            for i in range(cls.num_color_patterns()):
                color_pattern = i + 1
                row -= offset

                # Color pattern object
                meshes[key]['color_patterns'][color_pattern] = \
                    method([column, 0, row], color_pattern=color_pattern)

            for parameter in cls.metadata.extra_parameters:
                parameter_info = cls.metadata.extra_parameters[parameter]
                meshes[key]['extra_parameters'][parameter] = {}
                if parameter_info['type'] in ['float', 'int']:
                    values = dict(low=self.parameter_min(parameter_info),
                                  high=self.parameter_max(parameter_info))
                    for value_name in values:
                        value = values[value_name]
                        row -= offset
                        kwargs = {parameter: value}
                        meshes[key]['extra_parameters'][parameter][value_name] = \
                            method([column, 0, row], **kwargs)

            column += offset

        return meshes

    def parameter_min(self, parameter_info):
        if 'demo_min' in parameter_info:
            return parameter_info['demo_min']
        return (parameter_info['default'] + parameter_info['min']) / 2.0

    def parameter_max(self, parameter_info):
        if 'demo_max' in parameter_info:
            return parameter_info['demo_max']
        return (parameter_info['default'] + parameter_info['max']) / 2.0

    def hex_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 90,
            'v_num': 6,
            'u_cyclic': True,
            'v_cyclic': False,
            'position': position
        }
        HexTessagon = self.method_to_class()
        return self.tessellate(cylinder, HexTessagon,
                               **{**kwargs, **options})

    def tri_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 24,
            'v_num': 72,
            'position': position
        }
        TriTessagon = self.method_to_class()
        return self.tessellate(self.torus2, TriTessagon,
                               **{**kwargs, **options})

    def square_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 24,
            'v_num': 6,
            'rot_factor': 2,
            'position': position
        }
        SquareTessagon = self.method_to_class()
        return self.tessellate(torus, SquareTessagon,
                               **{**kwargs, **options})

    def rhombus_klein(self, u, v):
        (x, y, z) = klein(u, v)
        return (x, z, -y)

    def rhombus_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 80,
            'v_num': 12,
            # v_twist is currently broken, hopefully can turn this on again soon.
            # 'v_twist': True,
            'position': position
        }
        RhombusTessagon = self.method_to_class()
        return self.tessellate(self.rhombus_klein, RhombusTessagon,
                               **{**kwargs, **options})

    def octa_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 4,
            'v_num': 40,
            'v_cyclic': True,
            'u_cyclic': False,
            'u_twist': True,
            'position': position
        }
        OctaTessagon = self.method_to_class()
        return self.tessellate(mobius, OctaTessagon,
                               **{**kwargs, **options})

    def hex_tri_tessagon(self, position, **kwargs):
        options = {
            'u_range': [-1.0, 1.0],
            'v_range': [-1.0, 1.0],
            'u_num': 30,
            'v_num': 20,
            'u_cyclic': False,
            'v_cyclic': False,
            'position': position
        }
        HexTriTessagon = self.method_to_class()
        return self.tessellate(paraboloid, HexTriTessagon,
                               **{**kwargs, **options})

    def hex_square_tri_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 90,
            'v_num': 10,
            'position': position
        }
        HexSquareTriTessagon = self.method_to_class()
        return self.tessellate(torus, HexSquareTriTessagon,
                               **{**kwargs, **options})

    def pythagorean_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 25,
            'v_num': 6,
            'rot_factor': 2,
            'position': position
        }
        PythagoreanTessagon = self.method_to_class()
        return self.tessellate(torus, PythagoreanTessagon,
                               **{**kwargs, **options})

    def brick_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 15,
            'v_num': 3,
            'rot_factor': 3,
            'position': position
        }
        BrickTessagon = self.method_to_class()
        return self.tessellate(torus, BrickTessagon,
                               **{**kwargs, **options})

    def dodeca_tessagon(self, position, **kwargs):
        options = {
            'u_range': [-1.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 8,
            'v_num': 20,
            'u_cyclic': False,
            'v_cyclic': True,
            'position': position
        }
        DodecaTessagon = self.method_to_class()
        return self.tessellate(one_sheet_hyperboloid, DodecaTessagon,
                               **{**kwargs, **options})

    def big_hex_tri_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 56,
            'v_num': 8,
            'position': position
        }
        BigHexTriTessagon = self.method_to_class()
        return self.tessellate(torus, BigHexTriTessagon,
                               **{**kwargs, **options})

    def square_tri_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 40,
            'v_num': 8,
            'position': position
        }
        SquareTriTessagon = self.method_to_class()
        return self.tessellate(torus, SquareTriTessagon,
                               **{**kwargs, **options})

    def weave_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 16,
            'v_num': 12,
            'v_cyclic': False,
            'rot_factor': 1,
            'position': position
        }
        WeaveTessagon = self.method_to_class()
        return self.tessellate(sphere, WeaveTessagon,
                               **{**kwargs, **options})

    def chubby_torus(self, u, v):
        # u_cyclic = True, v_cyclic = True
        r1 = 5.0
        r2 = 1.5
        return general_torus(r1, r2, v, warp_var(u, 0.2))

    def floret_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 2,
            'v_num': 12,
            'parallelogram_vectors': [[9,-1], [1, 3]],
            'position': position
        }
        FloretTessagon = self.method_to_class()
        return self.tessellate(self.chubby_torus, FloretTessagon,
                               **{**kwargs, **options})

    def flip_axes_torus(self, u, v):
        return torus(v, -u)

    def hex_big_tri_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 2,
            'v_num': 5,
            'parallelogram_vectors': [[5, 1], [-3, 5]],
            'position': position
        }
        HexBigTriTessagon = self.method_to_class()
        return self.tessellate(self.flip_axes_torus, HexBigTriTessagon,
                               **{**kwargs, **options})

    def zig_zag_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 20,
            'v_num': 4,
            'rot_factor': 2,
            'position': position
        }
        ZigZagTessagon = self.method_to_class()
        return self.tessellate(torus, ZigZagTessagon,
                               **{**kwargs, **options})

    def dissected_square_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 64,
            'v_num': 8,
            'u_cyclic': True,
            'v_cyclic': False,
            'position': position
        }
        DissectedSquareTessagon = self.method_to_class()
        return self.tessellate(cylinder, DissectedSquareTessagon,
                               **{**kwargs, **options})

    def square_tri2_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 70,
            'v_num': 6,
            'v_cyclic': False,
            'position': position
        }
        SquareTri2Tessagon = self.method_to_class()
        return self.tessellate(cylinder, SquareTri2Tessagon,
                               **{**kwargs, **options})

    def dodeca_tri_tessagon(self, position, **kwargs):
        options = {
            'u_range': [-1.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 10,
            'v_num': 30,
            'u_cyclic': False,
            'v_cyclic': True,
            'position': position
        }
        DodecaTriTessagon = self.method_to_class()
        return self.tessellate(one_sheet_hyperboloid, DodecaTriTessagon,
                               **{**kwargs, **options})

    def cylinder2(self, u, v):
        return cylinder(v, u)

    def dissected_triangle_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 6,
            'v_num': 32,
            'u_cyclic': False,
            'v_cyclic': True,
            'position': position
        }
        DissectedTriangleTessagon = self.method_to_class()
        return self.tessellate(self.cylinder2, DissectedTriangleTessagon,
                               **{**kwargs, **options})

    def dissected_hex_quad_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 24,
            'v_num': 48,
            'u_cyclic': True,
            'v_cyclic': True,
            'position': position
        }
        DissectedHexQuadTessagon = self.method_to_class()
        return self.tessellate(self.chubby_torus, DissectedHexQuadTessagon,
                               **{**kwargs, **options})

    def dissected_hex_tri_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 20,
            'v_num': 40,
            'u_cyclic': True,
            'v_cyclic': True,
            'position': position
        }
        DissectedHexTriTessagon = self.method_to_class()
        return self.tessellate(self.chubby_torus, DissectedHexTriTessagon,
                               **{**kwargs, **options})

    def penta_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 40,
            'v_num': 8,
            'position': position
        }
        PentaTessagon = self.method_to_class()
        return self.tessellate(torus, PentaTessagon,
                               **{**kwargs, **options})

    def penta2_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 100,
            'v_num': 8,
            'position': position
        }
        Penta2Tessagon = self.method_to_class()
        return self.tessellate(torus, Penta2Tessagon,
                               **{**kwargs, **options})

    def torus2(self, u, v):
        return torus(v, u)

    def stanley_park_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 10,
            'v_num': 25,
            'position': position
        }
        StanleyParkTessagon = self.method_to_class()
        return self.tessellate(self.torus2, StanleyParkTessagon,
                               **{**kwargs, **options})

    def valemount_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 16,
            'v_num': 4,
            'rot_factor': 2,
            'position': position
        }
        ValemountTessagon = self.method_to_class()
        return self.tessellate(torus, ValemountTessagon,
                               **{**kwargs, **options})

    def islamic_hex_stars_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 8,
            'v_num': 2,
            'rot_factor': 5,
            'position': position
        }
        IslamicHexStarsTessagon = self.method_to_class()
        return self.tessellate(torus, IslamicHexStarsTessagon,
                               **{**kwargs, **options})

    def islamic_stars_crosses_tessagon(self, position, **kwargs):
        options = {
            'u_range': [-1.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 3,
            'v_num': 15,
            'rot_factor': 2,
            'u_cyclic': False,
            'v_cyclic': True,
            'position': position
        }
        IslamicStarsCrossesTessagon = self.method_to_class()
        return self.tessellate(one_sheet_hyperboloid, IslamicStarsCrossesTessagon,
                               **{**kwargs, **options})

    def cloverdale_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 14,
            'v_num': 14,
            'v_cyclic': False,
            'position': position
        }
        CloverdaleTessagon = self.method_to_class()
        return self.tessellate(sphere, CloverdaleTessagon,
                               **{**kwargs, **options})

    def hokusai_hashes_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 14,
            'v_num': 14,
            'v_cyclic': False,
            'position': position
        }
        HokusaiHashesTessagon = self.method_to_class()
        return self.tessellate(sphere, HokusaiHashesTessagon,
                               **{**kwargs, **options})

    def hokusai_parallelograms_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 54,
            'v_num': 8,
            'position': position
        }
        HokusaiParallelogramsTessagon = self.method_to_class()
        return self.tessellate(torus, HokusaiParallelogramsTessagon,
                               **{**kwargs, **options})

    def slats_tessagon(self, position, **kwargs):
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 48,
            'v_num': 12,
            'position': position
        }
        SlatsTessagon = self.method_to_class()
        return self.tessellate(torus, SlatsTessagon,
                               **{**kwargs, **options})
