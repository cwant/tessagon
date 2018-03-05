# Don't run me directly!
# Load the file demo/tessagon_demo.blend into blender, it will run me

import bpy
from tessagon.types.hex_tessagon import HexTessagon
from tessagon.misc.shapes import other_torus
from tessagon_common_demo import TessagonCommonDemo
from tessagon.adaptors.blender_adaptor import BlenderAdaptor

# Optional, for the wire_skin demos
# https://github.com/cwant/wire_skin
is_wire_skin_loaded = False
try:
    from wire_skin import WireSkin
    is_wire_skin_loaded = True
except ImportError:
    print('Could not load wire_skin, some demoes skipped')


def main():
    BlenderDemo().main()


class BlenderDemo(TessagonCommonDemo):
    def main(self):
        self.create_materials()
        self.create_objects()
        self.update_view()

    def update_view(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'area': area, 'region': region}
                        bpy.ops.view3d.viewnumpad(override, type='FRONT')
                        bpy.ops.view3d.view_all(override)
                        break

    def material_name(self, value, num_values):
        return 'Color-{}-of-{}'.format(value + 1, num_values)

    def diffuse_color(self, value, num_values):
        # Curated colors
        colors = {2: [[1.0, 1.0, 1.0],
                      [0.0, 0.0, 0.3]],
                  3: [[1.0, 1.0, 1.0],
                      [0.1, 0.3, 0.5],
                      [0.0, 0.0, 0.3]],
                  4: [[1.0, 1.0, 1.0],
                      [0.3, 0.5, 0.7],
                      [0.1, 0.3, 0.5],
                      [0.0, 0.0, 0.3]]}
        return colors[num_values][value]

    def create_materials(self):
        # Default material
        if 'DefaultColor' not in bpy.data.materials:
            self.create_material('DefaultColor', [1.0, 0.8, 0.5])

        # Create palletes based on how many different colors the object has
        for num_values in [2, 3, 4]:
            for value in range(num_values):
                name = self.material_name(value, num_values)
                if name in bpy.data.materials:
                    continue
                self.create_material(name, self.diffuse_color(value,
                                                              num_values))

    def create_material(self, name, diffuse_color):
        material = bpy.data.materials.new(name=name)
        material.diffuse_color = diffuse_color
        material.specular_intensity = 0.0
        material.diffuse_intensity = 1.0

    def create_objects(self):
        super().create_objects()

        if is_wire_skin_loaded:
            # WireSkin demo
            self.wire_skin_demo()

    def new_or_create_object(self, name):
        if name in bpy.data.objects:
            object = bpy.data.objects[name]
        else:
            me = bpy.data.meshes.new(name)
            object = bpy.data.objects.new(name, me)
            scn = bpy.context.scene
            scn.objects.link(object)
        return object

    def tessellate(self, f, tessagon_class, **kwargs):
        out_name = kwargs.get('object_name')
        if not out_name:
            out_name = tessagon_class.__name__
            color_pattern = kwargs.get('color_pattern') or None
            if color_pattern is not None:
                out_name += "Color%d" % (color_pattern)

        output_object = self.new_or_create_object(out_name)
        me = output_object.data

        me.materials.clear()

        extra_args = {'function': f,
                      'adaptor_class': BlenderAdaptor}
        tessagon = tessagon_class(**{**kwargs, **extra_args})

        bm = tessagon.create_mesh()

        # To debug:
        # tessagon.inspect()

        num_colors = len(set([face.material_index for face in bm.faces]))
        bm.to_mesh(me)
        output_object.data = me
        output_object.show_wire = True
        output_object.show_all_edges = True

        if num_colors > 1:
            for value in range(num_colors):
                name = self.material_name(value, num_colors)
                material = bpy.data.materials[name]
                me.materials.append(material)
        else:
            material = bpy.data.materials['DefaultColor']
            me.materials.append(material)

        scale = kwargs.get('scale') or None
        if scale is not None:
            output_object.scale = [scale]*3
        location = kwargs.get('position') or None
        if location is not None:
            output_object.location = location
        layer = kwargs.get('layer') or None
        if layer is not None:
            layers = [False] * 20
            # Input layer is 1-based, but array is 0-based
            layers[layer-1] = True
            output_object.layers = layers

        me.update()
        return output_object

    def wire_skin_demo(self):
        position = [-30, 0, 0]
        options = {
            'u_range': [0.0, 1.0],
            'v_range': [0.0, 1.0],
            'u_num': 8,
            'v_num': 20,
            'object_name': 'HexTorusIn',
            'position': position
        }
        ob = self.tessellate(other_torus, HexTessagon, **options)
        name = self.material_name(1, 2)
        material = bpy.data.materials[name]
        ob.data.materials.append(material)

        options = {
            'width': 0.1,
            'height': 0.2,
            'inside_radius': 0.1,
            'outside_radius': 0.1,
            'dist': 0.1,
            'crease': 1.0,
            'displace': 0.15,
            'position': position
        }
        ob = self.wire_to_skin("HexTorusIn", "WireTorusOut", **options)
        name = self.material_name(0, 2)
        material = bpy.data.materials[name]
        ob.data.materials.append(material)

    def wire_to_skin(self, in_name, out_name, **kwargs):
        input_object = bpy.data.objects[in_name]
        output_object = self.new_or_create_object(out_name)

        wire_skin = WireSkin(input_object.data, **kwargs)

        me = wire_skin.create_mesh()
        me.materials.clear()

        output_object.data = me
        location = kwargs.get('position') or None
        if location is not None:
            output_object.location = location

        return output_object
