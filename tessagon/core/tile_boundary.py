# TileBoundarys describe the boundaries of a tile.
# They are a list of features on a boundary,
# always listed in counter-clockwise order.
# Features are strings, and have the values:
#   Vertices: 'vert' (if only one vert), 'vert-1', 'vert-2', etc.
#   'split' (this describes if an edge crosses a boundary,
#            without connecting to a vert on the boundary)
#   'tangent-split' this describes a split on a corner where neither vertex
#          of the edge is in the tile
#   'edge' if an edge goes along the boundary (not crossing it)
#   Faces: 'face' (if only one face), 'face-1', 'face-2', etc
#   Only vertices and faces are directly used for connecting to neighboring
#   tiles,
#   split and edge are there to ensure the boundary is consistenent
#   with neighboring tiles, and sometimes to help figure out how faces
#   are constructed


class BoundaryBase:
    TOLERANCE = 0.0000001

    SIDES = ['top', 'left', 'bottom', 'right']
    INVERSES = {'top': 'bottom',
                'left': 'right',
                'bottom': 'top',
                'right': 'left'}
    ROTATIONS = {'top': 'left',
                 'left': 'bottom',
                 'bottom': 'right',
                 'right': 'top'}

    def invert_side(self, key):
        return self.INVERSES[key]

    def rotate_side(self, key):
        return self.ROTATIONS[key]

    def tile_rotate_side(self, side):
        if self.tile.rotate == 90:
            return self.rotate_side(side)
        elif self.tile.rotate == 180:
            return self.invert_side(side)
        elif self.tile.rotate == 270:
            return self.rotate_side(self.invert_side(side))
        return side


class SharedVert(BoundaryBase):

    def __init__(self, tile, side, feature, index_keys,
                 uv, **kwargs):
        self.tile = tile

        self.side = self.tile_rotate_side(side)

        self.feature = feature
        self.index_keys = index_keys
        self.uv = uv
        self.kwargs = kwargs

        self.tiles = []
        self.vert_index_keys = []

        self.u_boundary = kwargs.get('u_boundary', False)
        self.v_boundary = kwargs.get('v_boundary', False)

        self.tile.boundary.values[self.side][feature] = self

    def calculate_vert(self):
        vert = self.tile._get_vert(self.index_keys)
        if vert:
            return vert

        uvs = self.calculate_vert_uvs()
        if uvs is None:
            return None

        # uv = [0, 0]
        # if self.u_boundary:
        #     uv[0] = uvs[0][0]
        # else:
        #     uv[0] = sum([uv[0] for uv in uvs]) / len(uvs)
        # if self.v_boundary:
        #     uv[1] = uvs[0][1]
        # else:
        #     uv[1] = sum([uv[1] for uv in uvs]) / len(uvs)

        # TODO: figure out the above, causes occasional defects
        uv = uvs[0]

        vert = self.tile.make_vert(self.index_keys, uv)
        for i in range(len(self.tiles)):
            tile = self.tiles[i]
            index_keys = self.vert_index_keys[i]
            tile.set_equivalent_vert(index_keys, vert)

        return vert

    def is_corner(self):
        prototype_side = self.tile.boundary.prototype[self.side]
        if self.feature in [prototype_side[0], prototype_side[-1]]:
            return True

        return False

    def calculate_corner(self, tile, side, is_first_on_side):
        if tile is None:
            return

        index = -1
        if is_first_on_side:
            index = 0
        other_feature = tile.boundary.prototype[side][index]
        other_shared_vert = tile.boundary.values[side][other_feature]
        if other_shared_vert is None:
            return

        self.tiles.append(tile)
        self.vert_index_keys.append(other_shared_vert.index_keys)

    def calculate_corner_uvs(self):
        prototype_side = self.tile.boundary.prototype[self.side]

        is_first_on_side = (self.feature == prototype_side[0])

        next_side = self.side
        prev_side = self.rotate_side(self.side)
        next_tile = self.tile.neighbors[next_side]
        prev_tile = self.tile.neighbors[prev_side]

        opposite_tile = None
        if next_tile is not None:
            opposite_tile = next_tile.neighbors[prev_side]
        if opposite_tile is None and prev_tile is not None:
            opposite_tile = prev_tile.neighbors[next_side]

        side = self.rotate_side(self.side)
        self.calculate_corner(next_tile, side, is_first_on_side)
        side = self.rotate_side(side)
        self.calculate_corner(opposite_tile, side, is_first_on_side)
        side = self.rotate_side(side)
        self.calculate_corner(prev_tile, side, is_first_on_side)

        return [self.uv]

    def calculate_vert_uvs(self, first_shared_vert=None):
        if first_shared_vert == self:
            return []

        if first_shared_vert is None:
            first_shared_vert = self

            if self.is_corner():
                return self.calculate_corner_uvs()

        other_shared_vert = \
            self.tile.boundary.get_other_value(self.side,
                                               self.feature)

        uvs = [self.uv]
        if other_shared_vert is not None:
            verts = other_shared_vert.calculate_vert_uvs(first_shared_vert)
            uvs.extend(verts)

            first_shared_vert.tiles.\
                append(other_shared_vert.tile)
            first_shared_vert.vert_index_keys.\
                append(other_shared_vert.index_keys)

        return uvs


