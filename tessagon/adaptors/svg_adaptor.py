from colorsys import rgb_to_hsv, hsv_to_rgb
from random import uniform
from tessagon.adaptors.list_adaptor import ListAdaptor


def _str_to_rgba(color_str):
    if color_str[0] == '#':
        return _hex_to_rgba(color_str)
    list_str = color_str.translate({ord(i): None for i in 'rgba() '}).\
        split(',')
    if len(list_str) in [3, 4]:
        list_float = [float(c) for c in list_str]
        for i in range(3):
            list_float[i] = (list_float[i] / 255.0)
        return list_float

    raise ValueError('Unrecognized color: {}'.format(color_str))


def _hex_to_rgba(hex):
    if len(hex) < 8:
        hex = hex + 'FF'
    rgba = []
    for i in (1, 3, 5, 7):
        decimal = int(hex[i:i+2], 16)
        rgba.append(decimal / 255)
    return list(rgba)


def _rgba_to_fill_style(r, g, b, a=1.0):
    rgba = [round(255 * c) for c in [r, g, b]] + [a]
    return 'fill:rgb({},{},{});fill-opacity:{};'.format(*rgba)


def _unit_clamp(v):
    if v < 0.0:
        return 0.0
    elif v > 1.0:
        return 1.0
    return v


class SvgAdaptor(ListAdaptor):
    ADAPTOR_OPTIONS = ['svg_root_tag', 'svg_style',
                       'svg_fill_color', 'svg_fill_colors',
                       'svg_stroke_color', 'svg_stroke_width',
                       'svg_randomize_h', 'svg_randomize_s',
                       'svg_randomize_v']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.svg_root_tag = kwargs.get('svg_root_tag', False)
        # Optional: a string with style information
        self.style = kwargs.get('svg_style')
        self.svg_fill_colors = kwargs.get('svg_fill_colors')
        self.svg_fill_color = kwargs.get('svg_fill_color')
        self.svg_stroke_color = kwargs.get('svg_stroke_color')
        self.svg_stroke_width = kwargs.get('svg_stroke_width')

        self.svg_randomize_h = kwargs.get('svg_randomize_h')
        self.svg_randomize_s = kwargs.get('svg_randomize_s')
        self.svg_randomize_v = kwargs.get('svg_randomize_v')

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

        buffer += self.make_faces()

        buffer += "</g>\n"
        if self.svg_root_tag:
            buffer += "</svg>\n"

        return buffer

    def make_faces(self):
        buffer = ""
        if self.svg_fill_colors:
            for i in range(len(self.face_list)):
                face = self.face_list[i]
                color_index = self.color_list[i]
                fill_color = self.svg_fill_colors[color_index]
                buffer += self.make_face(face, fill_color)
        else:
            for face in self.face_list:
                buffer += self.make_face(face)

        return buffer

    def group_style(self):
        style = ""
        if self.svg_stroke_color:
            style += 'stroke:{};'.format(self.svg_stroke_color)
        if self.svg_stroke_width:
            style += "stroke-width:{};".\
                format(self.svg_stroke_width)
        if self.svg_fill_color:
            style += self._randomize_fill_style(self.svg_fill_color)
        if len(style) > 0:
            style = ' style="{}"'.format(style)
        return style

    def make_face(self, face, fill_color=None):
        style = ''
        if fill_color:
            style = 'style="{}"'.format(self._randomize_fill_style(fill_color))

        verts = [self.vert_list[v] for v in face]
        points_string = \
            ' '.join(["{},{}".format(vert[0],
                                     vert[1]) for vert in verts])
        return '<polygon {} points="{}" />'.format(style, points_string)

    def _randomize_fill_style(self, rgba_hex):
        if rgba_hex == 'none':
            return 'fill:none;'

        if not (self.svg_randomize_h or self.svg_randomize_s or
                self.svg_randomize_v):
            return 'fill:{};'.format(rgba_hex)

        rgba = _str_to_rgba(rgba_hex)
        (h, s, v) = rgb_to_hsv(*rgba[0:3])
        a = rgba[3]

        if self.svg_randomize_h:
            lower = _unit_clamp(h - self.svg_randomize_h)
            upper = _unit_clamp(h + self.svg_randomize_h)
            h = uniform(lower, upper)
        if self.svg_randomize_s:
            lower = _unit_clamp(s - self.svg_randomize_s)
            upper = _unit_clamp(s + self.svg_randomize_s)
            s = uniform(lower, upper)
        if self.svg_randomize_v:
            lower = _unit_clamp(v - self.svg_randomize_v)
            upper = _unit_clamp(v + self.svg_randomize_v)
            v = uniform(lower, upper)

        return _rgba_to_fill_style(*(list(hsv_to_rgb(h, s, v)) + [a]))
