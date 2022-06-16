from copy import deepcopy
from queue import PriorityQueue
from Point import Point
import math



#AIModule

'''AIModule Interface
createPath(map map_) -> list<points>: Adds points to a path'''

'''
Base class of all AI implementations 
An interface representing a pathfinder AI interface. 
The interface exports a single function(createPath) which accepts as input a Map and 
computes a path from the start location to the end location. 

'''
'''
Computes a path from the start to the end point. 
Given a terrain map containing a start and end point, 
computes a path from the start point to the end point. 
the returned list should be a sequence of points 
from the start location to the end location(containing these points)
such that each point in the sequence is reachable from the previous point. 

'''

class AIModule:
	
  def createPath(self, map_):
	
			
      pass



#StupidAI
				
'''
A sample AI that takes a very suboptimal path.
This is a sample AI that moves as far horizontally as necessary to reach
the target, then as far vertically as necessary to reach the target.
It is intended primarily as a demonstration of the various pieces of the
program.
'''
		
	
class StupidAI(AIModule):
	
	#Creates the path to the goal 

	def createPath(self, map_):
		
	#Holds the resulting path 
		path = []
		explored = []
		
		# Get starting point
		# Keep track of where we are and add the start point
		path.append(map_.start)
		current_point = deepcopy(map_.start)


		# Keep moving horizontally until we match the target
		while(current_point.x != map_.goal.x):
			# If we are left of goal, move right
			if current_point.x < map_.goal.x:
				current_point.x += 1
			# If we are right of goal, move left
			else:
				current_point.x -= 1
			path.append(deepcopy(current_point))
			

		# Keep moving vertically until we match the target
		while(current_point.y != map_.goal.y):
			# If we are left of goal, move right
			if current_point.y < map_.goal.y:
				current_point.y += 1
			# If we are right of goal, move left
			else:
				current_point.y -= 1
			path.append(deepcopy(current_point))

		# We're done! Hand it back. 
		
		return path
	
	
	
#Djikstras	
'''
Dijkstra's algorithm is provided for always yields the optimal path,
so we can compare the AI against the DijkstraAI module to see if the path is indeed optimal. 
'''
	
	
class Djikstras(AIModule):

	def createPath(self, map_):
		
		q = PriorityQueue()
		
		cost = {}
		prev = {}
		explored = {}
		
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)] = math.inf
				prev[str(i)+','+str(j)] = None
				explored[str(i)+','+str(j)] = False
				
		current_point = deepcopy(map_.start) #x,y
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)] = 0
		q.put(current_point)
		while q.qsize() > 0:
			# Get new point from PQ
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue
			explored[str(v.x)+','+str(v.y)] = True
			# Check if popping off goal
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break
			# Evaluate neighbors
			neighbors = map_.getNeighbors(v)
			for neighbor in neighbors:
				
				alt = map_.getCost(v, neighbor) + cost[str(v.x)+','+str(v.y)]
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt
					#add heuristic herr after alt 
					neighbor.comparator = alt+getHeuristic(map_,neighbor)
					prev[str(neighbor.x)+','+str(neighbor.y)] = v
					q.put(neighbor)
					path = []
					while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
						path.append(v)
						v = prev[str(v.x)+','+str(v.y)]
						path.append(map_.getStartPoint())
						path.reverse()
						return path
					
					
#AStarExp 


class AStarExp(AIModule):
	
	#create a path 
	
	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)]= math.inf
				prev[str(i)+','+str(j)]= None
				explored[str(i)+','+str(j)] = False 
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)]=0
		q.put(current_point)
		
		while q.qsize() > 0:
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue 
			explored[str(v.x)+','+str(v.y)] = True 
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break 
			neighbors = map_.getNeighbors(v)
			
			for neighbor in neighbors:
				alt = map_.getCost(v,neighbor)
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt 
					#add Heuristic here after alt 
					neighbor.comparator = alt+self.getHeuristic(map_,neighbor)
					prev[str(neighbor.x)+','+str(neighbor.y)] =v
				q.put(neighbor)
		path= []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
			path.append(map_.getStartPoint())
			path.reverse()
			return path 
		
		
		
		
		
		
		#define Heuristic
		
		def getHeuristic(self, map_,Node):
			NodeX = Node.x
			NodeY = Node.y
			endPointX = map_.getEndPoint().x
			endPointY = map_.getEndPoint().y
			xDistance = abs(NodeX - endPointX)
			yDistance = abs(NodeY - endPointY)
			h1 = map_.getTile(endPointX, endPointY)
			h0 = map_.getTile(NodeX,NodeY)
			d = max(xDistance, yDistance)
			
			
			
			if h0 > h1:
				return math.pow(2,(h1-h0)/d)*d        #delta h = |h goal - h initial| 
			elif h0 < h1:
				return 2*(h1-h0)+max(0,d-(h1-h0)) 
			return max(xDistance, yDistance)  
		
		if h0 > h1:
			return math.pow(2,(h1-h0)/d)*d
		elif h0 < h1:
			return 2*(h1-h0)+max(0,d-(h1-h0))
		return max(xDistance, yDistance)
	
	
	pass
	
	
	
	
	
	
	
	
