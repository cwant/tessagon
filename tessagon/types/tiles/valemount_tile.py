from tessagon.core.tile import Tile

#    o--o--o--o    1,2,3,4
#    |..|.....|
#    o..o--o--o    5,6,7,8
# ^  |..|..|..|
# |  o--o--o..o    9,10,11,12
# |  |.....|..|
# |  o--o--o--o    13,14,15,16
# V
#   U --->


class ValemountTile(Tile):
    BOUNDARY = dict(
        top=['vert-1', 'edge', 'vert-2', 'edge', 'vert-3',
             'edge', 'vert-4'],
        left=['vert-1', 'edge', 'vert-2', 'edge', 'vert-3',
              'edge', 'vert-4'],
        bottom=['vert-1', 'edge', 'vert-2', 'edge', 'vert-3',
                'edge', 'vert-4'],
        right=['vert-1', 'edge', 'vert-2', 'edge', 'vert-3',
               'edge', 'vert-4']
    )

    uv_ratio = 1.0

    def __init__(self, tessagon, **kwargs):
        super().__init__(tessagon, **kwargs)
        self.u_symmetric = False
        self.v_symmetric = False

    def init_verts(self):
        # Naming stuff is hard ...
        return {1: None,
                2: None,
                3: None,
                4: None,
                5: None,
                6: None,
                7: None,
                8: None,
                9: None,
                10: None,
                11: None,
                12: None,
                13: None,
                14: None,
                15: None,
                16: None}

    def init_faces(self):
        return {'A': None,
                'B': None,
                'C': None,
                'D': None,
                'E': None}

    def calculate_verts(self):
        # Top row
        self.add_vert(1,
                      0, 1,
                      top_boundary='vert-4')

        self.add_vert(2,
                      1/3.0, 1,
                      top_boundary='vert-3')

        self.add_vert(3,
                      2/3.0, 1,
                      top_boundary='vert-2')

        self.add_vert(4,
                      1, 1,
                      right_boundary='vert-4')

        # Next row
        self.add_vert(5,
                      0, 2/3.0,
                      left_boundary='vert-2')

        self.add_vert(6,
                      1/3.0, 2/3.0)

        self.add_vert(7,
                      2/3.0, 2/3.0)

        self.add_vert(8, 1, 2/3.0,
                      right_boundary='vert-3')

        # Next row
        self.add_vert(9,
                      0, 1/3.0,
                      left_boundary='vert-3')

        self.add_vert(10,
                      1/3.0, 1/3.0)

        self.add_vert(11,
                      2/3.0, 1/3.0)

        self.add_vert(12,
                      1, 1/3.0,
                      right_boundary='vert-2')

        # Bottom row
        self.add_vert(13,
                      0, 0,
                      left_boundary='vert-4')

        self.add_vert(14,
                      1/3.0, 0,
                      bottom_boundary='vert-2')

        self.add_vert(15,
                      2/3.0, 0,
                      bottom_boundary='vert-3')

        self.add_vert(16,
                      1, 0,
                      bottom_boundary='vert-4')

    def calculate_faces(self):
        self.add_face('A',
                      [5, 9, 10, 6, 2, 1])
        self.add_face('B',
                      [6, 7, 8, 4, 3, 2])
        self.add_face('C',
                      [13, 14, 15, 11, 10, 9])
        self.add_face('D',
                      [11, 15, 16, 12, 8, 7])
        self.add_face('E',
                      [10, 11, 7, 6])

    def color_pattern1(self):
        self.color_paths([
            ['E']
        ], 1, 0)
