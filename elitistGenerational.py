#!/home/charizard/anaconda3/bin/ipython3
import numpy as np;
import matplotlib.pyplot as plt;
import individual as I;
import chromosome as C;
import selection as S;
import fitness as F;
import sys;
#	Input arguments
try:
	outputfile = sys.argv[6];
except IndexError:
	print(" gAI - steady state - usage: ")
	print("\tinput file name, deepness, popsize, time, seed, out name");
inpath = sys.argv[1];
deepness = int(sys.argv[2]);
populationSize = int(sys.argv[3]);
time = int(sys.argv[4]);
seed = int(sys.argv[5]);
#	Creating population
f = F.fitness(inpath);
s = S.selection(inpath);
population = [];
for iter in range(populationSize):
	chrList = [];
	for chrIter in range(deepness):
		chrList.append(C.chromosome());
	print(len(chrList));
	ind = I.individual(deepness);
	ind.includeInformation(chrList);
	population.append(ind)
#	Evolution simulation
print("iteration\tmin\tmean");
stackCounter = 0;
oldFitness = 1e10;
for iT in range(time):
	# parents that had sex
	population = s.elitism(population, 5);
	for iter in range(10):
		pTHS = s.tournament(population, 4, 2);
		mutationRate, chromRate = s.adaptativeMutation(stackCounter, 0.1, 8);
		if len(pTHS) == 2:
			i1 = pTHS[0];
			i2 = pTHS[1];
			s1,s2 = i1.reproduce(i2);
			s1.mutate(0.01 + mutationRate, 2 + chromRate);
			s2.mutate(0.01 + mutationRate, 2 + chromRate);
		population.append(s1);
		population.append(s2);
	if iT % 1000 == 0:
		fitnessControl = [];
		for iter in range(len(population)):
			fitnessControl.append(f.evaluateIndividual(population[iter]));
		fitnessControl = np.array(fitnessControl);
		print("{0}".format(iT), end="\t");
		print("{0}\t{1}".format(fitnessControl.min(), np.mean(fitnessControl)));
		if np.abs(oldFitness < fitnessControl.min()) < 1e2:
			stackCounter = stackCounter + 1000;
		else:
			stackCounter = 0;
		f.plotForgedImage(population[fitnessControl.argmin()], "{0}_{1}".format(outputfile, iT), fitnessControl.min())



