class Ant:

	def __init__(self, problem):
		self.problem = problem
		self.n, self.m, self.jobs, self.ms_goal, self.fname = problem
		self.notVisitedNodes = [] #list of operations/nodes not yet visited by the ant
		self.tabuNodes = [] # list of operations/nodes that are visited by the ant
		self.availableNodes = [] #list of operations/nodes that are feasible and available at time t for the ant
		self.pheromoneList = [[0.5 for x in range(self.m)] for y in range (self.n)] #list holding the pheromone quantities on preceding edges for each job

	def addStartAndEndNode(self):
		nodes = [0]
		for i in self.jobs:
			nodes.append(i)
		l = len(nodes)
		nodes.append[l]
		


	def setInitialPheromoneValues(self):
		for i in self.pheromoneList:
			for j in i:
				j = 0.5

	def updatePheromoneValues(self):
		for i 


	def stateTransition(self):
		nextOperation = 





