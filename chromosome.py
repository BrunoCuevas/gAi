
import numpy as np;
class chromosome:
	def __init__(self, gI=None):

		self.__className = 'Chromosome';
		self.__version = 1.0;
		# 8 bits x 2 coordinates = 16
		# 6 coordinates = 96
		# 256 colours = 8
		# total = 104
		self.__length =  104;
		self.__str = 'chromosome';
		if gI==None:
			randomStart = np.random.rand(104);
			self.__gI = np.zeros(self.__length);
			self.__gI[randomStart > 0.5] = 1;
			self.__gI[randomStart < 0.5] = 0;
		else:
			self.__gI = gI;
	def __repr__(self):
		return self.__className;
	def copy(self):
		import chromosome as c;
		import numpy as np;
		info = np.copy(self.__gI);
		chro = c.chromosome(gI =info);
		return chro;
	def __modifyGI(self, newGI):
		if len(newGI) == self.__length:
			self.__gI = newGI;
			return 1;
		else:
			print("error: input has a different length that chromosome");
			return 0;
	def getGI(self):
		return self.__gI;
	def getLength(self):
		return self.__length;
	def getLabel(self):
		return self.__label;
	def exchange(self, chromosome, prob):
		import numpy as np;
		import chromosome as c;
		event = np.random.rand(1) < prob;
		chr1 = c.chromosome(np.copy(self.__gI));
		chr2 = c.chromosome(np.copy(chromosome.getGI()));
		if event == True:
			return chr1, chr2;
		else:
			return chr2, chr1;
	def mutate(self, rate):
		import numpy as np	;
		import chromosome as c;
		info = np.copy(self.__gI)	;
		
		mutationVector = np.random.rand(len(info));
		mutationVector[mutationVector < rate] = 0;
		mutationVector[mutationVector > rate] = 1;
		mutationVector = 1 - mutationVector;
		mutations = np.random.rand(len(info));
		mutations[mutations < 0.5] = 0;
		mutations[mutations > 0.5] = 1;
		info[mutationVector == 1] = mutations[mutationVector == 1];
		chr1 = c.chromosome(info);
		return chr1;
	def plotInfo(self):
		import matplotlib.pyplot as plt;
		displayMatrix = np.zeros((self.__length*10, 100));
		for iter in range(self.__length):
			displayMatrix[(iter*10):((iter+1)*10), :]=self.__gI[iter];
		plt.imshow(displayMatrix);
		plt.axis('off');
		
