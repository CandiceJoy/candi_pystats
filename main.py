import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
import scipy.special as sc

item = "Monster Slogbone"
term = "Monsters Hunted"
p = 0.03  # Probability of success
k = 1  # Desired successes
nStep = 3  # Number of attempts per trial
probability100 = 0.95  # Numbers >= this are considered 100%; the higher the number, the more points will be clustered near 100%
confidence = 0.8  # Confidence for the Confidence Interval (It will be this % sure that the # of successes is in the interval listed)

if probability100 >= 1.0:
	print("Error: Cannot have guaranteed probability >= 1")
	exit(1)

def formatPercent(num):
	return str("{:.2f}%".format(num * 100))


def formatNumber(num):
	return str("{:.0f}%".format(num * 100))

fig, ax = plt.subplots(1, 1)
lines = 20

# trials * nStep = attempts
attempts = 0  # Number of actual trials fed into binom
trials = 0  # Number of rounds of trials
prob = 0.0

while prob < probability100:
	attempts = attempts + nStep
	trials = trials + 1
	prob = (binom.sf(k, attempts, p) + binom.pmf(k, attempts, p))

print("Attempts to " + formatPercent(probability100) + ": " + formatNumber(attempts))
print("Trials to " + formatPercent(probability100) + ": " + formatNumber(trials))
print("Probability at " + formatNumber(trials) + " trials: " + formatNumber(prob))

step = (trials - 1) / lines
n = sc.round(np.arange(1, trials, step))  # Also the x-coord
y = (binom.sf(k, n * nStep, p) + binom.pmf(k, n * nStep, p)) * 100

ax.plot(n, y, 'bo', ms=8, label="Number of " + term)
ax.vlines(n, 0, y, colors='b', lw=5, alpha=1)

for x1, y1 in zip(n, y):
	ci = binom.interval(confidence, x1 * nStep, p)
	print(str(x1) + " , " + str(y1) + " = " + str(ci))
	label = formatNumber(x1) + "[" + formatNumber(ci[0]) + "," + formatNumber(ci[1]) + "]"
	plt.annotate(label, xy=(x1, y1), xytext=(x1, y1 + 3.5), weight="bold", size=6, ha="center", va="center")

ax.legend(loc='best', frameon=False)
ax.set_xlabel("Number of " + term)
ax.set_ylabel("P( " + item + " >= 1 )")
plt.xlim([1, trials])
plt.ylim([1, 120])
plt.grid()
plt.show()
