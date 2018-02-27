import vtk


class VtkAdaptor:
    def __init__(self, **kwargs):
        self.point_count = 0
        self.face_count = 0
        self.points = None
        self.polys = None
        self.poly_data = None
        self.scalars = None

    def create_empty_mesh(self):
        self.pcoords = vtk.vtkFloatArray()
        self.pcoords.SetNumberOfComponents(3)
        self.points = vtk.vtkPoints()
        self.polys = vtk.vtkCellArray()
        self.poly_data = vtk.vtkPolyData()

    def initialize_colors(self):
        self.scalars = vtk.vtkFloatArray()
        self.scalars.SetNumberOfComponents(1)
        self.scalars.SetNumberOfTuples(self.face_count)

    def create_vert(self, coords):
        self.pcoords.InsertNextTuple3(*coords)
        index = self.point_count
        self.point_count += 1
        return index

    def create_face(self, verts):
        self.polys.InsertNextCell(len(verts), verts)
        index = self.face_count
        self.face_count += 1
        return index

    def color_face(self, face, color_index):
        self.scalars.SetTuple1(face, color_index)

    def finish_mesh(self):
        self.points.SetData(self.pcoords)
        self.poly_data.SetPoints(self.points)
        self.poly_data.SetPolys(self.polys)
        if self.scalars:
            self.poly_data.GetCellData().SetScalars(self.scalars)

    def get_mesh(self):
        return self.poly_data
