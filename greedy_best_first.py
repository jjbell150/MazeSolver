

class Greedy_best_first():	
	def __init__(self,map):
		self.map = map
		self.name = 'Greedy Best First'
	
	def get_path(self,winning_node,nodes):	
		path = []
		current_node = winning_node
		
		for i in range(0,len(nodes)): #Will only loop for the length of the path
			if current_node[2] != None:
				path.insert(0,current_node[2])
				for node in nodes:
					if node[0] == current_node[3]:
						current_node = node
						break #Slightly speeds it up
		return path	
	
	#Will return true or false depending on whether or not the move will violate the rules
	def valid_move(self,move,current_tile,nodes):
		for node in nodes:
			if node[0] == current_tile+move:
				return False;
					
		if current_tile + move >= 0 and current_tile + move < len(self.map.tiles): #Check out of bounds
			if self.map.tiles[current_tile + move].is_wall == False: #Check wall collision
				if move == -1:
					if self.map.get_2D(current_tile)[0] == 0: #Stop it from using the left edge
						return False
				elif move == 1:
					if self.map.get_2D(current_tile)[0] == self.map.columns -1: #Stop it from using the right edge
						return False
				#Above the top and below the bottom are both out of bounds and should have already been caught, this is just an added precaution.
				elif move == self.map.columns:
					if self.map.get_2D(current_tile)[1] == self.map.rows -1: #Stop it from using the bottom
						return False
				elif move == -self.map.columns:
					if self.map.get_2D(current_tile)[1] == 0: #Stop it from using the top
						return False
				return True		
		return False
	
	def get_heuristic(self,start_cords = None):		
		#Gets the distance between the start and end, and converts it to an actual distance. 
		#Could also use the standard distance formula but I already had this code written.
		#Uses Manhattan Distance
		end_cords = self.map.get_2D(self.map.end_point)
		if start_cords is None:
			start_cords = self.map.get_2D(self.map.start_point)
		else:
			start_cords = self.map.get_2D(start_cords)
			
		if end_cords[0] > start_cords[0]:
			col_dist = end_cords[0] - start_cords[0]
		else:
			col_dist = start_cords[0] - end_cords[0]
			
		if end_cords[1] > start_cords[1]:
			row_dist = end_cords[1] - start_cords[1]
		else:
			row_dist = start_cords[1] - end_cords[1]
			
		distance = col_dist+row_dist
		return distance
	
	#Will return the quickest path
	def find_path(self):
		expanded = [] #Nodes that have been expanded, the list is kept so that they do not get expanded again and don't interfere with the selection process.
		nodes = [(self.map.start_point,self.get_heuristic(),None,None)] #tile index, H (heuristic), parent, direction taken
		
		max_heuristic = self.map.columns + self.map.rows
		winning_node = None

		while winning_node == None:
			priority_queue = []
			
			#Finds lowest cost unexpanded node
			lowest_cost = max_heuristic

			for node in nodes:
				if node[1] < lowest_cost and node not in expanded:
					lowest_cost = node[1]

			#Adds all nodes with that cost into the queue
			for node in nodes:
				if node[1] == lowest_cost and node not in expanded:
					priority_queue.append(node)

			#Adds all surrounding nodes into the list, and adds the node that was expanded into the list of expanded nodes
			for node in priority_queue:	
				if node[0] == self.map.end_point:
					winning_node = node
					break
				if self.valid_move(-self.map.columns,node[0],nodes):
					nodes.append([node[0] - self.map.columns,self.get_heuristic(node[0] - self.map.columns),'up',node[0]])		
				if self.valid_move(-1, node[0],nodes):
					nodes.append([node[0] - 1,self.get_heuristic(node[0] - 1),'left',node[0]])
				if self.valid_move(self.map.columns,node[0],nodes):
					nodes.append([node[0] + self.map.columns,self.get_heuristic(node[0] + self.map.columns),'down',node[0]])
				if self.valid_move(1,node[0],nodes):
					nodes.append([node[0] + 1,self.get_heuristic(node[0] + 1),'right',node[0]])
				
				expanded.append(node)
				self.map.tiles[node[0]].is_expanded = True #For printing purposes
			
			self.map.print_map()
			print ('---------------------------')
			
			if len(expanded) == len(nodes):
				return ["No path found"],len(nodes)
			
			
		#Prints a map for reference
		self.map.print_map()
			
		return self.get_path(winning_node,nodes),len(nodes)