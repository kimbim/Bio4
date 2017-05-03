from ant import Ant
from graph import Graph
from node import Node

class Acs:

	def __init__(self, problem):
		self.problem = problem
		self.evaporationFactor = 0 #(1-p) is the evaporation constant for the entire algorithm
		self.beta = 0.2
		self.alpha = 0.2

		self.numberOfAnts = 100
		self.generations = 100
		self.generationNumber = 0

		self.ants = []

		self.graph = Graph(self.problem)

		for i in range (1,self.numberOfAnts+2): #Iterate x times to make x ants
			tempAnt = Ant(self.problem, self.graph) #Initialize ants with possible first operations
			self.ants.append(tempAnt) #Append ants to the list of ants

	def algorithm(self):
		currentBestAnt = self.ants[0]
		while (self.generationNumber<= self.generations): #For 100 generations

			for ant in self.ants: #For all ants in each generation
				ant.calculateSolution() #calculate feasible solution for each ant
				solutionSequence = []
				for operation in ant.tabuNodes:
					solutionSequence.append(operation.operationNumber)
				ant.schedule_builder(self.problem, solutionSequence)
				ant.calculateMakespan()
				if ant.makespan < currentBestAnt.makespan:
					currentBestAnt = ant
				self.graph.localUpdate(ant) #After completion of feasible solution for each ant, perform local pheromone update to encourage exploration
			self.graph.globalUpdate(currentBestAnt) #Perform global update to evaporate pheromone on edges and increase pheromone on edges from the global best tour

			print("Best makespan: " + str(currentBestAnt.makespan))
			print("Generation: " + str(self.generationNumber))
			self.generationNumber += 1

		return currentBestAnt


