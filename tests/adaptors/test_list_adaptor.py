import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../..')

from tessagon.adaptors.list_adaptor import ListAdaptor  # noqa: E402


class TestListAdaptor:

    def test_create_empty_mesh(self):
        adaptor = ListAdaptor()
        adaptor.create_empty_mesh()
        assert adaptor.vert_list == []
        assert adaptor.face_list == []
        assert adaptor.color_list == []

    def test_create_vert(self):
        adaptor = ListAdaptor()
        adaptor.create_empty_mesh()
        vert0 = adaptor.create_vert([0.0, 1.0, 2.0])
        assert adaptor.vert_list == [[0.0, 1.0, 2.0]]
        assert vert0 == 0
        vert1 = adaptor.create_vert([3.0, 2.0, 1.0])
        assert adaptor.vert_list == [[0.0, 1.0, 2.0],
                                     [3.0, 2.0, 1.0]]
        assert vert1 == 1

    def test_create_face(self):
        adaptor = ListAdaptor()
        adaptor.create_empty_mesh()
        vert0 = adaptor.create_vert([0.0, 1.0, 2.0])
        vert1 = adaptor.create_vert([3.0, 2.0, 1.0])
        vert2 = adaptor.create_vert([5.0, 4.0, 2.0])
        vert3 = adaptor.create_vert([3.0, 1.0, 0.0])

        face0 = adaptor.create_face([vert0, vert1, vert2])
        assert adaptor.face_list == [[0, 1, 2]]
        assert face0 == 0

        face1 = adaptor.create_face([vert1, vert2, vert3])
        assert adaptor.face_list == [[0, 1, 2],
                                     [1, 2, 3]]
        assert face1 == 1

    def test_initialize_colors(self):
        adaptor = ListAdaptor()
        adaptor.create_empty_mesh()
        vert0 = adaptor.create_vert([0.0, 1.0, 2.0])
        vert1 = adaptor.create_vert([3.0, 2.0, 1.0])
        vert2 = adaptor.create_vert([5.0, 4.0, 2.0])
        vert3 = adaptor.create_vert([3.0, 1.0, 0.0])

        adaptor.create_face([vert0, vert1, vert2])
        adaptor.create_face([vert1, vert2, vert3])

        adaptor.initialize_colors()
        assert adaptor.color_list == [0, 0]

    def test_color_face(self):
        adaptor = ListAdaptor()
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

        assert adaptor.color_list == [2, 0, 1]

    def test_get_mesh(self):
        adaptor = ListAdaptor()
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

        mesh = adaptor.get_mesh()
        assert mesh == {'vert_list': [[0.0, 1.0, 2.0],
                                      [3.0, 2.0, 1.0],
                                      [5.0, 4.0, 2.0],
                                      [3.0, 1.0, 0.0]],
                        'face_list':  [[0, 1, 2],
                                       [1, 2, 3],
                                       [0, 2, 3]],
                        'color_list': [2, 0, 1]}
