'''
Implement the Johnson-Lindenstrauss Transform:
	n points in R^d, map to O(log(n) / epsilon^2) dimensions
	f(v) = 1/sqrt(k)Mv
'''
import numpy as np
import matplotlib.pyplot as plt
import random
n = 10000
d = 1000
epsilon = 0.2
data = np.random.rand(n, d)
k = int(np.log(n) / (epsilon ** 2))
M = np.random.randn(k, d)
sketch = 1 / np.sqrt(k) * data.dot(M.T)
# Compute the pairwise distance
numExperiments = 1000
origDists = np.zeros(numExperiments)
compressedDists = np.zeros(numExperiments)
for counter in range(1000):
	i = random.randint(0, n - 1)
	j = random.randint(0, n - 1)
	origDists[counter] = np.linalg.norm(data[i] - data[j])
	compressedDists[counter] = np.linalg.norm(sketch[i] - sketch[j])
plt.plot(origDists, compressedDists, 'ro')
maxDist = max(origDists.max(), compressedDists.max()) + 1
xs = np.arange(0, maxDist, 0.1)
plt.plot(xs, (1 - epsilon) * xs)
plt.plot(xs, (1 + epsilon) * xs)
plt.xlim([0, maxDist])
plt.ylim([0, maxDist])
plt.savefig('johnsonLindenstrauss')
plt.close()
