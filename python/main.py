from random import random, randint
from numpy import array
import plotly as py
import plotly.figure_factory as ff
from pso import algorithm
<<<<<<< Updated upstream
from ba import bees
import sys
=======
from graph import Graph
from acs import Acs

>>>>>>> Stashed changes

makespans = {1:56, 2:1059, 3:1276, 4:1130, 5:1451, 6:979}

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

	print(jobs)
	exit()
	return n, m, jobs, ms_goal, fname


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

	fig = ff.create_gantt(df, colors=colors, index_col='Resource', title='BioAI', group_tasks=True,
		show_colorbar=False, bar_width=0.4, showgrid_x=True, showgrid_y=True)

	py.offline.plot(fig, filename='BioAI.html')

colors = dict(	J1  = 'rgb(230, 183, 116)',	# 4 orange
				J2  = 'rgb(147, 229, 117)',	# 8 green
				J3  = 'rgb(118, 146, 228)',	# 15 blue
				J4  = 'rgb(230, 117, 116)',	# 2 red
				J5  = 'rgb(185, 118, 228)',	# 18 violet
				J6  = 'rgb(230, 215, 116)',	# 5 yellow
				J7  = 'rgb(117, 229, 216)', # 12 turqoise
				J8  = 'rgb(228, 119, 208)', # 20 pink
				J9  = 'rgb(179, 230, 116)', # 7 light green
				J10 = 'rgb(122, 118, 228)', # 16 dark blue
				J11 = 'rgb(231, 116, 148)', # 1
				J12 = 'rgb(230, 150, 116)', # 3
				J13 = 'rgb(212, 230, 116)', # 6
				J14 = 'rgb(117, 229, 119)', # 9
				J15 = 'rgb(117, 229, 152)', # 10
				J16 = 'rgb(117, 229, 184)', # 11
				J17 = 'rgb(117, 210, 229)', # 13
				J18 = 'rgb(118, 178, 228)', # 14
				J19 = 'rgb(153, 118, 228)', # 17
				J20 = 'rgb(216, 118, 228)') # 19

<<<<<<< Updated upstream
problem = read_data(int(sys.argv[1]))
=======
problem = read_data(5)
#test = Graph(problem)
test1 = Acs(problem)
exit()
>>>>>>> Stashed changes
pso = algorithm(problem)
#print(pso.fitness)
#gantt(pso)

bees_alg = bees(problem)
print(bees_alg.fitness)
gantt(bees_alg)