#!/home/charizard/anaconda3/bin/ipython3
class fitness():
	def __init__(self,inpath):
		from PIL import Image; 
		import numpy as np;
		self.inpath =  inpath;
		self.picture = np.asarray(Image.open(self.inpath).convert('L'));
		self.__X, self.__Y = self.picture.shape;
	def evaluateIndividual(self,individual):
		import numpy as np;
		forgedImage = self.extractPicture(individual);	
		difR = np.sum(np.abs(forgedImage - self.picture));
		return difR;
	def plotForgedImage(self,individual, name, fitness):
		import numpy as np;
		import matplotlib.pyplot as plt;
		forgedImage = self.extractPicture(individual);
		plt.imshow(forgedImage, cmap='gray', clim=(0,255)); 
		plt.title("{0} - F = {1}".format(name, fitness))
		plt.savefig(name+'.png');
		return 1;
	def evaluateIndividualOverPicture(self, individual, canvas, iZ):
		import numpy as np;
		import math as M;
		import cv2;
		blackCanvas = np.zeros((self.__X, self.__Y));
		coefTransCanvas = (1-(1/(iZ+1)));
		coefTransPolygon = 1/(iZ+1);
		canvas = canvas * coefTransCanvas;
		color, poS = individual.getFeatures(iZ);
		poS= np.array(poS, np.int32);
		poS.reshape((-1,1,2));
		forgedImage = canvas + cv2.fillPoly(canvas, [poS], (color*coefTransPolygon));
		return np.sum(np.abs(forgedImage - self.picture));
	def extractPicture(self,individual):
		import numpy as np;
		import math as M;
		import cv2;
		canvas = np.zeros((self.__X, self.__Y));
		forgedImage = np.zeros((self.__X, self.__Y));
		coefTrans = 1/individual.getDeepness();
		for iZ in range(0,individual.getDeepness()):
			color, poS = individual.getFeatures(iZ);
			poS = np.array(poS, np.int32);
			poS = poS.reshape((-1,1,2)); 
			forgedImage = forgedImage + cv2.fillPoly(canvas,[poS],int(color*coefTrans));
		return forgedImage;
