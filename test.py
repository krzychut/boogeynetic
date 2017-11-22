import matplotlib.pyplot as plt
import numpy as np

data = np.zeros(5000)
for i in range(100000):
    x = int(np.random.exponential(3)*100)
    if x < 5000:
        data[x] += 1

plt.plot(data)
plt.show()
