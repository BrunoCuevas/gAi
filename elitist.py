#!/home/charizard/anaconda3/bin/ipython3
import numpy as np;
import matplotlib.pyplot as plt;
import individual as I;
import chromosome as C;
import selection as S;
import fitness as F;
import sys;
import math;
#
#	Input arguments
#
try:
	outputfile = sys.argv[5];
except IndexError:
	print(" gAI - steady state - usage: ")
	print("\tinput file name, deepness, popsize, time, seed, out name");
inpath = sys.argv[1];
deepness = int(sys.argv[2]);
time = int(sys.argv[3]);
seed = int(sys.argv[4]);
np.random.seed(seed);
#
#	Creating log File
#

#
#	Creating population
#
f = F.fitness(inpath);
s = S.selection(inpath);
chrList = [];
for chrIter in range(deepness):
	chrList.append(C.chromosome());
ind = I.individual(deepness);
ind.includeInformation(chrList);
fX  = f.evaluateIndividual(ind);
#
#	Evolution simulation
#
stackCounter = 0;
print("iteration\tmin\tmean");
for iT in range(time):
	# parents that had sex
	nInd = ind.copyIndividual();
	mutationInc = 0.049 / ( 1 + math.exp(-stackCounter + 500));
	mutationChr = int((deepness/2)*(1/(1+math.exp(-stackCounter + 500))));
	nInd.mutate(0.01 + mutationInc, mutationChr);
	nFX = f.evaluateIndividual(nInd);
	if nFX < fX:
		ind = nInd;
		fX = nFX;
		stackCounter = 0;
	else:
		stackCounter = stackCounter + 1;
	if iT % 1000 == 0:
		print("{0}".format(iT), end="\t");
		print("{0}",format(fX));
		f.plotForgedImage(ind, "{0}_{1}".format(outputfile, iT), fX)
