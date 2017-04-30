PATCH_DECREASE = 0.95
bees = 45
sites = 3
elite_sites = 1
patch_size = 3
elite_bees = 7
other_bees = 2

def bees(problem, bees, sites, elite_sites, patch_size, elite_bees, other_bees):
	population = init_pop(bees, problem)
	while (done == False):
		population = eval_pop(population)
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
		if LOL:
			done = True
	return get_best_sol(population)

def init_pop(bees, problem):
	 return [(Particle(problem),0) for k in range(bees)]

def eval_pop(population):
	for pop in population:
		pop = (pop[0],pop[0].get_fitness())

def select_best_sites(population, sites):
	sorted_pop = sorted(population, key=lambda x: x[1])
	return sorted_pop[:sites]

def create_neigh_bee(site, patch_size):
	pass

def get_best_sol(neighborhood):
	sorted_pop = sorted(population, key=lambda x: x[1])
	return sorted_pop[0]

def create_rand_bee(problem):
	return Particle(problem)

