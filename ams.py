'''
Implementation of AMS algorithm for computing the second moment
F2 = f1^2 + ... + fk^2, where fi is the frequency of xi
The estimator is Y^2, where Y = sum(h(X)), where h: [U] -> 1, -1
We use h_{a, b}(x) = 1 if (a * x + b) % p is even else -1
Then we use the median of mean
number of median s: O(log(1/delta))
number of mean t: O(1/epsilon^2)
'''
import numpy as np
import random
import matplotlib.pyplot as plt
from collections import defaultdict
EPSILON = 0.1
DELTA = 0.1
MAX_N = 1000
for P in range(MAX_N, MAX_N * 2):
	isPrime = True
	for i in range(2, P):
		if P % i == 0:
			isPrime = False
			break
	if isPrime:
		break

class ams:
	def __init__(self):
		self.s = int(11 * np.log2(1 / DELTA))
		self.t = int(4 / (EPSILON ** 2))
		self.hashParams = [[(random.randint(0, P - 1), random.randint(0, P - 1)) for j in range(self.t)] for i in range(self.s)]
		self.Y = np.zeros((self.s, self.t))
	def put(self, value):
		for i in range(self.s):
			for j in range(self.t):
				a, b = self.hashParams[i][j]
				self.Y[i][j] += 1 if ((a * value + b) % P) % 2 == 0 else -1
	def query(self):
		# Compute the median of mean
		return sorted((self.Y ** 2).mean(axis = 1))[self.s // 2]

myRes = ams()
truth = defaultdict(int)
numExperiments = 500
estimators = np.zeros(numExperiments)
groundTruths = np.zeros(numExperiments)
for i in range(numExperiments):
	if i % 50 == 0:
		print(i)
	curr = random.randint(0, 20)
	truth[curr] += 1
	myRes.put(curr)
	estimators[i] = myRes.query()
	groundTruths[i] = sum([count ** 2 for count in list(truth.values())])
plt.plot(groundTruths, estimators)
plt.show()
