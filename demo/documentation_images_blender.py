# Don't run me directly!
# Load the file demo/tessagon_demo.blend into blender, it will run me
# Run the demo first to create the objects, and I will render them

# TODO: make this work with Blender >= 2.8
import math
import re
import os
import bpy

from tessagon import TessagonDiscovery

class DocumentationImages:
    CLASS_NAMES = {
        'regular':  ['SquareTessagon',
                     'HexTessagon',
                     'TriTessagon'],

        'archimedean': ['OctoTessagon',
                        'HexTriTessagon',
                        'HexSquareTriTessagon',
                        'DodecaTessagon',
                        'SquareTriTessagon',
                        'SquareTri2Tessagon',
                        'DodecaTriTessagon',
                        'BigHexTriTessagon'],

        'laves': ['RhombusTessagon',
                  'FloretTessagon',
                  'DissectedSquareTessagon',
                  'DissectedTriangleTessagon',
                  'DissectedHexQuadTessagon',
                  'DissectedHexTriTessagon',
                  'PentaTessagon',
                  'Penta2Tessagon'],

        'non_edge': ['PythagoreanTessagon',
                     'BrickTessagon',
                     'WeaveTessagon',
                     'HexBigTriTessagon',
                     'ZigZagTessagon',
                     'ValemountTessagon',
                     'CloverdaleTessagon',
                     'HokusaiParallelogramsTessagon'],

        'non_convex': ['StanleyParkTessagon',
                       'IslamicHexStarsTessagon',
                       'IslamicStarsCrossesTessagon'],

        'non_manifold': ['HokusaiHashesTessagon']
    }
    CLASSES = { tiling_type: list(map(TessagonDiscovery.get_class, names)) \
                    for (tiling_type, names) in CLASS_NAMES.items() }
    CLASS_LIST = sum(CLASSES.values(), [])

    def __init__(self):
        # Keep track of what to write for each classes documentation page
        # key is the tessagon name
        self.page_parts = { k.__name__: {}  for k in self.CLASS_LIST}

    def main(self):
        self.setup_render_scene()
        self.render_tessagons(self.CLASS_LIST)
        self.setup_thumbnail_scene()
        self.render_thumbnails(self.CLASS_LIST)
        self.write_markdown(self.CLASSES)

    def setup_render_scene(self):
        scn = bpy.context.scene
        self.set_layer(scn)
        scn.render.resolution_x = 400
        scn.render.resolution_y = 300
        scn.render.resolution_percentage = 100
        scn.render.use_freestyle = True
        scn.render.line_thickness = 0.5
        scn.render.layers[0].freestyle_settings.linesets[0].select_edge_mark = True
        scn.render.layers[0].freestyle_settings.linesets[0].select_material_boundary = True
        scn.render.layers[0].freestyle_settings.linesets[0].select_silhouette = False
        scn.render.layers[0].freestyle_settings.linesets[0].select_crease = False

        if 'Camera' not in bpy.data.objects:
            cam_data = bpy.data.cameras.new('Camera')
            camera = bpy.data.objects.new('Camera', cam_data)
        else:
            camera = bpy.data.objects['Camera']
        if 'Camera' not in scn.objects:
            scn.objects.link(camera)
        self.set_layer(camera)
        camera.location = [0, -17, 0]
        camera.rotation_euler = [math.pi/2, 0, 0]
        scn.camera = camera

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'area': area, 'region': region}
                        bpy.ops.view3d.snap_cursor_to_center(override)
                        area.spaces[0].pivot_point = 'CURSOR'
                        bpy.ops.view3d.viewnumpad(override, type='CAMERA')
                        camera.select = True
                        for ob in scn.objects:
                            if ob != camera:
                                ob.select = False
                        scn.objects.active = camera
                        bpy.ops.transform.rotate(override, value=-math.pi/6,
                                                 axis=(1, 0, 0))
                        break

        lamps = {}
        for name in ['MainLight', 'FillLight', 'BackLight']:
            if name not in bpy.data.objects:
                lamp_data = bpy.data.lamps.new(name, 'POINT')
                lamps[name] = bpy.data.objects.new(name, lamp_data)
                scn.objects.link(lamps[name])
            else:
                lamps[name] = bpy.data.objects[name]
            if name not in scn.objects:
                scn.objects.link(lamps[name])
            self.set_layer(lamps[name])
        lamps['MainLight'].location = [-5, -10, 5]
        lamps['FillLight'].location = [10, -30, 5]
        lamps['BackLight'].location = [-10, 50, 5]

        lamps['MainLight'].data.energy = 5.0
        lamps['FillLight'].data.energy = 5.0

        scn.world.horizon_color = [1, 1, 1]


    def setup_thumbnail_scene(self):
        scn = bpy.context.scene
        self.set_layer(scn)
        scn.render.resolution_x = 100
        scn.render.resolution_y = 75
        camera = bpy.data.objects['Camera']
        camera.location = [0, -17, 0]
        camera.rotation_euler = [math.pi/2, 0, 0]
        camera.data.lens = 120.0


    def set_layer(self, thing, layer=1):
        thing.layers[layer] = True
        for i in range(20):
            if i != layer:
                thing.layers[i] = False


    def render_tessagons(self, class_list):
        for cls in class_list:
            self.render_class(cls)

        self.render_object(['HexTorusIn', 'WireTorusOut'],
                           filename='wire_skin.png', mark_edges=False)


    def render_thumbnails(self, class_list):
        for cls in class_list:
            self.render_class(cls, thumbnail=True)

    def render_class(self, cls, **kwargs):
        class_name = cls.__name__
        page_parts = {}

        filename = self.render_object(class_name, **kwargs)

        if kwargs.get('thumbnail'):
            page_parts['thumbnail'] = filename
            self.page_parts[class_name].update(page_parts)

            return

        page_parts['image'] = filename

        color_page_parts = []
        for i in range(cls.num_color_patterns()):
            object_name = "%sColor%d" % (class_name, i+1)
            filename = self.render_object(object_name, **kwargs)
            color_page_parts.append(filename)
        if len(color_page_parts) > 0:
            page_parts['color_patterns'] = color_page_parts

        parameter_page_parts = {}
        for parameter in cls.metadata.extra_parameters:
            parameter_info = cls.metadata.extra_parameters[parameter]
            parameter_page_part = {'parameter': parameter,
                                    'parameter_info': parameter_info}
            if parameter_info['type'] == 'float':
                values = dict(
                    low=(parameter_info['default'] + parameter_info['min']) / 2.0,
                    high=(parameter_info['default'] + parameter_info['max']) / 2.0)
                for value_name in values:
                    value = round(values[value_name], 2)
                    object_name = "{}-{}={}".format(class_name, parameter, value)
                    filename = self.render_object(object_name, **kwargs)
                    parameter_page_part[value_name] = dict(
                        value=value,
                        filename=filename
                    )
                parameter_page_parts[parameter] = parameter_page_part
        if len(parameter_page_parts) > 0:
            page_parts['extra_parameters'] = parameter_page_parts

        self.page_parts[class_name].update(page_parts)

    def render_object(self, name, **kwargs):
        if isinstance(name, list):
            names = name
        else:
            names = [name]
        objects = [self.get_object(name) for name in names]
        for object in objects:
            if not object:
                return

        for object in objects:
            self.prepare_object_for_render(object, **kwargs)
            self.set_layer(object)

        # Writing PNG to /tmp or DOCUMENTATION_IMAGES_DIR
        dir = os.getenv('DOCUMENTATION_IMAGES_DIR') or '/tmp'
        filename = kwargs.get('filename') or self.class_to_snakecase(names[0])
        if kwargs.get('thumbnail'):
            filename += '_thumb'
        path = "%s/%s" % (dir, filename)

        print("Rendering and writing: %s" % path)
        bpy.context.scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
        for object in objects:
            self.set_layer(object, 0)

        return '{}.png'.format(filename)

    def prepare_object_for_render(self, object, **kwargs):
        object.location = [0, 0, 0]

        mesh = object.data
        mesh.show_double_sided = True
        mesh.use_auto_smooth = True
        mesh.auto_smooth_angle = math.pi / 6
        mark_edges = kwargs.get('mark_edges')
        if mark_edges is None:
            mark_edges = True
        if mark_edges:
            for edge in mesh.edges:
                edge.use_freestyle_mark = True
        mesh.update()


    def class_to_snakecase(self, cls):
        # Handle both class and string class name
        class_name = cls
        if type(cls) != str:
            class_name = cls.__name__
        # Convert class name to camelcase
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', class_name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def get_object(self, name):
        if name not in bpy.data.objects:
            print("%s not found, skipping!" % (name))
            return None
        return bpy.data.objects[name]

    def write_markdown(self, classes):
        # We just write the list part of the README.md to another
        # file because we don't want to clobber the whole file
        # (unfortunately have to copy/paste this list by hand)
        list_fp = open(self.list_markdown_filename(), 'w')

        # TODO: maybe move this mapping to TessagonDiscovery
        key_to_name = {
            'regular': 'Regular tilings',
            'archimedean': 'Archimedean tilings',
            'laves': 'Laves tilings',
            'non_edge': 'Non-edge-to-edge tilings',
            'non_convex': 'Non-convex tilings',
            'non_manifold': 'Non-manifold tilings'
        }
        # darn, keys aren't ordered by insertion
        for key in ['regular', 'archimedean', 'laves',
                    'non_edge', 'non_convex', 'non_manifold']:
            list_fp.write("### %s\n\n" % key_to_name[key])

            for cls in classes[key]:
                self.write_class_to_list_file(list_fp, cls)
                self.write_class_markdown_file(cls)

            list_fp.write("\n")
        list_fp.close()

    def list_markdown_filename(self):
        # Typically write this to /tmp
        dir = os.getenv('DOCUMENTATION_DIR') or '/tmp'
        return "%s/README_tessagon_list.md" % (dir)

    def markdown_filename(self, cls):
        return "documentation/types/{}.md".\
            format(self.class_to_snakecase(cls))

    def thumbnail_filename(self, cls):
        class_name = cls.__name__
        page_parts = self.page_parts[class_name]
        return "documentation/images/types/{}".format(page_parts['thumbnail'])

    def color_pattern_filename(self, cls, pattern_number):
        class_name = cls.__name__
        page_parts = self.page_parts[class_name]
        return \
            "../images/types/{}".format(page_parts['color_patterns'][pattern_number])

    def extra_parameter_filename(self, cls, parameter, value_name):
        class_name = cls.__name__
        page_parts = self.page_parts[class_name]
        parameter_part = page_parts['extra_parameters'][parameter][value_name]
        return \
            "../images/types/{}".format(parameter_part['filename'])

    def extra_parameter_value(self, cls, parameter, value_name):
        class_name = cls.__name__
        page_parts = self.page_parts[class_name]
        parameter_part = page_parts['extra_parameters'][parameter][value_name]
        return parameter_part['value']

    def write_class_to_list_file(self, list_fp, cls):
        class_name = cls.__name__
        num_patterns = cls.num_color_patterns()
        num_extra_parameters = cls.num_extra_parameters()

        extra_info = []
        if num_patterns > 0:
            if num_patterns == 1:
                extra_info.append('1 color pattern')
            else:
                extra_info.append('{} color patterns'.format(num_patterns))
        if num_extra_parameters > 0:
            if num_extra_parameters == 1:
                extra_info.append('1 extra parameter')
            else:
                extra_info.append('{} extra parameters'.\
                                  format(num_extra_parameters))

        list_fp.write("* [%s](%s)" % (class_name, self.markdown_filename(cls)))
        if len(extra_info) > 0:
            list_fp.write(" ({})".format(', '.join(extra_info)))
        list_fp.write("  \n")
        list_fp.write("  [![%s](%s)](%s)\n" % (class_name,
                                               self.thumbnail_filename(cls),
                                               self.markdown_filename(cls)))

    def write_class_markdown_file(self, cls):
        class_name = cls.__name__
        page_parts = self.page_parts[class_name]
        markdown_file = self.markdown_filename(cls)

        img_file = "../images/types/{}".format(page_parts['image'])

        markdown_fp = open(markdown_file, 'w')
        markdown_fp.write("# `%s`\n\n" % class_name)
        markdown_fp.write("![%s](%s)\n" % (class_name, img_file))

        self.write_class_markdown_file_color_patterns(markdown_fp, cls)
        self.write_class_markdown_file_extra_parameters(markdown_fp, cls)

        markdown_fp.close()

    def write_class_markdown_file_color_patterns(self, markdown_fp, cls):
        class_name = cls.__name__
        num_patterns = cls.num_color_patterns()
        if num_patterns > 0:
            markdown_fp.write("\n## Color patterns\n")
            for i in range(num_patterns):
                alt = "{} color pattern {}".format(class_name, i+1)
                markdown_fp.write("\n### `color_pattern=%d`\n\n" % (i+1))
                markdown_fp.write("![{}]({})\n".\
                                  format(alt, self.color_pattern_filename(cls, i)))

    def write_class_markdown_file_extra_parameters(self, markdown_fp, cls):
        class_name = cls.__name__
        num_extra_parameters = cls.num_extra_parameters()
        if num_extra_parameters > 0:
            markdown_fp.write("\n## Extra parameters\n")
            for parameter in cls.metadata.extra_parameters:
                parameter_info = cls.metadata.extra_parameters[parameter]
                extra_info = ["type: `{}`".format(parameter_info['type']),
                              "default: `{}`".format(parameter_info['default'])]
                if parameter_info.get('min') != None:
                    extra_info.append("minimum: `{}`".\
                                      format(parameter_info['min']))
                if parameter_info.get('max') != None:
                    extra_info.append("maximum: `{}`".\
                                      format(parameter_info['max']))
                markdown_fp.write("\n### `{}` ({})\n".\
                                  format(parameter, ", ".join(extra_info)))

                for value_name in ['low', 'high']:
                    image = self.extra_parameter_filename(cls, parameter, value_name)
                    value = self.extra_parameter_value(cls, parameter, value_name)
                    alt = "{} {}={}".format(class_name, parameter, value)
                    markdown_fp.write("#### `{}={}`\n".format(parameter, value))
                    markdown_fp.write("![{}]({})\n".format(alt, image))


def main():
    DocumentationImages().main()
