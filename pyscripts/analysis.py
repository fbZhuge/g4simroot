import csv
import numpy as np

numberOfVoxelsPerAxis = 9
water_cube = np.empty(shape=(numberOfVoxelsPerAxis,numberOfVoxelsPerAxis,numberOfVoxelsPerAxis), dtype=np.double)

def coord_from_copyno(copyno, numberOfVoxelsPerAxis):
    i = copyno%10
    j = ((copyno-i)//10)%10
    k = (((copyno-i)//10)-j)%10
    return (i, j, k)

def copyno_from_coord(i, j, k, numberOfVoxelsPerAxis):
    return i+10*j+100*k

filepath = "/home/kaiju/github/research/Geant4Sim/build/hits_csv.csv"
with open(filepath, newline='') as f:
    hits=csv.reader(f)
    for row in hits:
        voxel=int(row[0])
        edep=np.double(row[1])
        i, j, k = coord_from_copyno(voxel, numberOfVoxelsPerAxis)
        water_cube[i, j, k]+=edep
        # print(f"the energy deposied in {voxel} is {edep}")

for i in range(numberOfVoxelsPerAxis):
    for j in range(numberOfVoxelsPerAxis):
        for k in range(numberOfVoxelsPerAxis):
            copy=copyno_from_coord(i, j, k, numberOfVoxelsPerAxis)
            print(f"the energy deposited in {copy} is {water_cube[i, j, k]} MeV")


import matplotlib.pyplot as plt
import numpy as np


# prepare some coordinates
x, y, z = np.indices((numberOfVoxelsPerAxis, numberOfVoxelsPerAxis , numberOfVoxelsPerAxis))
print(f"{x.shape=}")
cube = (x < numberOfVoxelsPerAxis) & (y < numberOfVoxelsPerAxis) & (z < numberOfVoxelsPerAxis)
print(f"{cube.shape=}")
# combine the objects into a single boolean array
voxelarray = cube
water_cube = np.swapaxes(water_cube,1,2)
vox = np.array(water_cube, dtype=bool)
print(f"{water_cube.shape=}")
# set the colors of each object
colors = np.empty(voxelarray.shape, dtype=object)
colors[cube] = 'red'

# and plot everything
ax = plt.figure().add_subplot(projection='3d')
ax.voxels(vox, facecolors=colors, edgecolor='k')

plt.show()
