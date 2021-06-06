import matplotlib.pyplot as plt
import numpy as np
import math

"""
Part A section C
"""
def fieldDirection(t,w):
    Ep = 4*np.cos(w*t)
    Es = 4*np.cos(w*t-math.pi/2)
    return (Ep,Es)

"""
Part A section D
"""    
t = 3
w = 1
p = 0
s = 0

Ep, Es = fieldDirection(t,w)

u,v = np.meshgrid(Ep, Es)

fig, ax = plt.subplots()

ax.quiver(p,s,u,v)

plt.title("Field Polarization at t=3 sec")
plt.xlabel("p axis")
plt.ylabel("s axis")

plt.savefig('polar3.png')
plt.show()