from operator import attrgetter
from random import random, randint
import numpy as np

def algorithm(problem):

	population_size = 100
	max_generations = 100

	best_global_fitness = None
	best_global_position = None

	population = [Particle(problem) for k in range(population_size)]

	parameters = best_global_fitness, best_global_position, max_generations

	for generation in range(max_generations):
		for particle in population:
			update(particle, generation, parameters)
			if particle.fitness <= problem[3]:
				return particle

	return min(population, key=attrgetter('fitness'))

def update(particle, generation, parameters):
	best_global_fitness, best_global_position, max_generations = parameters

	particle.fitness = particle.get_fitness()

	