class SharedFace(BoundaryBase):
    def __init__(self, tile, side, feature, index_keys,
                 vert_index_keys_list, **kwargs):
        self.tile = tile
        self.side = self.tile_rotate_side(side)

        self.feature = feature
        self.index_keys = index_keys
        self.vert_index_keys_list = vert_index_keys_list
        self.kwargs = kwargs

        self.verts = []
        self.tiles = []
        self.face_index_keys = []

        # For really complex paths ...
        self.next_shared_face = None

        self.tile.boundary.values[self.side][feature] = self

    def __str__(self):
        return "<{} (Tile: {}, {}, {}) index_keys: {}, vert_indices: {}>".\
            format(self.__class__.__name__,
                   self.tile.fingerprint,
                   self.side,
                   self.feature,
                   self.index_keys,
                   self.vert_index_keys_list)

    def calculate_face(self):
        if self.kwargs.get('indirect') is True:
            return None

        face = self.tile._get_face(self.index_keys)
        if face is not None:
            return face

        self.verts = []
        self.tiles = []
        self.face_index_keys = []

        verts = self.calculate_face_verts()
        if verts is None:
            return None

        face = self.tile.make_face(self.index_keys, verts, **self.kwargs)
        for i in range(len(self.tiles)):
            tile = self.tiles[i]
            index_keys = self.face_index_keys[i]
            tile.set_equivalent_face(index_keys, face)

    def is_boundary(self, vert_index):
        return (type(vert_index) == list and vert_index[0] == ["boundary"])

    def get_other_shared_face(self, vert_index):
        this_side = self.tile_rotate_side(vert_index[1])
        this_feature = vert_index[2]

        return self.tile.boundary.get_other_value(this_side,
                                                  this_feature)

    def calculate_face_verts(self, first_shared_face=None,
                             next_shared_face=None):
        first_vert = None

        for i in range(len(self.vert_index_keys_list)):
            vert_index = self.vert_index_keys_list[i]
            if first_shared_face is None:
                first_shared_face = self

            if len(first_shared_face.verts) > 0:
                first_vert = first_shared_face.verts[0]

            if self.is_boundary(vert_index):
                other_shared_face = self.get_other_shared_face(vert_index)
                if other_shared_face is None:
                    return None

                if next_shared_face is not None:
                    if other_shared_face.index_keys == \
                       next_shared_face.index_keys:
                        other_shared_face = next_shared_face
                        next_shared_face = None
                else:
                    if self.next_shared_face is not None:
                        next_shared_face = self.next_shared_face

                do_other_verts = True

                if self != first_shared_face and \
                   other_shared_face == first_shared_face:
                    do_other_verts = False

                if do_other_verts:
                    verts = other_shared_face.\
                        calculate_face_verts(first_shared_face,
                                             next_shared_face)

                    if verts is None:
                        return None

                    first_shared_face.tiles.append(other_shared_face.tile)
                    first_shared_face.face_index_keys.\
                        append(other_shared_face.index_keys)

                    for vert in verts:
                        if vert == first_vert:
                            return first_shared_face.verts

                        if len(first_shared_face.verts) > 0:
                            # Watch out for doubles on adjacent tiles
                            if vert != first_shared_face.verts[-1]:
                                self.verts.append(vert)

            else:
                vert = self.tile._get_vert(vert_index)
                if vert is None:
                    return None

                append_vert = True
                if len(first_shared_face.verts) > 0 and \
                   vert == first_shared_face.verts[-1]:
                    append_vert = False
                if vert == first_vert:
                    # We done
                    return self.verts
                if first_vert is None:
                    first_vert = vert
                if append_vert:
                    first_shared_face.verts.append(vert)

        return self.verts


