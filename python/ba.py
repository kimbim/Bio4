from random import randint
import numpy as np
from bee import Bee

PATCH_DECREASE = 0.95

def bees(problem, bees=45, sites=3, elite_sites=1, patch_size=3, elite_bees=7, other_bees=2):
	population = init_pop(bees, problem)
	done = False
	iterations = 0
	max_iterations = 100
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
				neighborhood.append(create_neigh_bee(best_sites[i], patch_size, problem))
			next_generation.append(get_best_sol(neighborhood))
		remaining_bees = bees - sites
		for j in range(remaining_bees):
			next_generation.append(create_rand_bee(problem))
		
		if best_sites[0].get_fitness() < get_best_sol(next_generation).get_fitness():
				next_generation.remove(get_best_sol(next_generation))
				next_generation.append(best_sites[0])

		population = next_generation
		
		print("Generation: " + str(iterations+1))
		print("Makespan of best bee: " + str(get_best_sol(population).get_fitness()))
		iterations += 1
		if iterations >= max_iterations:
			done = True
	return get_best_sol(population)

def init_pop(bees, problem):
	return [Bee(problem) for k in range(bees)]

def select_best_sites(population, sites):
	sorted_pop = sorted(population, key=lambda x: x.get_fitness())
	return sorted_pop[:sites]

def create_neigh_bee(site, patch_size, problem):
	p = site.position[:]
	i = randint(0, len(p)-1)
	j = randint(i, len(p))
	temp = p[i:j]
	p = np.concatenate([p[:i],p[j:]])
	r = randint(0, len(p))
	p = np.insert(p, r, temp)
	temp = Bee(problem, p)
	schedule = temp.schedule_builder(list(p))
	temp.schedule = schedule
	return temp

def get_best_sol(neighborhood):
	sorted_pop = sorted(neighborhood, key=lambda x: x.get_fitness())
	return sorted_pop[0]

def create_rand_bee(problem):
	return Bee(problem)

