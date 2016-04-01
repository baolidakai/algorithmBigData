'''
Implementation of BJKST '02 to estimate the number of distinct elements
t = c / epsilon^2, maintain smallest t hash values h(x)
Estimator: t / (t th smallest)
Compute median of s = O(log(1 / delta)) copies
'''
from heapq import heappush, heappop
import random
import matplotlib.pyplot as plt
import numpy as np
MAX_N = 100
for P in range(MAX_N * 20, MAX_N * 40):
	isPrime = True
	for i in range(2, P):
		if P % i == 0:
			isPrime = False
			break
	if isPrime:
		break
class bjkst:
	def __init__(self, c = 5, EPSILON = 0.1, DELTA = 0.1):
		self.epsilon = EPSILON
		self.delta = DELTA
		self.t = int(c / (self.epsilon ** 2))
		self.s = int(11 * np.log2(1 / DELTA))
		self.hashParams = [(random.randint(0, P - 1), random.randint(0, P - 1)) for i in range(self.s)]
		self.sketch = [[] for i in range(self.s)] # Maintains a list of max heaps containing the smallest t elements
	def put(self, value):
		for i, (a, b) in enumerate(self.hashParams):
			# Compute the new hash value
			currHashVal = (a * value + b) % P / P
			# Update the smallest t hash values
			heappush(self.sketch[i], -currHashVal)
			while len(self.sketch[i]) > self.t:
				heappop(self.sketch[i])
	def query(self):
		# The list of t-th smallest element
		sketch = [-self.sketch[i][0] for i in range(self.s)]
		# Compute the median of sketch
		med = sorted(sketch)[self.s // 2]
		# Return the estimator
		return self.t / med
	def __str__(self):
		return ' '.join(map(str, self.sketch))

bj = bjkst()
numExperiments = 1000
groundTruth = np.zeros(numExperiments)
estimators = np.zeros(numExperiments)
nums = set()
for i in range(numExperiments):
	curr = random.randint(0, 10000)
	nums.add(curr)
	bj.put(curr)
	groundTruth[i] = len(nums)
	estimators[i] = bj.query()
plt.plot(groundTruth, estimators)
plt.plot(groundTruth, groundTruth)
plt.xlabel('Ground Truth')
plt.ylabel('Estimator')
plt.savefig('bjkst')
plt.close()
