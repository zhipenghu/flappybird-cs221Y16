import json
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


fil = open('qvalues.json', 'r')
qvalues = json.load(fil)
fil.close()

# visValues = {}
xdif = []
ydif = []
vel = []
color = []
for key, value in qvalues.iteritems():
    if value[0] >= value[1]:
        pass
    else:
        color.append('r')
        cod = tuple(key.split('_'))
        xdif.append(int(cod[0]))
        ydif.append(int(cod[1]))
        vel.append(int(cod[2]))

    # cod = tuple(key.split('_'))
    # xdif.append(int(cod[0]))
    # ydif.append(int(cod[1]))
    # vel.append(int(cod[2]))

# ax.scatter(cod[0], cod[1], cod[2], c=color, marker='o')
ax.scatter(xdif, ydif, vel, c=color, marker = 'o')

ax.set_xlabel('Xdif')
ax.set_ylabel('Ydif')
ax.set_zlabel('Vel')

plt.show()