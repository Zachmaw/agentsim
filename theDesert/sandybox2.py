import matplotlib.pyplot as plt
import numpy as np
from scipy.special import expit
x = np.linspace(-4, 4, 121)
y = expit(x)
plt.plot(x, y)
plt.grid()
plt.xlim(-4, 6)
plt.xlabel('x')
plt.title('expit(x)')
plt.show()