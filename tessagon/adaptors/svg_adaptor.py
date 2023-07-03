from tessagon.adaptors.list_adaptor import ListAdaptor


class SvgAdaptor(ListAdaptor):
    ADAPTOR_OPTIONS = ['svg_root_tag', 'svg_style',
                       'svg_fill_color', 'svg_fill_colors',
                       'svg_stroke_color', 'svg_stroke_width']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.svg_root_tag = kwargs.get('svg_root_tag', False)
        # Optional: a string with style information
        self.style = kwargs.get('svg_style')
        self.svg_fill_colors = kwargs.get('svg_fill_colors')
        self.svg_fill_color = kwargs.get('svg_fill_color')
        self.svg_stroke_color = kwargs.get('svg_stroke_color')
        self.svg_stroke_width = kwargs.get('svg_stroke_width')

    def get_mesh(self):
        buffer = ""
        if self.svg_root_tag:
            if self.svg_root_tag is True:
                buffer += '<svg xmlns="http://www.w3.org/2000/svg">'
            else:
                buffer += self.svg_root_tag
        buffer += "<g>"

        style = self.make_style()
        if style:
            buffer += "<style>{}</style>".format(style)

        for i in range(len(self.face_list)):
            face = self.face_list[i]
            class_string = ""
            if len(self.color_list) > 0:
                color = self.color_list[i]
                class_string = ' class="color-{}"'.format(color)
            verts = [self.vert_list[v] for v in face]
            points_string = \
                ' '.join(["{},{}".format(vert[0],
                                         vert[1]) for vert in verts])
            buffer += '<polygon points="{}"{} />'.format(points_string,
                                                         class_string)
        buffer += "</g>"
        if self.svg_root_tag:
            buffer += "</svg>"
        return buffer

    def make_style(self):
        if self.style:
            return self.style

        style = ""
        polygon_style = ""
        if self.svg_fill_colors:
            for i in range(len(self.svg_fill_colors)):
                style += '.color-{} {{\n  fill:{};\n}}\n'.\
                    format(i, self.svg_fill_colors[i])
        if self.svg_stroke_color:
            polygon_style += '  stroke:{};\n'.format(self.svg_stroke_color)
        if self.svg_stroke_width:
            polygon_style += "  stroke-width:{};\n".\
                format(self.svg_stroke_width)
        if self.svg_fill_color:
            polygon_style += '  fill:{};\n'.format(self.svg_fill_color)

        if len(polygon_style) > 0:
            style += "polygon {{\n{}}}\n".format(polygon_style)

        if len(style) > 0:
            return style

        return None
