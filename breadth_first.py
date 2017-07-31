#First it finds the nodes with the lowest depth, and adds them to a list of nodes to be expanded.
#Then it expands them in the specified order, adding extensions of that branch to the list of nodes.
#The node contains its location, depth along with the node above it on the branch and the direction taken to get to it from its parent.
#Then it checks all nodes to see if any of them are on the end tile, and if there are then it sets that as the win candidate
#There is a possibility of there being more than one winning node with the same efficency, but the first one is chosen as it conforms the most to the default movement guide.
#Then it takes the winning node, finds the node before it on the branch, which finds the node above it and so on.
#The direction is recorded at each loop, and they are inserted backwards as we're starting at the end.
#Then it passes it on to be printed.
class Breadth_first():
	def __init__(self,map):
		self.map = map
		self.name = 'Breadth First'
	
	def get_path(self,winning_node,nodes):	
		path = []
		current_node = winning_node
		
		for i in range(0,winning_node[1]): #Will only loop for the length of the path
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
	
	def find_path(self):
		expanded = [] #Nodes that have been expanded, the list is kept so that they do not get expanded again and don't interfere with the selection process.
		nodes = [(self.map.start_point,0,None,None)] #tile index, depth, parent, direction taken
		
		actions = 0 #How many moves it took to find the end
		winning_node = None

		while winning_node == None: 
			#Finds lowest unexpanded node
			to_expand = []
			lowest_node = nodes[-1]

			#Find the current branch level
			
			for node in nodes:
				if node[1] < lowest_node[1] and node not in expanded:
					lowest_node = node

			#Adds all nodes on that level into the queue
			for node in nodes:
				if node[1] == lowest_node[1] and node not in expanded and node not in to_expand:
					to_expand.append(node)
			
			#Adds all surrounding nodes into the list, and adds the node that was expanded into the list
			for node in to_expand:	
				if node[0] == self.map.end_point:
					winning_node = node
					break; #Stops it from picking another winner
					
				if self.valid_move(-self.map.columns,node[0],nodes):
					nodes.append([node[0] - self.map.columns,lowest_node[1] + 1,'up',node[0]])		
				if self.valid_move(-1, node[0],nodes):
					nodes.append([node[0] - 1,lowest_node[1] + 1,'left',node[0]])
				if self.valid_move(self.map.columns,node[0],nodes):
					nodes.append([node[0] + self.map.columns,lowest_node[1] + 1,'down',node[0]])
				if self.valid_move(1,node[0],nodes):
					nodes.append([node[0] + 1,lowest_node[1] + 1,'right',node[0]])
				
				expanded.append(node)
				self.map.tiles[node[0]].is_expanded = True #For printing purposes
			
			self.map.print_map()
			
			print ('---------------------------')
			
			if len(expanded) == len(nodes):
				return ["No path found"],len(nodes)
	
		
		return self.get_path(winning_node,nodes),len(nodes)