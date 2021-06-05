import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft2, fftshift
import math

GRAPH_WIDTH = 10e3 * 2
GRAPH_HIGHT = 10e3 * 2
RESOLUSION = 10

u = np.arange(-GRAPH_WIDTH//2, GRAPH_WIDTH//2, RESOLUSION)
v = np.arange(-GRAPH_HIGHT//2, GRAPH_HIGHT//2, RESOLUSION)
U, V = np.meshgrid(u, v)

#####################
# definitions (in microns)
#####################
wave_length = 0.649 
k = 2*math.pi/wave_length

z_meters = 0.1
z = z_meters * 1e6

#####################
# transfer function
#####################

def circle(u,v):
    R = 500
    r = math.sqrt(u**2 + v**2)
    if (r <= R):
        return 1
    else:
        return 0

T = np.copy(U)
SIZE = np.shape(T)

for i in range(len(U)):
	for j in range(len(U[i])):
		u = U[i][j]
		v = V[i][j]
		
		T[i][j] = circle(u,v)


#########################
# Draw hole
#########################

fig = plt.figure(figsize=(10, 5))
fig.add_subplot(1,2,1)
plt.imshow(T, cmap='gray', extent=[-GRAPH_WIDTH//2, GRAPH_WIDTH//2,-GRAPH_HIGHT//2, GRAPH_HIGHT//2])

E_inc = np.ones(SIZE, dtype='complex_')


########################
# E(u,v,0)
########################
E_0 = 1 * T[u][v]


########################
# fourier transform
########################
nu_factor = 20

S = fftshift(fft2(E_0)/(SIZE[0] * SIZE[1]))

w1 = int(GRAPH_WIDTH*(1-1/nu_factor) / RESOLUSION / 2)
w2 = int(GRAPH_WIDTH*(1+1/nu_factor) / RESOLUSION / 2)
h1 = int(GRAPH_HIGHT*(1-1/nu_factor) / RESOLUSION / 2)
h2 = int(GRAPH_HIGHT*(1+1/nu_factor) / RESOLUSION / 2)

S_sliced = S[w1:w2 , h1:h2]

S = np.kron(S_sliced, np.ones((nu_factor,nu_factor)))

#########################
# Projection Plane
#########################

SCREEN_WIDTH = GRAPH_WIDTH
SCREEN_HIGHT = GRAPH_HIGHT
SCREEN_RES = RESOLUSION

x = np.arange(-SCREEN_WIDTH//2, SCREEN_WIDTH//2, SCREEN_RES)
y = np.arange(-SCREEN_HIGHT//2, SCREEN_HIGHT//2, SCREEN_RES)
X, Y = np.meshgrid(x,y)

E_sphere = np.zeros(X.shape, dtype='complex_')

for i in range(len(X)):
	for j in range(len(X[i])):
		x = X[i][j]
		y = Y[i][j]
		E_sphere[i][j] = (1/z) * (math.e**(-j*k*z)) * \
        (math.e**(-j*k*(math.sqrt(x**2+y**2))/(2*z)))


########################
# E(x,y,z)
########################
E = E_sphere * S


########################
# I, the intensity of the light
########################

I = np.abs(E)

fig.add_subplot(1,2,2)
plt.imshow(I, cmap='gray', extent=[-SCREEN_WIDTH//2, SCREEN_WIDTH//2,-SCREEN_HIGHT//2, SCREEN_HIGHT//2])
plt.show()