from random import randint
import numpy as np
from particle import Particle
from particle import schedule_builder

PATCH_DECREASE = 0.95

def bees(problem, bees=45, sites=3, elite_sites=1, patch_size=3, elite_bees=7, other_bees=2):
	population = init_pop(bees, problem)
	done = False
	iterations = 0
	while (done == False):
		next_generation = []
		patch_size = patch_size*PATCH_DECREASE
		best_sites = select_best_sites(population, sites)
		for i in range(len(best_sites)):
			recruited_bees = 0
			if (i < elite_sites):
				recruited_bees += elite_bees
			else:
				recruited_bees += other_bees
			neighborhood = []
			for j in range(recruited_bees):
				neighborhood.append(create_neigh_bee(best_sites[i], patch_size))
			next_generation.append(get_best_sol(neighborhood))
		remaining_bees = bees - sites
		for j in range(remaining_bees):
			next_generation.append(create_rand_bee(problem))
		population = next_generation
		print(get_best_sol(population).get_fitness())
		iterations += 1
		if iterations == 100:
			done = True
	return get_best_sol(population)

def init_pop(bees, problem):
	 return [Particle(problem) for k in range(bees)]

def eval_pop(population):
	for i in range(len(population)):
		population[i] = (population[i][0], population[i][0].get_fitness())

def select_best_sites(population, sites):
	sorted_pop = sorted(population, key=lambda x: x.get_fitness())
	return sorted_pop[:sites]

def create_neigh_bee(site, patch_size):
	p = site.position[:]
	i = randint(0, len(p)-1)
	j = randint(i, len(p))
	temp = p[i:j]
	p = np.concatenate([p[:i],p[j:]])
	r = randint(0, len(p))
	p = np.insert(p, r, temp)
	schedule = schedule_builder(site.problem, list(p))
	site.position = p
	site.schedule = schedule
	return site

def get_best_sol(neighborhood):
	sorted_pop = sorted(neighborhood, key=lambda x: x.get_fitness())
	return sorted_pop[0]

def create_rand_bee(problem):
	return Particle(problem)

