#!/home/charizard/anaconda3/bin/ipython3
import chromosome as c;

class individual ():
	def __init__(self, deepness):
		self.__X = 8;
		self.__Y = 8;
		self.__D = deepness;
		# vS means vertix size
		vS = 16;
		self.__vS = vS;
		# All attributes named as "p_" mean "pointer of _"
		self.__pC = 0; #pointer of colour
		self.__p1 = 8; #pointer of first vertix assuming 256 colours
		self.__p2 = 8 + vS;
		self.__p3 = 8 + (2*vS);
		self.__p4 = 8 + (3*vS);
		self.__p5 = 8 + (4*vS);
		self.__p6 = 8 + (5*vS);
		# Note that we are assuming 4 vertix as much
	def copyIndividual(self):
		ind = individual(self.__D);
		geneticMaterial = [];
		for iter in range(len(self.__geneticMaterial)):
			geneticMaterial.append(self.__geneticMaterial[iter].copy());
		ind.includeInformation(geneticMaterial);
		return ind;
	def getDeepness(self):
		return self.__D;
	def includeInformation(self, chromosomeList):
		import chromosome as c;
		geneticMaterial = [];
		if len(chromosomeList) == self.__D:
			for iter in range(self.__D):
				if type(chromosomeList[iter]) == c.chromosome:
					geneticMaterial.append(chromosomeList[iter]);
				else:
					print("Individual can only accept chromosome as genetic input");
					return 0;
		else:
			print("Individual karyotipe size is different!");
			return 0;
		self.__geneticMaterial = geneticMaterial;
		return 1;
	def getFeatures(self, z):
		import numpy as np;
		import math;
		try: 
			chrom = self.__geneticMaterial[z];
		except AttributeError:
			print("Genetic material is not defined for {0}".format(z));
		code = chrom.getGI();
		colour = self.binaryReader(code[self.__pC:self.__pC+8]);
		v1x = self.binaryReader(code[self.__p1:self.__p1 + self.__X]);
		v1y = self.binaryReader(code[self.__p1 + self.__X:self.__p1 + self.__vS]);
		v2x = self.binaryReader(code[self.__p2:self.__p2 + self.__X]);
		v2y = self.binaryReader(code[self.__p2 + self.__X:self.__p2 + self.__vS]);
		v3x = self.binaryReader(code[self.__p3:self.__p3 + self.__X]);
		v3y = self.binaryReader(code[self.__p3 + self.__X:self.__p3 + self.__vS]);
		v4x = self.binaryReader(code[self.__p4:self.__p4 + self.__X]);
		v4y = self.binaryReader(code[self.__p4 + self.__X:self.__p4 + self.__vS]);
		v5x = self.binaryReader(code[self.__p5:self.__p5 + self.__X]);
		v5y = self.binaryReader(code[self.__p5 + self.__X:self.__p5 + self.__vS]);
		v6x = self.binaryReader(code[self.__p6:self.__p6 + self.__X]);
		v6y = self.binaryReader(code[self.__p6 + self.__X:self.__p6 + self.__vS]);
		pos = [[v1x, v1y],[v2x, v2y],[v3x, v3y],[v4x, v4y],[v5x,v5y],[v6x,v6y]];
		pos = np.array(pos);
		moduleDist = np.zeros(6);
		for iter in range(6):
			moduleDist[iter] = self.module(pos[iter,:], [0,0]);
		# sP -> starting point
		sP = moduleDist.argmin();
		# lP -> list of points in the envelope
		lP = list();
		while not sP in lP:
			lP.append(sP);
			minAng = 1e3; # Just some big number
			for iter in range(6):
				if not iter == sP:
					cos = (pos[iter,0] - pos[sP,0]);
					cos = cos / self.module(pos[iter,:], pos[sP,:]);
					ang = math.acos(cos);
					if ang < minAng:
						minAng = ang;
						nSP = iter;
			sP = nSP;
		ordPos = list();
		for iter in range(len(lP)):
			ordPos.append(pos[iter,:]);
		return colour, ordPos;
	def binaryReader(self, string):
		import numpy as np;
		if not type(string) == np.array:
			string = np.array(string);
		counter = 0;
		lenString = len(string);
		for iter in range(len(string)):
			counter = string[iter]*(2**(iter)) + counter;
		return counter;
	def module(self,v1,v2):
		import numpy as np;
		import math;
		return math.sqrt(((v1[0]-v2[0])**2)+((v1[1]-v2[1])**2)) + 1e-6;
	def getGeneticMaterial(self,z):
		try:
			return self.__geneticMaterial[z];
		except AttributeError:
			return "Individual has no genetic material for deepness {0}".format(z);
	def getAllGeneticMaterial(self):
		chrList = [];
		for iter in range(self.__D):
			chrList.append(self.__geneticMaterial[iter].copy());
		return chrList;
	def reproduce(self, match):
		if type(match) == individual:
			if match.getDeepness() == self.__D:
				listNewOwnChr = [];
				listNewOtherChr = [];
				for iter in range(self.__D):
					u = self.__geneticMaterial[iter];
					v = match.getGeneticMaterial(iter);
					a,b = u.exchange(v, 0.25);
					listNewOwnChr.append(a);
					listNewOtherChr.append(b);
				i1 = individual(self.__D)
				i2 = individual(self.__D);
				i1.includeInformation(listNewOwnChr);
				i2.includeInformation(listNewOtherChr);
				return i1, i2;
			else:
				print("Individuals can not match since they have different deepness");
		else:
			print("Individuals can only have sex with other individuals");
		return 0;
	def mutate(self, prob, nC):
		import numpy as np;
		for iter in range(nC):
			chrChossen = np.random.randint(0, high=self.__D, size=1);
			u = self.__geneticMaterial[chrChossen[0]];
			u = u.mutate(prob);
			self.__geneticMaterial[chrChossen] = u;
		return 1	
	def mutateMod(self, prob, nC):
		import numpy as np;
		u = self.__geneticMaterial[nC];
		u = u.mutate(prob);
		self.__geneticMaterial[nC] = u;
		return 1
