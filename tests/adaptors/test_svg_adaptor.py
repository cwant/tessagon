import os
import sys
from html.parser import HTMLParser

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.adaptors.svg_adaptor import SvgAdaptor  # noqa: E402


class SvgToList(HTMLParser):
    # Very basic, enough information to test
    def __init__(self):
        HTMLParser.__init__(self)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        self.parts.append(tag)
        for attr in attrs:
            self.parts.append(attr[0])
            self.parts.append(attr[1])


class TestSvgAdaptor:

    # Note, this is a subclass of ListAdaptor, so see those tests
    # for a more rigourous treatment

    def setup_adaptor(self, adaptor):
        adaptor.create_empty_mesh()
        vert0 = adaptor.create_vert([0.0, 1.0, 2.0])
        vert1 = adaptor.create_vert([3.0, 2.0, 1.0])
        vert2 = adaptor.create_vert([5.0, 4.0, 2.0])
        vert3 = adaptor.create_vert([3.0, 1.0, 0.0])

        face0 = adaptor.create_face([vert0, vert1, vert2])
        adaptor.create_face([vert1, vert2, vert3])
        face2 = adaptor.create_face([vert0, vert2, vert3])

        adaptor.initialize_colors()
        adaptor.color_face(face0, 2)
        adaptor.color_face(face2, 1)

        adaptor.finish_mesh()

    def test_get_mesh(self):
        adaptor = SvgAdaptor()
        self.setup_adaptor(adaptor)
        mesh = adaptor.get_mesh()

        parser = SvgToList()
        parser.feed(mesh)
        parser.close()

        print(parser.parts)
        assert parser.parts == ['g',

                                'polygon', 'points', '0.0,1.0 3.0,2.0 5.0,4.0',
                                'class', 'color-2',

                                'polygon', 'points', '3.0,2.0 5.0,4.0 3.0,1.0',
                                'class', 'color-0',

                                'polygon', 'points', '0.0,1.0 5.0,4.0 3.0,1.0',
                                'class', 'color-1']

    def test_get_mesh_root_tag(self):
        adaptor = SvgAdaptor(svg_root_tag=True)
        self.setup_adaptor(adaptor)
        mesh = adaptor.get_mesh()

        parser = SvgToList()
        parser.feed(mesh)
        parser.close()

        print(parser.parts)
        assert parser.parts == ['svg',
                                'xmlns', 'http://www.w3.org/2000/svg',
                                'g',

                                'polygon', 'points', '0.0,1.0 3.0,2.0 5.0,4.0',
                                'class', 'color-2',

                                'polygon', 'points', '3.0,2.0 5.0,4.0 3.0,1.0',
                                'class', 'color-0',

                                'polygon', 'points', '0.0,1.0 5.0,4.0 3.0,1.0',
                                'class', 'color-1']

    def test_get_mesh_style(self):
        adaptor = SvgAdaptor(svg_style='whatever;')
        self.setup_adaptor(adaptor)
        mesh = adaptor.get_mesh()

        parser = SvgToList()
        parser.feed(mesh)
        parser.close()

        print(parser.parts)
        assert parser.parts == ['g',
                                'style',

                                'polygon', 'points', '0.0,1.0 3.0,2.0 5.0,4.0',
                                'class', 'color-2',

                                'polygon', 'points', '3.0,2.0 5.0,4.0 3.0,1.0',
                                'class', 'color-0',

                                'polygon', 'points', '0.0,1.0 5.0,4.0 3.0,1.0',
                                'class', 'color-1']
