class selection():
	def __init__(self, path2picture):
		import fitness as F;
		self.__evaluator = F.fitness(path2picture);
	def elitism(self, population, elitSize):
		import fitness as F;
		import numpy as np;
		popSize = len(population);
		fitnessVector = np.zeros(len(population));
		elite = [];
		for iter in range(popSize):
			fitnessVector[iter] = self.__evaluator.evaluateIndividual(population[iter]);
		for iter in range(elitSize):
			eliteInstance = fitnessVector.argmin();
			fitnessVector[eliteInstance] = 1e9; # This could lead to fail
			elite.append(population[eliteInstance]);
		return elite;
	def tournament(self, population, size, finalistsSize):
		import fitness as F;
		import numpy as np;
		#
		finalist = list();
		popSize = len(population);
		for iter in range(finalistsSize):
			term = np.array([0,0]);
			term[0] = np.random.randint(0, high=popSize, size=1);	
			term[1] = np.random.randint(0, high=popSize, size=1);
			matchPoints = np.array([0,0]);
			matchPoints[0]= self.__evaluator.evaluateIndividual(population[term[0]]);
			matchPoints[1]= self.__evaluator.evaluateIndividual(population[term[1]]);
			winner = term[matchPoints.argmin()];
			loser = term[matchPoints.argmax()];
			for iter in range(size - 1):
				term[matchPoints.argmax()] = np.random.randint(0, high=popSize,size=1);
				matchPoints[matchPoints.argmax()] = self.__evaluator.evaluateIndividual(population[term[matchPoints.argmax()]]);
				winner = term[matchPoints.argmin()];
				loser = term[matchPoints.argmax()];
			finalist.append(population[winner]);
		return finalist;
	def parka(self, population, finalistsSize, newbies):
		import numpy as np;
		popSize = len(population);
		counter = 0;
		for iter in range(finalistsSize):
			deathChossen = np.random.randint(0, high = popSize, size=1);
			population[deathChossen] = newbies[counter];
			popSize = len(population);
			counter = counter + 1;
		return population;
	def adaptativeMutation (self, stackCounter, maxRate, maxChr):
		import math;
		rate = (maxRate/(1+(math.exp(-0.5*stackCounter - 500))));
		chrom = int((maxChr/(1 + (math.exp(-0.5*stackCounter - 500)))));
		return rate, chrom
