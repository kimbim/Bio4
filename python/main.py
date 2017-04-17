from random import random
from numpy import array
import plotly as py
import plotly.figure_factory as ff


makespans = {1:56, 2:1059, 3:1276, 4:1130, 5:1451, 6:979}

class Particle:
	def __init__(self, problem):
		self.n, self.m, self.jobs, self.ms_goal, self.fname = problem
		self.position = self.generate_random_position()
		self.velocity = self.generate_random_velocity()
		self.schedule = schedule_builder(problem,list(self.position[:]))
		self.fitness = self.get_fitness()
		self.best_fitness = None
		self.best_position = None

	def generate_random_position(self):
		return array([int(1000*random())/10 for i in range(1, self.n*self.m+1)])

	def generate_random_velocity(self):
		return array([int(2000*random()-1000)/10 for i in range(1,self.n*self.m+1)])

	def get_fitness(self):
		return max([machine[-1][3] for machine in self.schedule])+1


def read_data(fname):
	ms_goal = makespans[fname]
	with open('../Test data/'+str(fname)+'.txt','r') as file:
		lines = []
		for line in file:
			lines.append(line.split())
	line = lines.pop(0)
	n, m = int(line[0]), int(line[1])
	jobs = {}
	for k, line in enumerate(lines):
		sequence = []
		for i in range(0,len(line)//2):
			sequence.append((int(line.pop(0))+1, int(line.pop(0))))
		jobs[k+1] = sequence
	return n, m, jobs, ms_goal, fname



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

def gantt(solution):
	df = []
	for machine in solution.schedule:
		for task in machine:
			d = {}
			d['Resource'] = 'J' + str(task[0])
			d['Task'] = 'Machine' + str(task[1])
			d['Start'] = '0000-01-01 ' + str(task[2]//60).zfill(2)+':'+str(task[2]%60).zfill(2)+':00'
			d['Finish'] = '0000-01-01 '+str(task[3]//60).zfill(2)+':'+str(task[3]%60).zfill(2)+':00'
			df.append(d)

	fig = ff.create_gantt(df, index_col='Resource', title='BioAI', group_tasks=True,
		show_colorbar=False, bar_width=0.4, showgrid_x=True, showgrid_y=True)

	py.offline.plot(fig, filename='BioAI')


problem = read_data(1)

particle = Particle(problem)

print(particle.schedule)

gantt(particle)

