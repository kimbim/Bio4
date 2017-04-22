from random import random, randint
from numpy import array

class Particle:
	def __init__(self, problem):
		self.problem = problem
		self.n, self.m, self.jobs, self.ms_goal, self.fname = problem
		self.position = self.generate_random_position()
		self.velocity = self.generate_random_velocity()
		self.schedule = schedule_builder(problem,list(self.position[:]))
		self.fitness = self.get_fitness()
		self.best_fitness = None
		self.best_position = None

	def generate_random_position(self):
		return array([randint(0,100) for i in range(1, self.n*self.m+1)])

	def generate_random_velocity(self):
		return array([randint(-100,100) for i in range(1,self.n*self.m+1)])

	def get_fitness(self):
		return max([machine[-1][3] for machine in self.schedule])+1


def schedule_builder(problem,particle):
	n, m, jobs  = problem[0], problem[1], problem[2]
	operations = [(i, o[0]) for i in range(1, n+1) for o in jobs[i]]
	integer_series = [None] * len(particle)
	sorted_individual = sorted(particle)

	for i in range(1, len(particle)+1):
		real_number = sorted_individual[i-1]
		index = particle.index(real_number)
		particle[index] = None
		integer_series[index] = i

	jobs_order = [operations[i-1][0] for i in integer_series]

	sequence = []
	counters = [0]*(n+1)

	for i in jobs_order:
		sequence.append((i, jobs[i][counters[i]][0], jobs[i][counters[i]][1]))
		counters[i] += 1

	job_timers = [0]*(n+1)
	timelines = [[] for x in range(0,m)]

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
