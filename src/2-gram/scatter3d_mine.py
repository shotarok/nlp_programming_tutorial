import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for line in iter(sys.stdin.readline, ""):
    x, y, z = map(lambda x: float(x), line.rstrip().split())
    ax.scatter(x, y, z)

ax.set_xlabel('lambda_one')
ax.set_ylabel('lambda_two')
ax.set_zlabel('entropy')

plt.show()

