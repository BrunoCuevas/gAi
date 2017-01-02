#!/home/charizard/anaconda3/bin/ipython3
import numpy as np;
import matplotlib.pyplot as plt;
import individual as I;
import chromosome as C;
import selection as S;
import fitness as F;
import sys;
import time as TT;
start = TT.time();
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
fileOut = open(outputfile+ '.dat', 'w+');
fileOut.write("Time\tMin\n");
fileOut.close();
fileOut = open(outputfile+ '.dat', 'ab');
#	Creating population
f = F.fitness(inpath);
s = S.selection(inpath);
population = [];
for iter in range(populationSize):
	chrList = [];
	chrList.append(C.chromosome());
	ind = I.individual(1);
	ind.includeInformation(chrList);
	population.append(ind)
#	Evolution simulation
print("iteration\tmin\tmean");
stackCounter = 0;
oldFitness = 1e10;
counter = 0;
timeCounter = 0;
lStart = TT.time();
for iChr in range(deepness):
	print("Working in {0}".format(iChr));
	counter = counter + 1;
	iT = 0;
	oldFitness = 1e10;
	while stackCounter < 300:
		# parents that had sex
		population = s.elitism(population, populationSize - 10);
		if TT.time() - start > (30*60):
			break;
		if TT.time() - lStart > 100:
			timeCounter = timeCounter + 1;
			lStart = TT.time();
			row2save = np.array([timeCounter*100, oldFitness]);
			np.savetxt(fileOut, row2save.reshape(1,-1), fmt="%10.2f", delimiter="\t");
		for iter in range(5):
			pTHS = s.tournament(population, 4, 2);
			if len(pTHS) == 2:
				i1 = pTHS[0];
				i2 = pTHS[1];
				s1,s2 = i1.reproduce(i2);
				s1.mutateMod(0.05 , iChr);
				s2.mutateMod(0.05 , iChr);
			population.append(s1);
			population.append(s2);
		if iT % 100 == 0:
			fitnessControl = [];
			for iter in range(len(population)):
				fitnessControl.append(f.evaluateIndividual(population[iter]));
			fitnessControl = np.array(fitnessControl);
			print("{0}".format(iT), end="\t");
			print("{0}\t{1}\t{2}".format(fitnessControl.min(), np.mean(fitnessControl),stackCounter));
			if np.abs(oldFitness - fitnessControl.min()) < 1e2:
				stackCounter = stackCounter + 100;
			else:
				stackCounter = 0;
				oldFitness = fitnessControl.min();
			f.plotForgedImage(population[fitnessControl.argmin()], "{0}_{1}".format(outputfile, iChr), fitnessControl.min())
		iT = iT + 1;
	stackCounter = 0;
	fI = population[fitnessControl.argmin()].copyIndividual();
	del population;
	population = [];
	end = TT.time();
	if end - start > (30*60):
		break;
	for iP in range(populationSize):
		chrList = [];
		chrList = fI.getAllGeneticMaterial();
		chrList.append(C.chromosome());
		ind = I.individual(iChr + 2);
		ind.includeInformation(chrList);
		population.append(ind);
# Second Step. Profiling.
father = fI.copyIndividual();
oldFitness = f.evaluateIndividual(father);
for iter in range(time):
	end = TT.time();
	if (end - start) > (30*60):
		break;
	if TT.time() - lStart > 100 :
		timeCounter = timeCounter + 1;
		lStart = TT.time()
		row2save = np.array([timeCounter*100, oldFitness]);
		np.savetxt(fileOut, row2save.reshape(1,-1), fmt="%10.2f", delimiter="\t");
	son = father.copyIndividual();
	son.mutate(0.05, 2);
	newFitness = f.evaluateIndividual(son);
	if newFitness < oldFitness:
		father = son;
		oldFitness = newFitness;
		f.plotForgedImage(father, "Finalist", oldFitness);
	#row2write = np.array([iter, oldFitness]);
	#np.savetxt(fileOut, row2write.reshape(1,-1), fmt="%10.2f", delimiter="\t");

fileOut.close();
