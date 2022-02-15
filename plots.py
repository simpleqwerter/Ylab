
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
plt.axes()

circle = plt.Circle((0, 0), radius=7.75, fc='g', edgecolor='black')
rectangle = plt.Rectangle((10,10), width=8, height=6, fc='r',edgecolor='black')
poly = ptch.CirclePolygon((20,20), radius=10, resolution=1000) # Circle

points = [[7, 7],  [15,15], [-15, 15]]
line = plt.Polygon(points, closed=True, fill='g', edgecolor='r')

plt.gca().add_patch(circle)
plt.gca().add_patch(rectangle)
plt.gca().add_patch(line)
plt.gca().add_patch(poly)


plt.axis('scaled')
plt.show()



##################### create 3d axes
fig = plt.figure()

ax = plt.axes(projection='3d')

# set title
ax.set_title('Learning about 3D plots')

plt.show()
