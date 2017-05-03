from random import random, randint
from numpy import array

class Bee:

	#def __repr__(self):
	#	return str(self.fitness)

	def __init__(self, problem, position='Default'):
		self.problem = problem
		self.n, self.m, self.jobs, self.ms_goal, self.fname = problem
		
		if position == 'Default':
			self.position = self.generate_random_position()
		else:
			self.position = position

		self.schedule = self.schedule_builder(list(self.position[:]))
		self.fitness = self.get_fitness()

	def generate_random_position(self):
		return array([randint(0,100) for i in range(1, self.n*self.m+1)])

	def get_fitness(self):
		return max([machine[-1][3] for machine in self.schedule])+1

	def schedule_builder(self, position):
		operations = [(i, o[0]) for i in range(1, self.n+1) for o in self.jobs[i]]
		int_series = [None] * len(position)
		sorted_ind = sorted(position)

		for i in range(1, len(position)+1):
			r_number = sorted_ind[i-1]
			index = position.index(r_number)
			position[index] = None
			int_series[index] = i

		j_order = [operations[i-1][0] for i in int_series]

		seq = []
		counters = [0]*(self.n+1)

		for i in j_order:
			seq.append((i, self.jobs[i][counters[i]][0], self.jobs[i][counters[i]][1]))
			counters[i] += 1

		j_timers = [0]*(self.n+1)
		timelines = [[] for x in range(0,self.m)]

		for operation in seq:
			j, m, d = operation
			start = j_timers[j]
			inserted = False
			for k, time_slot in enumerate(timelines[m-1]):
				if start+d < time_slot[2]:
					end = start+d
					timelines[m-1].insert(k, (j, m, start, end))
					inserted = True
					break
				else:
					if time_slot[3] > j_timers[j]:
						start = time_slot[3]
			if not inserted:
				end = start + d
				timelines[m-1].append((j,m,start,end))
			j_timers[j] = end

		schedule = []
		for m in timelines:
			schedule.append(sorted(m, key=lambda x: x[2]))
		return schedule