#AStarDiv 
	
class AStarDiv(AIModule):
	
	
#create a path 
	
	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)]= math.inf
				prev[str(i)+','+str(j)]= None
				explored[str(i)+','+str(j)] = False 
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)]=0
		q.put(current_point)
		
		while q.qsize() > 0:
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue 
			explored[str(v.x)+','+str(v.y)] = True 
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break 
			neighbors = map_.getNeighbors(v)
			
			for neighbor in neighbors:
				alt = map_.getCost(v,neighbor)
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt 
					#add Heuristic here after alt 
					neighbor.comparator = alt+self.getHeuristic(map_,neighbor)
					prev[str(neighbor.x)+','+str(neighbor.y)] =v
				q.put(neighbor)
		path= []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
			path.append(map_.getStartPoint())
			path.reverse()
			return path 
	
	
	
	
	#define heuristic
	
def getHeuristic(self, map_,Node):
	NodeX = Node.x    #p1.x
	NodeY = Node.y     #p1.y
	endPointX = map_.getEndPoint().x  #p2.x
	endPointY = map_.getEndPoint().y  #p2.y
	
	xDistance = abs(NodeX - endPointX)
	yDistance = abs(NodeY - endPointY)
	h0 = map_.getTile(NodeX, NodeY) 
	d = max(xDistance,yDistance)
	if h0 == 0:
		return 0 
	v = math.floor(math.log(h_0)/math.log(2))
	return max((d-v)/2,0)

pass 






#AStarMSH
			
			
class AStarMSH(AIModule):
	
	#create a path 
	
	def createPath(self, map_):
		q = PriorityQueue()
		cost = {}
		prev = {}
		explored = {}
		for i in range(map_.width):
			for j in range(map_.length):
				cost[str(i)+','+str(j)]= math.inf
				prev[str(i)+','+str(j)]= None
				explored[str(i)+','+str(j)] = False 
		current_point = deepcopy(map_.start)
		current_point.comparator = 0
		cost[str(current_point.x)+','+str(current_point.y)]=0
		q.put(current_point)
		
		while q.qsize() > 0:
			v = q.get()
			if explored[str(v.x)+','+str(v.y)]:
				continue 
			explored[str(v.x)+','+str(v.y)] = True 
			if v.x == map_.getEndPoint().x and v.y == map_.getEndPoint().y:
				break 
			neighbors = map_.getNeighbors(v)
			
			for neighbor in neighbors:
				alt = map_.getCost(v,neighbor)
				if alt < cost[str(neighbor.x)+','+str(neighbor.y)]:
					cost[str(neighbor.x)+','+str(neighbor.y)] = alt 
					#add Heuristic here after alt 
					neighbor.comparator = alt+self.getHeuristic(map_,neighbor)
					prev[str(neighbor.x)+','+str(neighbor.y)] =v
				q.put(neighbor)
		path= []
		while not(v.x == map_.getStartPoint().x and v.y == map_.getStartPoint().y):
			path.append(v)
			v = prev[str(v.x)+','+str(v.y)]
			path.append(map_.getStartPoint())
			path.reverse()
			return path
		
	#defining the heursitic
	
	
		
def getHeuristic(self, map_,Node):
	
	NodeX = Node.x #p1.x
	NodeY = Node.y #p1.y
	endPointX = map_.getEndPoint().x #p2.x
	endPointY = map_.getEndPoint().y #p2.y
	
	d = max(abs(endPointX - NodeX), abs(endPointY - NodeY))
	d2 = abs(endPointX-NodeX)+abs(endPointY - NodeY)
	height = self.getHeuristic(map_.getTile(map_.getEndPoin())-map_.getTile(Node))
	h_n = 0.0
	
	#going uphill 
	if height >= 0:
		if d>=height:
			h_n = (height*2)+(d-height)
		elif d< height and d2 > height:
			h_n = ((height %d)+4)+((d-(height%d))*2)
		elif d2 == height:
			h_n = (height*2)
		elif d2 < height:
			h_n = ((height % d2)*pow(2,ceil(height/d2)))+((d2-(height%d2))*pow(2,floor(height/d2)))
			#height < 0, going downhill 
		else:
			height *= -1 
			if d >= height:
				h_n = (height*0.5)+(d-height)
			elif d<height:
				h_n = ((height %d)*pow(2,-1*ceil(height/d)))+((d-(height%d))*pow(2,-1*floor(height/d)))
				return h_n 
			pass
				
				
				
				
			

						
						

								
								
								
								
					
					
			
						
							
							
						
						
					
				
				
				
				
		
		















































		