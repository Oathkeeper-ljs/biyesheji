import table_global
import cuckoofilter
import delaunay2D
import numpy as np

"""tg = table_global.table_global()
cf = cuckoofilter.CuckooFilter(capacity=4,bucket_size=4,fingerprint_size=1,max_displacements=500)

cf.insert(["hello",1])
cf.insert(["world",2])
cf.insert(["football",4])
cf.insert(["wanghualu",3])
cf.insert(["liujiangshu",2])
print(cf.buckets)
print(cf.contains("hello"))
print(cf.delete(["hello",1]))
print(cf.buckets)
"""
numSeeds = 10
radius = 100
seeds = radius * np.random.random((numSeeds, 2))
print("seeds:\n", seeds)
print("BBox Min:", np.amin(seeds, axis=0),
      "Bbox Max: ", np.amax(seeds, axis=0))

center = np.mean(seeds, axis=0)
dt = delaunay2D.Delaunay2D(center, 50*radius)

for s in seeds:
    dt.addPoint(s)

print("Input points:\n", seeds)
print ("Delaunay triangles:\n", dt.exportTriangles())

import matplotlib.pyplot as plt
import matplotlib.tri
import matplotlib.collections

fig, ax = plt.subplots()
ax.margins(0.1)
ax.set_aspect('equal')
plt.axis([-1, radius+1, -1, radius+1])

cx, cy = zip(*seeds)
dt_tris = dt.exportTriangles()
ax.triplot(matplotlib.tri.Triangulation(cx, cy, dt_tris), 'bo--')

plt.show()


"""
#a = tg.contains(0)
tg.insert(0,100)
tg.insert(1,101)
print(len(tg.table))
a = tg.delete(0,102)
b = tg.delete(1,100)
c = tg.delete(0,101)
print(tg.table)

print(a)
print(b)
print(c)
d = [[0,1],[1,2]]
print(len(d))
print(d[0])
print([0,] in d)
"""