class Node:

	def __init__(self, num, problem):
		self.problem = problem
		self.operationNumber = num
		self.initialPheromoneLevel = 0.5
		self.edges = {}  #A map holding all the edges out of the node instance. Key = to-node, value = tuple (x,y) where x = pheromonelevel on the edge and y = heuristic distance
		self.processed = False
		if self.operationNumber == 0:

			self.processingTime = 0
			self.machine = 0
			self.job = 0

			for m in range(1,(self.problem[0]*self.problem[1]-1),self.problem[1]):
				i, j = self.getJob(m)
				self.edges[m] = (self.initialPheromoneLevel, self.problem[2][i][j][1])

		else:
			i, j = self.getJob(num)
			tempTuple = self.problem[2][i][j]
			self.job = i
			self.machine = tempTuple[0]
			self.processingTime = tempTuple[1]

			if num % self.problem[1]!= 0:
				self.edges[num+1] = (self.initialPheromoneLevel, self.problem[2][i][j+1][1])

			counter = 1
			for k in range(1,self.problem[0]+1): #Iterate over all jobs
				for l in range(self.problem[1]):
					if k == self.job:
						counter += 1
					else:
						self.edges[counter] = (self.initialPheromoneLevel,self.problem[2][k][l][1])
						counter += 1

	def process(self):
		self.processed = True

	def reset(self):
		self.processed = False

	def getJob(self, id):
		d = float(id) / float(self.problem[1])
		if (d % 1 == 0):
			i = int(d) 
		else:
			i = int(d)+1
		j = id % self.problem[1]
		if j == 0:
			j = self.problem[1]-1
		else:
			j = j - 1
		return i, j