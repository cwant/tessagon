from tessagon.adaptors.list_adaptor import ListAdaptor


class SvgAdaptor(ListAdaptor):
    ADAPTOR_OPTIONS = ['svg_root_tag', 'svg_style']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.svg_root_tag = kwargs.get('svg_root_tag', False)
        # Optional: a string with style information
        self.style = kwargs.get('svg_style')

    def get_mesh(self):
        buffer = ""
        if self.svg_root_tag:
            if self.svg_root_tag is True:
                buffer += '<svg xmlns="http://www.w3.org/2000/svg">'
            else:
                buffer += self.svg_root_tag
        buffer += "<g>"
        if self.style:
            buffer += "<style>{}</style>".format(self.style)

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
