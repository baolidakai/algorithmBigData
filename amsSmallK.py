'''
Implements the estimation of F_k for k < 2
Estimator: Y = \sum f_iX_i, where X_i ~ D_p
To generate X_i, construct theta ~ U[-pi/2, pi/2], r ~ U[0, 1],
X_i = sin(p theta)/(cos(theta))^(1/p) * (cos((1 - p)theta) / log(1/r))^{(1 - p) / p}
Use the median of the absolute value of |Y_i|

To construct a hash function, we need (a, b, c, d):
	theta = - pi / 2 + pi * ((a * x + b) % p) / p
	r = ((c * x + d) % p) / p
'''
import numpy as np
from collections import defaultdict

t = 1000 # Number of different estimators
k = 1000 # Number of maximum possible different elements
p = 0.5
for P in range(k * 10, k * 20):
	isPrime = True
	for i in range(2, P):
		if P % i == 0:
			isPrime = False
			break
	if isPrime:
		break

class momentSketch:
	def __init__(self):
		self.params = [(np.random.randint(P), np.random.randint(P), np.random.randint(P), np.random.randint(P)) for i in range(t)]
		self.Ys = np.zeros(t)
		self.sample = [] # samples from D
	def put(self, value, freq):
		for i in range(t):
			a, b, c, d = self.params[i]
			# Compute two hash values
			theta = - np.pi / 2 + np.pi * ((a * value + b) % P) / P
			r = ((c * value + d) % P + 0.5) / (P + 1)
			# Sample from the p-stable distribution
			x = np.sin(p * theta) / (np.cos(theta) ** (1 / p)) * ((np.cos((1 - p) * theta) / np.log(1 / r)) ** ((1 - p) / p))
			if np.isnan(x):
				print(theta)
				print(r)
			self.Ys[i] += x * freq
			self.sample.append(x)
	def query(self):
		median = sorted(np.abs(self.Ys))[t // 2] / sorted(np.abs(self.sample))[len(self.sample) // 2]
		estimator = median ** p
		return estimator

sk = momentSketch()
counter = defaultdict(float)
for i in range(1000):
	value = np.random.randint(20)
	freq = np.random.randn()
	sk.put(value, freq)
	counter[value] += freq
estimator = sk.query()
groundTruth = sum([np.abs(x) ** p for x in counter.values()])
print('Estimator = %s, ground truth = %s' % (estimator, groundTruth))
