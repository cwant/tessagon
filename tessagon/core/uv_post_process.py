from random import random, uniform
from math import sin, cos, pi, radians


def _scale_vert(vert, about, factor):
    diff = [vert[i] - about[i] for i in [0, 1]]
    return [about[i] + factor * diff[i] for i in [0, 1]]


def _rotate_vert(vert, about, theta):
    diff = [vert[i] - about[i] for i in [0, 1]]
    return [about[0] + (cos(theta) * diff[0] - sin(theta) * diff[1]),
            about[1] + (sin(theta) * diff[0] + cos(theta) * diff[1])]


class UVPostProcess:
    def __init__(self, **kwargs):
        self.uv_mesh_maker = None
        self.disjoint_faces = kwargs.get('disjoint_faces', False)

        self.random_vert_offset_radius = \
            kwargs.get('uv_random_vert_offset_radius')

        self.random_face_offset_radius = \
            kwargs.get('uv_random_face_offset_radius')
        if self.random_face_offset_radius:
            self.disjoint_faces = True

        rotate_faces_degrees = kwargs.get('uv_rotate_faces_degrees')
        if rotate_faces_degrees:
            self.rotate_faces_radians = radians(rotate_faces_degrees)
            self.disjoint_faces = True
        else:
            self.rotate_faces_radians = None

        rotate_faces_random_degrees = \
            kwargs.get('uv_rotate_faces_random_degrees')
        if rotate_faces_random_degrees:
            self.rotate_faces_random_radians = \
                radians(rotate_faces_random_degrees)
            self.disjoint_faces = True
        else:
            self.rotate_faces_random_radians = None

        # 1.0 means no scaling
        self.scale_faces = kwargs.get('uv_scale_faces')
        if self.scale_faces:
            self.disjoint_faces = True

        # [min, max]
        self.scale_faces_random_range = \
            kwargs.get('uv_scale_faces_random_range')
        if self.scale_faces_random_range:
            self.disjoint_faces = True

    @property
    def verts(self):
        return self.uv_mesh_maker.verts

    @property
    def faces(self):
        return self.uv_mesh_maker.faces

    def run(self, uv_mesh_maker):
        self.uv_mesh_maker = uv_mesh_maker
        self._make_faces_disjoint()
        self._scale_verts_about_faces()
        self._rotate_verts_about_faces()
        self._random_offset_verts()

    def _make_faces_disjoint(self):
        if not self.disjoint_faces:
            return

        vert_used = {}
        for i in range(len(self.faces)):
            face = self.faces[i]
            new_face = []
            for vert_index in face:
                if vert_index in vert_used:
                    # Gotta make a new vert since this one
                    # is used on a previous face
                    vert = self.verts[vert_index]
                    new_vert = vert.copy()
                    new_vert_index = len(self.verts)
                    self.verts.append(new_vert)
                    new_face.append(new_vert_index)
                else:
                    vert_used[vert_index] = True
                    new_face.append(vert_index)
            self.faces[i] = new_face

    def _scale_verts_about_faces(self):
        if self.scale_faces:
            for face in self.faces:
                self._scale_face_about_centroid(face, self.scale_faces)

        if self.scale_faces_random_range:
            for face in self.faces:
                scale = uniform(*self.scale_faces_random_range)
                self._scale_face_about_centroid(face, scale)

    def _rotate_verts_about_faces(self):
        if self.rotate_faces_radians:
            for face in self.faces:
                self._rotate_face_about_centroid(face,
                                                 self.rotate_faces_radians)

        if self.rotate_faces_random_radians:
            for face in self.faces:
                theta = random() * self.rotate_faces_random_radians
                self._rotate_face_about_centroid(face, theta)

    def _random_offset_verts(self):
        if self.random_face_offset_radius:
            for face in self.faces:
                radius = random() * self.random_face_offset_radius
                theta = 2 * pi * random()
                for vert_index in face:
                    self.verts[vert_index][0] += (radius * cos(theta))
                    self.verts[vert_index][1] += (radius * sin(theta))

        if self.random_vert_offset_radius:
            for i in range(len(self.verts)):
                radius = random() * self.random_vert_offset_radius
                theta = 2 * pi * random()
                self.verts[i][0] += (radius * cos(theta))
                self.verts[i][1] += (radius * sin(theta))

    def _face_centroid(self, face):
        (u, v) = (0, 0)
        for vert_index in face:
            vert = self.verts[vert_index]
            u += vert[0]
            v += vert[1]
        u /= len(face)
        v /= len(face)
        return (u, v)

    def _scale_face_about_centroid(self, face, scale):
        centroid = self._face_centroid(face)
        for vert_index in face:
            vert = self.verts[vert_index]
            new_vert = _scale_vert(vert, centroid, scale)
            self.verts[vert_index] = new_vert

    def _rotate_face_about_centroid(self, face, theta):
        centroid = self._face_centroid(face)
        for vert_index in face:
            vert = self.verts[vert_index]
            new_vert = _rotate_vert(vert, centroid, theta)
            self.verts[vert_index] = new_vert
