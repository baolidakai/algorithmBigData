'''
Implementation of counting distinct elements
'''
import numpy as np
import random
import matplotlib.pyplot as plt
DELTA = 0.1 # Failure probability
EPSILON = 0.1 # Approximation accuracy
UPPER_BOUND = 100000 # Upper bound for the elements
P = UPPER_BOUND
# Compute a prime larger than UPPER_BOUND
for p in range(UPPER_BOUND, UPPER_BOUND * 2):
	isPrime = True
	for i in range(2, p):
		if p % i == 0:
			isPrime = False
			break
	if isPrime:
		P = p
		break
N = UPPER_BOUND # Large number for the hash family design

class countDistinctElements:
	'''
	Counts the number of distinct elements in the stream without storing them explicitly
	Assume nonnegative elements <= UPPER_BOUND
	Y = min(h(x)) for x in the stream
	Z = avg(Y1, ..., Yt), t = 4/epsilon^2
	median of Z1, ..., Zs is the final estimation of 1/(k + 1), s = 11log(1/delta)
	Use universal hash family: h_{a, b}(x) = (a * x + b) % p % n / n, with p larger than max value of x
	n larger than the number of distinct elements
	'''
	def __init__(self):
		self.s = int(11 * np.log2(1 / DELTA))
		self.t = int(4 / (EPSILON ** 2))
		self.minimumHashValues = np.ones((self.s, self.t))
		self.hashParameters = [[(random.randint(0, P - 1), random.randint(0, P - 1)) for _ in range(self.t)] for _ in range(self.s)] # params[i][j] contains the parameters for (Zi, Yj)
	def put(self, value):
		'''
		Update the hash values for all hash functions
		'''
		for i in range(self.s):
			for j in range(self.t):
				a, b = self.hashParameters[i][j]
				hashValue = (a * value + b) % P % N / N
				if hashValue < self.minimumHashValues[i][j]:
					self.minimumHashValues[i][j] = hashValue
	def count(self):
		'''
		Return the estimation of the count of different elements
		Not supposed to be called often
		'''
		# Estimate median of mean of minimum Hash values
		Zs = self.minimumHashValues.mean(axis = 1)
		estimator = sorted(Zs)[self.s // 2]
		return int(1 / estimator)

class groundTruthCounter:
	def __init__(self):
		self.counter = set()
	def put(self, value):
		self.counter.add(value)
	def count(self):
		return len(self.counter)

gtc = groundTruthCounter()
cde = countDistinctElements()
numExperiments = 1000
gtcCounts = [None] * numExperiments
cdeCounts = [None] * numExperiments
for i in range(numExperiments):
	# Generate the random value
	curr = random.randint(0, UPPER_BOUND - 1)
	gtc.put(curr)
	cde.put(curr)
	gtcCounts[i] = gtc.count()
	cdeCounts[i] = cde.count()
plt.plot(gtcCounts, cdeCounts)
plt.xlabel('True Count')
plt.ylabel('Estimated Count')
plt.savefig('distinctElements')
