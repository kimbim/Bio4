from node import Node
import random
import math

class Ant:

	def __init__(self, problem, graph):
		self.problem = problem
		self.n, self.m, self.jobs, self.ms_goal, self.fname = problem
		self.alpha = 1.0
		self.beta = 0.2
		self.q0 = 0.8
		self.notVisitedNodes = [] #list of operations/nodes not yet visited by the ant
		self.tabuNodes = [] # list of operations/nodes that are visited by the ant
		self.availableNodes = [] #list of operations/nodes that are feasible and available at time t for the ant
		self.initialAvailNodes = []
		#self.pheromoneList = [[0.5 for x in range(self.m)] for y in range (self.n)] #list holding the pheromone quantities on preceding edges for each job
		self.graph = graph
		self.currentNode = self.graph.nodes[0] #This is set to represent the dummynode in the graph where each ant starts
		self.schedule = False
		self.makespan = False

		for key in self.currentNode.edges: #iterate over all the first operations from each job
			self.availableNodes.append(self.graph.nodes[key]) #Append these operations to the available operation list
			self.initialAvailNodes.append(self.graph.nodes[key])

	def reset(self):
		self.tabuNodes = []
		self.availableNodes = self.initialAvailNodes
		self.currentNode = self.graph.nodes[0]

	def calculateSolution(self):
		while len(self.tabuNodes)<self.problem[0]*self.problem[1]:
			self.stateTransition()

	def stateTransition(self):
		candidateProbabilities = [] #A list to hold the probability of the available nodes
		for node in self.availableNodes:
			stateTransitionProbability = math.pow(float(self.currentNode.edges[node.operationNumber][0]), float(self.alpha))*math.pow(float(1/float(self.currentNode.edges[node.operationNumber][1])), float(self.beta))
			candidateProbabilities.append((stateTransitionProbability, node))
		if (random.random()<=self.q0):
			self.currentNode = max(candidateProbabilities, key=lambda x: x[0])[1]
			self.tabuNodes.append(self.currentNode)
			self.calculateAvailableNodes()

		#Perform roulette wheel probability selection to find the next operation
		else:
			probabilitySum = 0
			for prob in candidateProbabilities:
				probabilitySum += prob[0]

			rouletteWheel = []
			counter = 0
			for prob in candidateProbabilities:
				tempTuple = (prob[1], counter + prob[0]/probabilitySum)
				rouletteWheel.append(tempTuple)
				counter = tempTuple[1]
			rand = random.random()
			for i in range(len(rouletteWheel)):
				if rand<rouletteWheel[i][1]:
					self.currentNode = rouletteWheel[i][0]
					self.tabuNodes.append(self.currentNode)
					self.calculateAvailableNodes()
					break

	def calculateAvailableNodes(self):
		self.availableNodes = []
		
		for node in self.graph.nodes:
			if node in self.initialAvailNodes:
				if node not in self.tabuNodes:
					self.availableNodes.append(node)
			elif node not in self.tabuNodes and node.operationNumber in self.currentNode.edges.keys() and self.graph.nodes[node.operationNumber-1] in self.tabuNodes:
				self.availableNodes.append(node)


	def schedule_builder(self, problem, ant):
		n, m, jobs, _, _ = problem

		operations = [(i, o[0]) for i in range(1, n+1) for o in jobs[i]]

		integer_series = [None] * len(ant)
		sorted_individual = sorted(ant)

		for i in range(1, len(ant)+1):
			real_number = sorted_individual[i-1]
			index = ant.index(real_number)
			ant[index] = None
			integer_series[index] = i
		
		jobs_order = [operations[i-1][0] for i in integer_series]
		
		sequence = []
		counters = [0]*(n+1)

		for i in jobs_order:
			sequence.append((i, jobs[i][counters[i]][0], jobs[i][counters[i]][1]))
			counters[i] += 1

		job_timers = [0] * (n + 1)
		timelines = [[] for x in range(0, m)]

		for operation in sequence:
			job, machine, duration = operation
			start = job_timers[job]
			inserted = False
			for k, time_slot in enumerate(timelines[machine-1]):
				if start + duration < time_slot[2]:
					end = start + duration
					timelines[machine-1].insert(k, (job, machine, start, end))
					inserted = True
					break
				else:
					if time_slot[3] > job_timers[job]:
						start = time_slot[3]
			if not inserted:
				end = start + duration
				timelines[machine-1].append((job, machine, start, end))
			job_timers[job] = end

		schedule = []
		for machine in timelines:
			schedule.append(sorted(machine, key=lambda x: x[2]))
		self.schedule = schedule

	def calculateMakespan(self):
		self.makespan = max([machine[-1][3] for machine in self.schedule])+1