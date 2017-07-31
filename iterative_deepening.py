#First it checks possible moves from the starting position, adding them to a list in an order that fulfils the default direction requirements.
#Then it takes the last value in the list, and explores what options are avaliable to it, up to the current depth limit.
#It does this until there are no options to add to the list, then it removes the path it just took, backtracks one move, and checks if there are now options, effectively expanding the next node.
#It will do this until it finds a branch that has movement options avaliable and it below the current depth limit.
#It won't register nodes until it plans to expand them, increasing efficency. This also prevents nodes from being queued twice.
#Once it runs out of nodes within the depth limit, it will increase the limit.

#Essentially a combination of depth-first and breadth-first
class Iterative_deepening:
	def __init__(self,map):
		self.map = map
		self.name = 'Iterative Deepening'
	
	def get_path(self,winning_node,nodes):	
		path = []
		current_node = winning_node
		
		for i in range(0,winning_node[1]): #Will only loop for the depth of the path
			if current_node[3] != None:
				path.insert(0,current_node[2])
				for node in nodes:
					if node[0] == current_node[3]:
						current_node = node
						break #Slightly speeds it up
		return path
	
	#Will return true or false depending on whether or not the move will violate the rules
	def valid_move(self,move,current_node,visited,depth_limit):
		for node in visited:
			if current_node[0] + move == node[0]:
				return False
				
		if current_node[1] > depth_limit:
			return False
					
		if current_node[0] + move >= 0 and current_node[0] + move < len(self.map.tiles): #Check out of bounds
			if self.map.tiles[current_node[0] + move].is_wall == False: #Check wall collision
				if move == -1:
					if self.map.get_2D(current_node[0])[0] == 0: #Stop it from using the left edge
						return False
				elif move == 1:
					if self.map.get_2D(current_node[0])[0] == self.map.columns -1: #Stop it from using the right edge
						return False
				#Above the top and below the bottom are both out of bounds and should have already been caught, this is just an added precaution.
				elif move == self.map.columns:
					if self.map.get_2D(current_node[0])[1] == self.map.rows -1: #Stop it from using the bottom
						return False
				elif move == -self.map.columns:
					if self.map.get_2D(current_node[0])[1] == 0: #Stop it from using the top
						return False
				return True		
		return False
	
	def find_path(self):
		visited = [] #Nodes that have been expanded, the list is kept so that they do not get expanded again and don't interfere with the selection process.
		nodes = []#self.map.start_point,0,None,None] #tile index, depth, direction taken, parent
		path_options = [self.map.start_point,0,None,None]
		
		current_node = self.map.start_point,0,None,None
		deepest_node = self.map.start_point,0,None,None
		
		depth_limit = 0

		while current_node[0] != self.map.end_point:
			tries = 0
			moved = False
			
			while moved == False:
					
				dead_end = True
				if self.valid_move(-self.map.columns,current_node,visited,depth_limit):
					nodes.append([current_node[0] - self.map.columns,current_node[1]+1,'up',current_node[0]])		
					dead_end = False
				elif self.valid_move(-1, current_node,visited,depth_limit):
					nodes.append([current_node[0] - 1,current_node[1]+1,'left',current_node[0]])
					dead_end = False
				elif self.valid_move(self.map.columns,current_node,visited,depth_limit):
					nodes.append([current_node[0] + self.map.columns,current_node[1]+1,'down',current_node[0]])
					dead_end = False
				elif self.valid_move(1,current_node,visited,depth_limit):
					nodes.append([current_node[0] + 1,current_node[1]+1,'right',current_node[0]])
					dead_end = False
					
				#Remove node from frontier
				if current_node not in visited:
					visited.append(current_node)
				
				self.map.tiles[current_node[0]].is_current_tile = False
				self.map.tiles[current_node[0]].is_expanded = True
				
				
				if current_node[1] >= deepest_node[1]:
					deepest_node = current_node
				
				
				#Once it has backtracked to the beginning, increase the depth and start from the deepest point
				if dead_end == False:
					current_node = nodes[-1]
					visited.append(current_node)	
					moved = True
				elif tries < len(visited):
					tries = tries + 1 #Keeps track of how many steps need to be reversed
					
					current_node = visited[len(visited) - tries -1] #Hop back, -1 keeps it from skipping steps							
				else:
					depth_limit += 1
					tries = 0
					
				self.map.tiles[current_node[0]].is_current_tile = True
				
				if depth_limit > self.map.columns + self.map.rows: #Checks if it has exceeded the maximum possible depth
					return ["No path found"],len(nodes)+1
			
			self.map.print_map()
			
			print ('---------------------------')		

		
		return self.get_path(current_node,nodes),len(nodes)+1