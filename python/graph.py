from node import Node
from ant import Ant

class Graph:
	def __init__(self, problem):
		self.problem = problem
		self.nodes = []
		self.evaporationFactor = 0.01
		self.alpha = 0.01
		self.initialPheromoneLevel = 0.5
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
			currentNode.edges[node.operationNumber] = ((1.0-float(self.evaporationFactor))*float(currentNode.edges[node.operationNumber][0]) + float(self.evaporationFactor)*float(self.initialPheromoneLevel), float(currentNode.edges[node.operationNumber][1])) #Update the pheromone level on the edges traversed by the ant
			currentNode = node #Set the current node to be the next node

	def globalUpdate(self, bestAnt):
		#printlist = []
		
		#for node in bestAnt.tabuNodes:
		#	printlist.append(node.operationNumber)
		#print('Best tour: ' + str(printlist))
		#print('')
		for node in self.nodes: #For all nodes/operations in the graph
			if (node.operationNumber != 0):
				nodeIndexGlobalBest = bestAnt.tabuNodes.index(node) #Find the index in the globalBestSolution list
				if nodeIndexGlobalBest != len(bestAnt.tabuNodes): #As long as it is not the last operation
					nextNodeIndex = nodeIndexGlobalBest + 1 #The next operation's index
				for i in range(1,self.problem[0]*self.problem[1]+1): #For all edges from the current node
					if(i in node.edges.keys()): #If the edge exists
						node.edges[i] = ((1.0-float(self.alpha))*float(node.edges[i][0]) + 1.05*self.deltaPheromone(i, nextNodeIndex, bestAnt), float(node.edges[i][1])) #Update the pheromone level on the edge
				else:
					for j in range(1,self.problem[0]*self.problem[1]+1): #For all edges from the current node
						if(j in node.edges.keys()): #If the edge exists
							node.edges[j] = ((1.0-float(self.alpha))*float(node.edges[j][0]), float(node.edges[j][1]))
			else: #If the node is the  dummy node, update all its edges
				nextNodeIndex = 0
				for k in range(1,self.problem[0]*self.problem[1]+1): #For all edges from the current node
					if(k in node.edges.keys() and k == nextNodeIndex): #If the edge exists
						node.edges[k] = ((1.0-float(self.alpha))*float(node.edges[k][0]) + 1.05*self.deltaPheromone(k, nextNodeIndex, bestAnt), float(node.edges[k][1])) #Update the pheromone level on the edge
					elif(k in node.edges.keys()):
						node.edges[k] = ((1.0-float(self.alpha))*float(node.edges[k][0]), float(node.edges[k][1]))

		#for node in self.nodes:
		#	print('NodeNr: ' + str(node.operationNumber) + ': ' + str(node.edges))

	def deltaPheromone(self, i, nextNodeIndex, bestAnt):	#Check if edge is on the global best tour

		if i == bestAnt.tabuNodes[nextNodeIndex-1].operationNumber: #If the edge is on the global-best-tour
			return 1.0/float(bestAnt.makespan)
		else:
			return 0

		



