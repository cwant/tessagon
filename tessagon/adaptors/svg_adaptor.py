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
                buffer += '<svg xmlns="http://www.w3.org/2000/svg">\n'
            else:
                buffer += self.svg_root_tag

        buffer += "<g{}>\n".format(self.group_style())

        if self.style:
            buffer += "<style>{}</style>".format(self.style)

        if self.svg_fill_colors:
            color_indices = self.make_color_indices()
            for i in range(len(self.svg_fill_colors)):
                if i not in color_indices:
                    continue
                fill_color = self.svg_fill_colors[i]
                faces = [self.face_list[j] for j in color_indices[i]]
                buffer += self.make_color_group(faces, fill_color)
        else:
            for face in self.face_list:
                buffer += self.make_face(face)

        buffer += "</g>\n"
        if self.svg_root_tag:
            buffer += "</svg>\n"
        return buffer

    def group_style(self):
        style = ""
        if self.svg_stroke_color:
            style += 'stroke:{};'.format(self.svg_stroke_color)
        if self.svg_stroke_width:
            style += "stroke-width:{};".\
                format(self.svg_stroke_width)
        if self.svg_fill_color:
            style += 'fill:{};'.format(self.svg_fill_color)
        if len(style) > 0:
            style = ' style="{}"'.format(style)
        return style

    def make_color_indices(self):
        color_indices = {}
        for i in range(len(self.color_list)):
            color = self.color_list[i]
            if color not in color_indices:
                color_indices[color] = []
            color_indices[color].append(i)

        return color_indices

    def make_color_group(self, faces, fill_color):
        buffer = '<g style="fill:{};">\n'.format(fill_color)
        for face in faces:
            buffer += self.make_face(face)
        buffer += '</g>\n'

        return buffer

    def make_face(self, face):
        verts = [self.vert_list[v] for v in face]
        points_string = \
            ' '.join(["{},{}".format(vert[0],
                                     vert[1]) for vert in verts])
        return '<polygon points="{}" />'.format(points_string)
