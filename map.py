from tile import Tile

class Map():	
	def __init__(self,file_name):
		self.tiles = []
		self.rows = 0
		self.columns = 0
		self.size = 0
		self.start_point = 0
		self.end_point = 0
		
		#Gets the map as an list of lines
		lines = self.get_lines(file_name)
		
		#Sets the column & row values
		self.get_size(lines[0])
		
		#Create tiles with information
		self.create_tiles()
		
		#Sets walls
		self.set_walls(lines)
		
		#Sets the start and end positions
		self.set_start_point(lines[1])
		self.set_end_point(lines[2])
		
	#Inputs the map file as a list
	def get_lines(self,file_name):
		file = open(file_name, 'r')
		lines = file.readlines()
		file.close()
		
		return lines
	
	#Populates the tiles list
	def create_tiles(self):
		for i in range(0,self.size):
			self.tiles.append(Tile())
			
	def get_size(self,line):
		size = line.replace("[","").replace("]","").split(",")
		self.rows = int(size[0])
		self.columns = int(size[1])		
		self.size = self.rows * self.columns
		
	def get_lines(self,file_name):
		lines = None
		while lines is None:
			try:
				file = open(file_name, 'r')
				lines = file.readlines()
				file.close()
			except:
				print('Please enter a valid file:')
				file_name = input()
			
		
		return lines
		
	def set_start_point(self,line):
		start = line.replace("(","").replace(")","").split(",")		
		self.start_point = self.get_point(start[0],start[1])
		self.tiles[self.start_point].is_current_tile = True
	def set_end_point(self,line):
		end = line.replace("(","").replace(")","").split(",")
		self.end_point = self.get_point(end[0],end[1])
		self.tiles[self.end_point].is_end = True
		
	def set_walls(self,lines):
		for i in range(3,len(lines)): #For each line that isn't the size, start or end
			wall_tiles = lines[i].replace("(","").replace(")","").split(",") #Creates list with 4 entries, 0-1 is first tile which should be set outright, 2-3 is the size
			#Sets first tile
			self.tiles[self.get_point(wall_tiles[0],wall_tiles[1])].set_wall()
			
			#Sets tiles to the right
			if int(wall_tiles[2]) > 1:
				for i in range(1,int(wall_tiles[2])):
					self.tiles[self.get_point(wall_tiles[0],wall_tiles[1]) + i].set_wall()
			
			#Sets tiles downwards
			row_index = self.columns
			if int(wall_tiles[3]) > 1:
				for i in range(1,int(wall_tiles[3])):
					self.tiles[self.get_point(wall_tiles[0],wall_tiles[1]) + row_index].set_wall()
					if int(wall_tiles[2]) > 1:
						for i in range(1,int(wall_tiles[2])):
							self.tiles[self.get_point(wall_tiles[0],wall_tiles[1]) + row_index+1].set_wall()
					row_index += self.columns
					
	#Loops through each column in each row, printing a character based on its values
	def print_map(self):
		row_index = self.columns - 1 #Keeps track of the value of the last tile in a row, makes it easier to read the map
		for r in range(0,self.rows):
			line_to_print = ""
			for c in range(0,self.columns):
				tile = self.get_point(c,r)
				if self.tiles[tile].is_wall == True:
					line_to_print += "#"
				elif self.tiles[tile].is_end == True:
					line_to_print += "X"
				elif self.tiles[tile].is_current_tile == True:
					line_to_print += "O"	
				elif self.tiles[tile].is_expanded == True:
					line_to_print += "+"
				else:
					line_to_print += "@"
					
			line_to_print += " " + str(row_index)
			row_index += self.columns
			print (line_to_print)

	#Gets the column and row that corrisponds with an list value
	def get_2D(self,point):
		rows = 0
		value = []
		
		#Each row is made up of x number of columns, 
		#I get the rows by subtracting the columns as tiles increment horizontally, 
		#and what is left is how many columns there are.
		while point >= self.columns:
			rows = rows + 1
			point = point - self.columns
		
		value.append(point)
		value.append(rows)
		return value
		
	#Gets the value for a tile in the tiles list that corrisponds with a tile with cordinates
	def get_point(self,column,row):
		return (self.columns * int(row)) + int(column)
			