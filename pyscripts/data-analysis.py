import csv
import numpy as np

NbVoxelsPerAxe=10  # from 1 to 99, it must much numberOfDetectors in construction.cc in Geant4
water_voxel=np.zeros(shape=(NbVoxelsPerAxe,NbVoxelsPerAxe,NbVoxelsPerAxe),dtype=np.double)

def coordinates_from_chamber_nb(chamber_number, vox_per_axis):
    chamber_number=int(row[0])
    if(vox_per_axis<=9):
        i=chamber_number%10
        j=((chamber_number-i)//10)%10
        k=(((chamber_number-i)//10) - j)//10
        return (i,j,k)
    elif(10<=vox_per_axis<=99):
        i=chamber_number%100
        j=((chamber_number-i)//100)%100
        k=(((chamber_number-i)//100) - j)//100
        return (i,j,k)
    else:
        i=chamber_number%1000
        j=((chamber_number-i)//1000)%1000
        k=(((chamber_number-i)//1000) - j)//1000
        return (i,j,k)

def chamber_nb_from_coordinates(i, j, k, vox_per_axis):
    if(vox_per_axis<=9):
        return i+10*j+100*k
    elif(10<=vox_per_axis<=99):
        return i+100*j+10000*k
    else:
        return i+1000*j+1000000*k

# open the csv log file and stor the edp in each voxel in a tensor
filename='/home/iap_school/github/g4simRoot/build/csv_files/run01.csv'
with open(filename, newline='') as csvfile:
    f = csv.reader(csvfile)
    for row in f:
        chamberNb=int(row[0])
        edep=np.double(row[1])
        i,j,k=coordinates_from_chamber_nb(chamberNb, NbVoxelsPerAxe)
        water_voxel[i,j,k]+=edep

# for i in range(NbVoxelsPerAxe):
#     for j in range(NbVoxelsPerAxe):
#         for k in range(NbVoxelsPerAxe):
#             voxelNb=chamber_nb_from_coordinates(i,j,k,NbVoxelsPerAxe)
#             print(f'ChamberNB = {voxelNb}, i = {i}, j = {j}, k = {k}')
#             print(f'The Energy deposited in the chamber {voxelNb} is {water_voxel[i,j,k]}')

print(f"Water voxel  =\n {water_voxel}")
max_edep=np.max(water_voxel)
print(f"maximum energy deposit is {max_edep}")

min_edep=np.min(water_voxel[np.nonzero(water_voxel)])
print(f"minimum energy deposit is {min_edep}")

total_edep=np.sum(water_voxel)
print(f"total energy deposit is {total_edep}")
print(f"lost energy = {1000-total_edep}")

step_energy=(max_edep-min_edep)/6
normalized_water_voxel=water_voxel/max_edep

sum_z_axis=np.zeros(NbVoxelsPerAxe)
for k in range(NbVoxelsPerAxe):
    for i in range(NbVoxelsPerAxe):
        for j in range(NbVoxelsPerAxe):
            sum_z_axis[k]+=water_voxel[i,j,k]

sum_x_axis=np.zeros(NbVoxelsPerAxe)
for i in range(NbVoxelsPerAxe):
    for k in range(NbVoxelsPerAxe):
        for j in range(NbVoxelsPerAxe):
            sum_x_axis[i]+=water_voxel[i,j,k]

sum_y_axis=np.zeros(NbVoxelsPerAxe)
for j in range(NbVoxelsPerAxe):
    for k in range(NbVoxelsPerAxe):
        for j in range(NbVoxelsPerAxe):
            sum_y_axis[j]+=water_voxel[i,j,k]

import matplotlib.pyplot as plt

t = range(1,NbVoxelsPerAxe+1)
# plt.plot(t,sum_z_axis, color="blue")
# plt.xlabel("Z direction")
# plt.ylabel("Energy deposition in Mev")
# plt.title("Z Energy profile")
# plt.show()

# plt.bar(t, sum_z_axis, color="blue")
# plt.show()

#plt.bar(t, sum_x_axis, color="red")
#plt.show()


plt.plot(t, sum_x_axis, color="red")
plt.xlabel("X direction")
plt.ylabel("Energy deposition in eV")
plt.title("X Energy profile")
plt.show()

#plt.bar(t, sum_y_axis, color="green")
#plt.show()

plt.plot(t, sum_y_axis, color="green")
plt.xlabel("Y direction")
plt.ylabel("Energy deposition in Mev")
plt.title("Y Energy profile")
plt.show()
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

# prepare some coordinates
x, y, z = np.indices((NbVoxelsPerAxe, NbVoxelsPerAxe, NbVoxelsPerAxe))

# draw cuboids in the top left and bottom right corners, and a link between them
cube = (x < NbVoxelsPerAxe) & (y < NbVoxelsPerAxe) & (z < NbVoxelsPerAxe)

voxels1 = np.logical_not(cube)
voxels2 = np.logical_not(cube)
voxels3 = np.logical_not(cube)
voxels4 = np.logical_not(cube)
voxels5 = np.logical_not(cube)
voxels6 = np.logical_not(cube)

for i in range(NbVoxelsPerAxe):
    for j in range(NbVoxelsPerAxe):
        for k in range(NbVoxelsPerAxe):
            if (water_voxel[i, j, k] > 0 and water_voxel[i, j, k] <= step_energy):
                voxels1[k,j,i]=True
            if (water_voxel[i, j, k] > step_energy and water_voxel[i, j, k] <= 2*step_energy):
                voxels2[k,j,i]=True
            if (water_voxel[i, j, k] > 2*step_energy and water_voxel[i, j, k] <= 3*step_energy):
                voxels3[k,j,i]=True
            if (water_voxel[i, j, k] > 3*step_energy and water_voxel[i, j, k] <= 4*step_energy):
                voxels4[k,j,i]=True
            if (water_voxel[i, j, k] > 4*step_energy and water_voxel[i, j, k] <= 5*step_energy):
                voxels5[k,j,i]=True
            if (water_voxel[i, j, k] > 5*step_energy and water_voxel[i, j, k] <= max_edep):
                voxels6[k,j,i]=True

voxels = voxels1 | voxels2 | voxels3 | voxels4 | voxels5 | voxels6
voxels_neg = np.logical_not(voxels)
# set the colors of each object
colors = np.empty(cube.shape, dtype=object)
# colors[voxels1] = '#f3d7d0'
# colors[voxels2] = '#e3b0a3'
# colors[voxels3] = '#d18978'
# colors[voxels4] = '#bc634f'
# colors[voxels5] = '#a53b28'
# colors[voxels6] = '#8b0000'
colors[voxels1] = '#FEF001'
colors[voxels2] = '#FFCE03'
colors[voxels3] = '#FD9A01'
colors[voxels4] = '#FD6104'
colors[voxels5] = '#FF2C05'
colors[voxels6] = '#F00505'
colors[voxels_neg] = '0.8'

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.voxels(voxels1, facecolors=colors, edgecolor='black', alpha=0.6)
ax.voxels(voxels2, facecolors=colors, edgecolor='black', alpha=0.6)
ax.voxels(voxels3, facecolors=colors, edgecolor='black', alpha=0.6)
ax.voxels(voxels4, facecolors=colors, edgecolor='black', alpha=0.6)
ax.voxels(voxels5, facecolors=colors, edgecolor='black', alpha=0.6)
ax.voxels(voxels6, facecolors=colors, edgecolor='black', alpha=0.6)
ax.voxels(voxels_neg, facecolors=colors, edgecolor='grey', alpha=0.1)

plt.show(block=True)
