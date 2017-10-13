from tessagon.core.tile import Tile

class EquivalentCornersTile(Tile):
  def init_faces(self):
    return { 'middle': None,
             'lefttop': None,
             'leftbottom': None,
             'rightbottom': None,
             'righttop': None }

  def calculate_faces(self):
    self.middle_face()
    self.lefttop_face()
    self.leftbottom_face()
    self.rightbottom_face()
    self.righttop_face()

  def leftbottom_face(self):
    tile = self.get_neighbor_path(['bottom'])
    if not tile:
      return None
    tile.lefttop_face()

  def rightbottom_face(self):
    tile = self.get_neighbor_path(['bottom', 'right'])
    if not tile:
      return None
    tile.lefttop_face()

  def righttop_face(self):
    tile =  self.neighbors['right']
    if not tile:
      return None
    tile.lefttop_face()
