from operator import attrgetter
from random import random, randint
import numpy as np
from particle import Particle
from particle import schedule_builder

def algorithm(problem):

	population_size = 100
	max_generations = 100

	best_global_fitness = None
	best_global_position = None

	population = [Particle(problem) for k in range(population_size)]

	parameters = best_global_fitness, best_global_position, max_generations

	for generation in range(max_generations):
		print("Generation: " + str(generation))
		for particle in population:
			update(particle, generation, parameters)
			if particle.fitness <= problem[3]:
				return particle

	return min(population, key=attrgetter('fitness'))

def update(particle, generation, parameters):
	best_global_fitness, best_global_position, max_generations = parameters

	particle.fitness = particle.get_fitness()

	if particle.best_fitness is None or particle.fitness < particle.best_fitness:
		particle.best_fitness = particle.fitness
		particle.best_position = particle.position

	if best_global_fitness is None or particle.fitness < best_global_fitness:
		best_global_fitness = particle.fitness
		best_global_position = particle.position

	w = 1.2-0.8/ max_generations*generation

	particle.velocity = w*particle.velocity + 2*random()*(particle.best_position-particle.position) \
	+ 2*random()*(best_global_position-particle.position)

	if random() < (1-generation/max_generations):
		swap(particle)
	if random() < (1-generation/max_generations):
		insert(particle)
	if random() < (1-generation/max_generations):
		inverse(particle)
	if random() < (1-generation/max_generations):
		long_distance(particle)
	
def swap(particle):
	p = particle.position[:]
	i = randint(0, len(p)-2)
	p[i], p[i+1] = p[i+1], p[i]
	schedule = schedule_builder(particle.problem, list(p))
	fitness = max([machine[-1][3] for machine in schedule])+1
	if fitness < particle.fitness:
		particle.position = p
		particle.schedule = schedule
		particle.fitness = fitness

def insert(particle):
	p = particle.position[:]
	i = randint(0, len(p)-1)
	p = np.insert(p, randint(0, len(p)-1), p[i])
	p = np.delete(p, i)
	schedule = schedule_builder(particle.problem, list(p))
	fitness = max([machine[-1][3] for machine in schedule])+1
	if fitness < particle.fitness:
		particle.position = p
		particle.schedule = schedule
		particle.fitness = fitness

def inverse(particle):
	p = particle.position[:]
	i = randint(0, len(p)-1)
	j = randint(i, len(p))
	p[i:j] = p[i:j][::-1]
	schedule = schedule_builder(particle.problem, list(p))
	fitness = max([machine[-1][3] for machine in schedule])+1
	if fitness < particle.fitness:
		particle.position = p
		particle.schedule = schedule
		particle.fitness = fitness

def long_distance(particle):
	p = particle.position[:]
	i = randint(0, len(p)-1)
	j = randint(i, len(p))
	temp = p[i:j]
	p = np.concatenate([p[:i],p[j:]])
	r = randint(0, len(p))
	p = np.insert(p, r, temp)
	schedule = schedule_builder(particle.problem, list(p))
	fitness = max([machine[-1][3] for machine in schedule])+1
	if fitness < particle.fitness:
		particle.position = p
		particle.schedule = schedule
		particle.fitness = fitness
