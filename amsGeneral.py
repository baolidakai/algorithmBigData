'''
Implements the AMS algorithm for estimating general moment F_k (k > 2)
Use reservoir sampling to sample the variable
t in a random number in {1, ..., m}, R = {j|aj = at, t <= j <= m}
Y = m(g(R) - g(R - 1)) where g(x) = x^k
Expected value of Y is F_k
We use median of mean
'''
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
k = 3 # Estimate F_k
DELTA = 0.1
EPSILON = 0.1
class AMS:
	def __init__(self, x):
		# x is the first value in the stream
		self.m = 1
		self.s = int(11 * np.log2(1 / DELTA))
		self.t = int(4 / (EPSILON ** 2))
		self.R = np.ones((self.s, self.t))
		self.values = np.empty((self.s, self.t)) # All a_t
		self.values.fill(x)
	def put(self, x):
		# Put x in the stream
		self.m += 1
		# Update the samples
		for i in range(self.s):
			for j in range(self.t):
				if np.random.random() <= 1 / self.m:
					self.values[i][j] = x
					self.R[i][j] = 0
		for i in range(self.s):
			for j in range(self.t):
				if self.values[i][j] == x:
					self.R[i][j] += 1
	def query(self):
		# Compute the corresponding Ys
		Ys = (self.R ** k - (self.R - 1) ** k) * self.m
		estimator = sorted(Ys.mean(axis = 1))[self.s // 2]
		return estimator

class exactMoment:
	def __init__(self, x):
		self.counter = defaultdict(int)
		self.counter[x] += 1
	def put(self, x):
		self.counter[x] += 1
	def query(self):
		rtn = 0
		for key in self.counter:
			rtn += self.counter[key] ** k
		return rtn

ams = AMS(1)
em = exactMoment(1)
numExperiments = 1000
groundTruths = np.zeros(numExperiments)
estimators = np.zeros(numExperiments)
for i in range(numExperiments):
	curr = np.random.randint(0, 20)
	ams.put(curr)
	em.put(curr)
	estimators[i] = ams.query()
	groundTruths[i] = em.query()
plt.plot(groundTruths, estimators)
plt.show()
