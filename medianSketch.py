'''
Implementation of median of Y:
	Assume the elements of stream are nonnegative integers <= MAX_N
	p > 20k is a prime
	h_{a, b}(x) = (ax + b) % p
	Y = min(h_{a, b}(x) / p)
	O(log(1/delta)) copies of Y
'''
import numpy as np
import random
import matplotlib.pyplot as plt
DELTA = 0.1
MAX_N = 1000
for P in range(MAX_N * 20, MAX_N * 40):
	isPrime = True
	for i in range(2, P):
		if P % i == 0:
			isPrime = False
			break
	if isPrime:
		break
class medianSketch:
	def __init__(self):
		self.numCopy = int(11 * np.log2(1 / DELTA))
		self.sketch = np.ones(self.numCopy)
		self.hashParams = [(random.randint(0, P - 1), random.randint(0, P - 1)) for i in range(self.numCopy)]
	def put(self, value):
		for idx, (a, b) in enumerate(self.hashParams):
			# Update the sketch with the new hash value if it's smaller
			currHashVal = ((a * value + b) % P) / P
			self.sketch[idx] = min(self.sketch[idx], currHashVal)
	def query(self):
		# Return reciprocal of median of sketch
		return 1 / sorted(self.sketch)[self.numCopy // 2]
# Test out the code
ms = medianSketch()
est = np.zeros(MAX_N * 10)
truth = set()
groundTruth = np.zeros(MAX_N * 10)
for experiment in range(MAX_N * 10):
	curr = random.randint(0, MAX_N)
	ms.put(curr)
	truth.add(curr)
	est[experiment] = ms.query()
	groundTruth[experiment] = len(truth)
plt.plot(groundTruth, est)
plt.plot(groundTruth, groundTruth * 3)
plt.plot(groundTruth, groundTruth / 3)
plt.xlabel('True number of distinct elements')
plt.ylabel('Estimated number of distinct elements')
plt.savefig('medianSketch')
plt.close()