class TileBoundary(BoundaryBase):

    def __init__(self, tile, **kwargs):
        self.tile = tile

        self.prototype = {}
        self.values = {}
        self.num_verts = {}
        self.num_faces = {}
        self.rotate = kwargs.get('rotate')

        for side in self.SIDES:
            prototype = kwargs.get(side)
            side = self.tile_rotate_side(side)

            self.prototype[side] = prototype
            self.values[side] = {}

            self.num_verts[side] = 0
            self.num_faces[side] = 0
            for feature in self.prototype[side]:
                self.values[side][feature] = None
                if 'vert' in feature:
                    self.num_verts[side] += 1
                if 'face' in feature:
                    self.num_faces[side] += 1

    def validate(self):
        self._validate_prototype()
        self._validate_neighbor_prototypes()

    def is_last_corner(self, side, feature):
        return (feature == self.prototype[side][-1])

    def is_approaching_tangent_split(self, side, feature):
        other_tile = self.tile.neighbors[side]
        other_prototype = other_tile.boundary.prototype
        rotate_side = self.rotate_side(side)
        return (feature == self.prototype[side][-2]) and \
            (self.prototype[side][-1] == 'split') and \
            (other_prototype[rotate_side][-1] == 'tangent-split')

    def should_skip_over_tile(self, side, feature):
        other_tile = self.tile.neighbors[side]
        other_prototype = other_tile.boundary.prototype
        invert_side = self.invert_side(side)
        return (feature == self.prototype[side][1]) and \
            (self.prototype[side][0] == 'split') and \
            (other_prototype[invert_side][-1] == 'tangent-split')
        pass

    def get_other_value(self, side, feature):
        other_tile = self.tile.neighbors[side]
        if other_tile is None:
            return None

        other_prototype = other_tile.boundary.prototype
        other_values = other_tile.boundary.values
        rotate_side = self.rotate_side(side)
        invert_side = self.invert_side(side)
        rotate_invert_side = self.rotate_side(invert_side)

        # Corners are special, everything is counter-clockwise
        # Corners with a split/tangent-split can also be special
        # This is confusing, some more information here:
        # https://raw.githubusercontent.com/cwant/tessagon/master/documentation/code/tangent-split.svg

        if self.is_last_corner(side, feature):
            other_side = rotate_side
            other_feature = other_tile.boundary.prototype[other_side][-1]
        elif self.is_approaching_tangent_split(side, feature):
            other_side = rotate_side
            other_feature = other_tile.boundary.prototype[other_side][-2]
        elif self.should_skip_over_tile(side, feature):
            # Skip to the tile after the next one
            other_tile = other_tile.neighbors[rotate_invert_side]
            if other_tile is None:
                return None
            other_prototype = other_tile.boundary.prototype
            other_values = other_tile.boundary.values
            other_side = rotate_side
            other_feature = other_prototype[other_side][-2]
        else:
            other_side = self.invert_side(side)
            other_feature = self.get_other_feature(side, feature)

        return other_values[other_side][other_feature]

    def get_other_feature(self, side, feature):
        # If the side is 'left' and the feature is 'face-m',
        # we return the boundary with side 'right'
        # and feature 'face-(n-m+1)' from the left tile.
        if feature in ['vert', 'face', 'edge', 'split', 'tangent-split']:
            return feature

        (feature_type, num) = feature.split('-')
        if 'vert' in feature:
            num = self.num_verts[side] - int(num) + 1
        else:
            num = self.num_faces[side] - int(num) + 1

        return '{}-{}'.format(feature_type, num)

    def get_shared_verts(self):
        out = []
        for side in self.SIDES:
            for feature in self.values[side]:
                if 'vert' not in feature:
                    continue
                if self.values[side][feature] is None:
                    continue
                out.append(self.values[side][feature])

        return out

    def get_shared_faces(self):
        out = []
        for side in self.SIDES:
            for feature in self.values[side]:
                if self.values[side][feature] is None:
                    continue
                if 'face' not in feature:
                    continue
                out.append(self.values[side][feature])

        return out

    def _validate_prototype(self):
        for key in self.prototype:
            self._validate_side(self.prototype[key])
        self._validate_corners()

    def _validate_side(self, side):
        self._validate_vert_features(side)
        self._validate_face_features(side)
        self._validate_other_features(side)

    def _validate_vert_features(self, side):
        verts = list(filter(lambda x: 'vert' in x,
                            side))
        if len(verts) == 1:
            # Make sure this is the only vert
            if verts[0] != 'vert':
                raise ValueError('Boundary has one vert not named "vert"')
        elif len(verts) > 1:
            vert_names = \
                ['vert-{}'.format(n) for n in range(1, len(verts) + 1)]
            for vert_name in vert_names:
                if vert_name not in verts:
                    ValueError('{} verts in boundary, '
                               'but {} not one of them'.
                               format(len(verts), vert_name))

    def _validate_face_features(self, side):
        # TODO: This might be the least DRY code in the history of mankind,
        # but how to make it more abstract without making it a confusing mess?
        faces = list(filter(lambda x: 'face' in x,
                            side))
        if len(faces) == 1:
            # Make sure this is the only face
            if faces[0] != 'face':
                raise ValueError('Boundary has one face not named "face"')
        elif len(faces) > 1:
            face_names = ['face-{}'.format(n) for n in
                          range(1, len(faces) + 1)]
            for face_name in face_names:
                if face_name not in faces:
                    ValueError('{} faces in boundary, '
                               'but {} not one of them'.
                               format(len(faces), face_name))

    def _validate_other_features(self, side):
        for key in side:
            if key not in ['edge', 'split', 'tangent-split']:
                if 'vert' not in key and 'face' not in key:
                    ValueError('{} is not a valid boundary feature'.
                               format(key))

    def _validate_neighbor_prototypes(self):
        for side in ['top', 'left', 'bottom', 'right']:
            other_tile = self.tile.neighbors[side]
            if other_tile:
                other_side = self.invert_side(side)
                other_prototype = other_tile.boundary.prototype[other_side]

                if self.clean_prototype(other_prototype) != \
                   self.clean_prototype(self.reverse_prototype(side)):
                    this_class = self.tile.__class__.__name__
                    other_class = other_tile.__class__.__name__
                    raise ValueError('{}/{} tile boundary is '
                                     'inconsistent: {}/{}'.
                                     format(side, other_side,
                                            this_class, other_class))

    def clean_prototype(self, prototype):
        out = []
        for feature in prototype:
            if feature == 'tangent-split':
                feature = 'split'
            out.append(feature)
        return out

    def reverse_prototype(self, side):
        out = []

        for feature in reversed(self.prototype[side]):
            out.append(self.get_other_feature(side, feature))

        return out

    def _validate_corners(self):
        # Light version ... (could check 'face-n'/'vert-n' values)
        for i in range(len(self.SIDES)):
            this_side = self.SIDES[i]
            next_side = self.SIDES[(i+1) % 4]

            # Is the last item in this side compatible
            # with the first item in the next side?
            this_corner = self.prototype[this_side][-1]
            next_corner = self.prototype[next_side][0]
            okay = True
            if ('face' in this_corner) and ('face' not in next_corner):
                okay = False
            if ('vert' in this_corner) and ('vert' not in next_corner):
                okay = False
            if (this_corner == 'edge') and (next_corner != 'split'):
                okay = False
            if (this_corner == 'split') and (next_corner not in
                                             ['edge', 'split']):
                okay = False
            if (this_corner == 'tangent-split') and \
               (next_corner != 'tangent-split'):
                okay = False

            if not okay:
                raise ValueError('Bad {}/{} corner in boundary: {}/{}'.
                                 format(this_side, next_side,
                                        this_corner, next_corner))
