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
		integer_series = [None] * len(position)
		sorted_individual = sorted(position)

		for i in range(1, len(position)+1):
			real_number = sorted_individual[i-1]
			index = position.index(real_number)
			position[index] = None
			integer_series[index] = i

		jobs_order = [operations[i-1][0] for i in integer_series]

		sequence = []
		counters = [0]*(self.n+1)

		for i in jobs_order:
			sequence.append((i, self.jobs[i][counters[i]][0], self.jobs[i][counters[i]][1]))
			counters[i] += 1

		job_timers = [0]*(self.n+1)
		timelines = [[] for x in range(0,self.m)]

		for operation in sequence:
			job, machine, duration = operation
			start = job_timers[job]
			inserted = False
			for k, time_slot in enumerate(timelines[machine-1]):
				if start+duration < time_slot[2]:
					end = start+duration
					timelines[machine-1].insert(k, (job, machine, start, end))
					inserted = True
					break
				else:
					if time_slot[3] > job_timers[job]:
						start = time_slot[3]
			if not inserted:
				end = start + duration
				timelines[machine-1].append((job,machine,start,end))
			job_timers[job] = end

		schedule = []
		for machine in timelines:
			schedule.append(sorted(machine, key=lambda x: x[2]))
		return schedule
