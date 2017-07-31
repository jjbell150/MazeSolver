class Tile():
	def __init__(self):
		self.is_wall = False
		self.is_current_tile = False
		self.is_end = False
		self.is_expanded = False
	
	def set_wall(self):
		if self.is_end == False and self.is_current_tile == False: #Minor error checking
			self.is_wall = True
		
		