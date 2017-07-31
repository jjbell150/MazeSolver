#First it checks possible moves from the starting position, adding them to a list in an order that fulfils the default direction requirements.
#Then it takes the last value in the list, and explores what options are avaliable to it.
#It does this until there are no options to add to the list, then it removes the path it just took, backtracks one move, and checks if there are now options, effectively expanding the next node.
#It will do this until it finds a branch that has movement options avaliable.
#It won't register nodes until it plans to expand them, increasing efficency. This also prevents nodes from being queued twice.
class Depth_first:
	def __init__(self,map):
		self.map = map
		self.name = 'Depth First'
	
	def valid_move(self,move,current_tile,visited):
		if (current_tile + move) in visited:
			return False
			
		if current_tile + move >= 0 and current_tile + move < len(self.map.tiles): #Check out of bounds
			if self.map.tiles[current_tile + move].is_wall == False: #Check wall collision
				if move == -1:
					if self.map.get_2D(current_tile)[0] == 0: #Stop it from using the left edge
						return False
				elif move == 1:
					if self.map.get_2D(current_tile)[0] == self.map.columns-1: #Stop it from using the right edge
						return False
				#Above the top and below the bottom are both out of bounds and should have already been caught, this is just an added precaution.
				elif move == self.map.columns:
					if self.map.get_2D(current_tile)[1] == self.map.rows-1: #Stop it from using the bottom
						return False
				elif move == -self.map.columns:
					if self.map.get_2D(current_tile)[1] == 0: #Stop it from using the top
						return False
				return True
					
		return False
	
	def find_path(self):
		visited = [] #Keeps track of visited nodes to prevent loops
		path = [] #Keeps track of which directions were taken to print later on
		path_options = [] #Keeps track of how many paths it can take
		current_tile = self.map.start_point #Where it starts
		
		self.map.print_map()
		while current_tile != self.map.end_point:
			print ('---------------------------')
			moved = False
			tries = 0
			
			while moved == False:	
				dead_end = True
				
				if self.valid_move(-self.map.columns,current_tile,visited):
					path_options.append(current_tile -self.map.columns)
					
					dead_end = False
					path.append("up")
				elif self.valid_move(-1, current_tile,visited):
					path_options.append(current_tile -1)
					
					dead_end = False
					path.append("left")
				elif self.valid_move(self.map.columns, current_tile,visited):
					path_options.append(current_tile + self.map.columns)
					
					dead_end = False
					path.append("down")
					
				elif self.valid_move(1, current_tile,visited):
					path_options.append(current_tile + 1)
					
					dead_end = False
					path.append("right")				
				
				self.map.tiles[current_tile].is_current_tile = False
				
				#Remove node from frontier
				if current_tile not in visited:
					visited.append(current_tile)
				
				#If it's a dead end, go backwards one step and loop through again to see if there are now more opportunities. 
				if dead_end == False:
					current_branch = (path_options[-1])
					visited.append(current_branch)
					current_tile = current_branch	
					moved = True
				else:
					if len(path) == 0:
						return ["No path found"],len(visited)

					tries = tries + 1 #Keeps track of how many steps need to be reversed
					path.pop() #Removes the last move, so that it can move on to the next branch
					path_options.pop() #Signifies the end of a branch
					current_tile = visited[len(visited) - tries -1] #Hop back, -1 keeps it from skipping steps				
				
				self.map.tiles[current_tile].is_current_tile = True
			self.map.print_map()
			tries = 0			
		
		return path,len(visited)