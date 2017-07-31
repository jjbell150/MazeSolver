from map import Map

from depth_first import Depth_first
from breadth_first import Breadth_first
from astar import AStar
from greedy_best_first import Greedy_best_first
from iterative_deepening import Iterative_deepening
from iterative_astar import Iterative_astar
from greedy import Greedy

import sys

class Main():
	def __init__(self):
		#If parameters are missing then they will default to unentered, which will trigger re-entry of both arguments
		try:
			self.file_name = sys.argv[1].lower() #Map name
		except:
			self.file_name = 'Unentered'
		try:
			self.search_algorithm = sys.argv[2].lower() #Algorithm name
		except:
			self.search_algorithm = 'Unentered'
			
		self.map = Map(self.file_name) #Map contains a list of tiles and other features
		
		self.solver = self.find_solver(self.search_algorithm) #The algorithm used
		path, num_nodes = self.solver.find_path() #The actual solving part
		self.print_result(path,num_nodes) #Print results
	
	#Converts the name into an actual file, done this way to allow me to use several aliases
	def find_solver(self, algorithm):
		solver = None
		while solver is None:
			if algorithm == 'depth_first' or algorithm == 'dfs': 
				solver = Depth_first(self.map)
			elif algorithm == 'breadth_first' or algorithm == 'bf' or algorithm == 'bfs':
				solver = Breadth_first(self.map)
			elif algorithm == 'astar' or algorithm == 'a*':
				solver = AStar(self.map)
			elif algorithm == 'greedy_best_first' or algorithm == 'gbf' or algorithm == 'gbfs':
				solver = Greedy_best_first(self.map)		
			elif algorithm == 'iterative_deepening' or algorithm == 'id' or algorithm == 'ids':
				solver = Iterative_deepening(self.map)		
			elif algorithm == 'greedy' or algorithm == 'g' or algorithm == 'gs':
				solver = Greedy(self.map)	
				
			#Iterative astar works, but it does not work well. 
			#I did not research it much before building it, and I got a few key details wrong.
			#I decided to scrap it and use a different informed custom search (greedy), as it would have taken me far too long to redo it.
			#But I figured it would still be a valuable thing to include just to show my progress.
			elif algorithm == 'iterative_astar' or algorithm == 'ia*':
				solver = Iterative_astar(self.map)				
			else:
				print('Valid searches are: dfs (depth first), bfs (breadth first), A*, greedy, ids (iterative deepening) or gbfs (greedy best first)')
				print('Please enter an algorithm:')
				algorithm = input()
		
		return solver
			
	def print_result(self,path,num_nodes):
		#Print algorithm
		print("Algorithm used: "+self.solver.name)
		#Print file
		print("Map name: "+self.file_name)
		#Print nodes in tree
		print("There are "+str(num_nodes)+" nodes in the search tree")
		#Print path
		to_print = ""
		for direction in path:
			if direction != None:
				to_print += direction+" "
		
		print (to_print)
		

Main()