#A* but it starts from the end and recalculates all the nodes each cycle. 
#Essentially A* with iterative deepening
#Very CPU intensive, but it uses far less memory.
#Incredibly slow on large maps.

class Iterative_astar:
	G_INCREMENT = 1 #Controls how wide it searches
	
	def __init__(self,map):
		self.map = map
		self.name = 'Iterative A*'
	
	def get_path(self,winning_node,nodes):	
		path = []
		current_node = winning_node
		
		for i in range(0,winning_node[1]): #Will only loop for the length of the path
			if current_node[4] != None:
				path.append(current_node[3])
				for node in nodes:
					if current_node[4] == node[0]:
						current_node = node
						break #Slightly speeds it up
		return path	
		
	def get_heuristic(self,start_cords = None):		
		#Gets the distance between the start and end, and converts it to an actual distance. 
		#Could also use the standard distance formula but I already had this code written.
		#Uses Manhattan Distance
		end_cords = self.map.get_2D(self.map.start_point)
		if start_cords is None:
			start_cords = self.map.get_2D(self.map.end_point)
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
	
	#Will return true or false depending on whether or not the move will violate the rules
	def valid_move(self,move,current_node,expanded,threshold):
		for node in expanded:
			if current_node[0] + move == node[0]:
				return False
				
		if current_node[1]+current_node[2] > threshold:
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
		start_node = self.map.end_point,0,self.get_heuristic(),None,None #Starts at the end and works its way back
		current_node = start_node
		
		actions = 0 #How many moves it took to find the end
		threshold = 6
		winning_node = None

		while winning_node == None:
			threshold += 1 + self.G_INCREMENT
			dead_end = False
			nodes = [start_node] #tile index, distance from start, heuristic,parent
			expanded = []
		
			actions = actions + 1
			
			
			while dead_end == False and winning_node == None:
				self.map.print_map()
			
				print ('---------------------------')
				actions = actions + 1
				
				lowest_cost = threshold
				for node in nodes:
					if node[1] + node[2] <= lowest_cost and node not in expanded:
						lowest_cost = node[1] + node[2]	
					
				priority_queue = []

				#Adds all nodes with that cost into the queue
				dead_end = True
				for node in nodes:
					if node[1]+node[2] == lowest_cost and node not in expanded:
						priority_queue.append(node)
						dead_end = False
				


				#Adds all surrounding nodes into the list, and adds the node that was expanded into the list of expanded nodes
				for node in priority_queue:	
					if node[0] == self.map.start_point:
						winning_node = node
						break
						
					if self.valid_move(-self.map.columns,node,expanded,threshold):
						nodes.append([node[0] - self.map.columns,node[1]+self.G_INCREMENT,self.get_heuristic(node[0] - self.map.columns),'down',node[0]])
					if self.valid_move(-1, node,expanded,threshold):
						nodes.append([node[0] - 1,node[1]+self.G_INCREMENT,self.get_heuristic(node[0] - 1),'right',node[0]])
					if self.valid_move(self.map.columns,node,expanded,threshold):
						nodes.append([node[0] + self.map.columns,node[1]+self.G_INCREMENT,self.get_heuristic(node[0] + self.map.columns),'up',node[0]])
					if self.valid_move(1,node,expanded,threshold):
						nodes.append([node[0] + 1,node[1]+self.G_INCREMENT,self.get_heuristic(node[0] + 1),'left',node[0]])
					
						
					expanded.append(node)
					self.map.tiles[node[0]].is_expanded = True #For printing purposes							
					
	
		
		
		return self.get_path(winning_node,nodes),len(nodes)