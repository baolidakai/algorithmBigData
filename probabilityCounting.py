'''
Implementation of the probabilistic counting algorithm:
	Idea:
	INCREMENT - add 1 to X w.p. 1 / 2^X
	QUERY - 2^X
'''
import random
import numpy as np
trueCount = 100
DELTA = 0.1
EPSILON = 0.1
def simulateOnce():
	X = 0
	for i in range(trueCount):
		if random.random() < 1 / (2 ** X):
			X += 1
	return 2 ** X
s = int(11 * np.log2(1 / DELTA))
t = int(4 / (EPSILON ** 2))
# We use the median of s average of t
estimates = np.array([[simulateOnce() for j in range(t)] for i in range(s)])
Zs = estimates.mean(axis = 1)
estimator = sorted(Zs)[s // 2]
print('True count is %s, estimator is %s' % (trueCount, estimator))
