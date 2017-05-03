from node import Node
from ant import Ant

class Graph:
	def __init__(self, problem):
		self.problem = problem
		self.nodes = []
		self.evaporationFactor = 0.01
		self.alpha = 0.1
		self.initialPheromoneLevel = 0.2
		self.machines = {}

		for i in range(problem[0]*problem[1]+1): #Create one node for each operation in the jssp
			self.nodes.append(Node(i, self.problem))

		for j in range(1,self.problem[1]+1): #Create a map containing a list over all operations processed by the same machine, key = machine number
			machineList = []
			for node in self.nodes:
				if node.machine == j:
					machineList.append(node)
			self.machines[j] = machineList


		#print (self.nodes[0].edges)

	def localUpdate(self, ant):
		currentNode = self.nodes[0] #Current node is set to the dummynode at beginning of each local update
		for node in ant.tabuNodes: #Iterate over the ant's solution to find the sequence of the operations
			currentNode.edges[node.operationNumber][0] = (1-self.evaporationFactor)*currentNode.edges[node.operationNumber][0] + self.evaporationFactor*self.initialPheromoneLevel #Update the pheromone level on the edges traversed by the ant
			currentNode = node #Set the current node to be the next node

	def globalUpdate(self, globalBestTour):
		for node in self.nodes: #For all nodes/operations in the graph
			nodeIndexGlobalBest = globalBestTour.index(node) #Find the index in the globalBestSolution list
			if nodeIndexGlobalBest != len(globalBestTour): #As long as it is not the last operation
				nextNodeIndex = nodeIndexGlobalBest + 1 #The next operation's index
			for i in range(1,self.problem[0]*self.problem[1]+1): #For all edges from the current node
				if(i in nodes.edges.keys()): #If the edge exists
					node.edges[i][0] = (1-self.alpha)*node.edges[i][0] + deltaPheromone(i, nextNodeIndex, globalBestTour) #Update the pheromone level on the edge

	def deltaPheromone(self, i, nextNodeIndex, globalBestTour):	#Check if edge is on the global best tour
		if i == globalBestTour[nextNodeIndex].operationNumber: #If the edge is on the global-best-tour
			lengthOfBestTour = 0
			for node in globalBestTour:
				lengthOfBestTour += node.processingTime
			return 1/lengthOfBestTour
		else:
			return 0

		



