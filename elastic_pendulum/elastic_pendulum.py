#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import math

#Starting Parameters:
dt = 10**(-3) #time step
T = 10 #time Range

phi0_degr = 60 #Angle in Degrees
w0 = 0 #Angular Velocity
L0 = 0 #Lenght of Springdisplacement
v0 = 0 #Velocity of Springlength

L_0 = 2 #Base-Length of spring
m = 0.5 #mass
g = 10 #Gravity
k = 1 #Spring-constant

phi0 = (phi0_degr*math.pi)/180 #degrees to radians

#EOM:
    #   phidot = w
    #   Ldot = v

def vdot_eq(L, phi, w):
    spring_len = (L_0+L)
    return spring_len*(w**2)+g*math.cos(phi)-(k/m)*L

def wdot_eq(L, v, phi, w):
    spring_len = (L_0+L)
    return (-2/spring_len)*w*v-(g/spring_len)*math.sin(phi)

#Euler Func:
def euler(vdot_eq, wdot_eq, L0, v0, phi0, w0, dt, T):
    n = int(round(T/dt))
        
    L = np.zeros(n+1)
    v = np.zeros(n+1)
    phi = np.zeros(n+1)
    w = np.zeros(n+1)
    t = np.zeros(n+1)

    L[0] = L0
    v[0] = v0
    phi[0] = phi0
    w[0] = w0
    t[0] = 0

    for k in range(n):
        t[k+1] = t[k] + dt    
        L[k+1] = L[k] + v[k]*dt
        phi[k+1] = phi[k] + w[k]*dt
        v[k+1] = v[k] + vdot_eq(L[k], phi[k], w[k])*dt
        w[k+1] = w[k] + wdot_eq(L[k], v[k], phi[k], w[k])*dt
    return L, v, phi, w, t

#Do the Calculations:
L, v, phi, w, t = euler(vdot_eq, wdot_eq, L0, v0, phi0, w0, dt, T)

length = np.zeros(len(t)) #total length of Spring
for i in range(len(t)):
    length[i] = L_0 + L[i]

#converting to x-y:
    #x = (L_0+L)sin(phi)
    #y = -(L_0+L)cos(phi)

x = np.zeros(len(t))
y = np.zeros(len(t))
for i in range(len(t)):
    x[i] = length[i]*math.sin(phi[i])
    y[i] = (-1)*length[i]*math.cos(phi[i])
    #print(x[i], y[i]) #uncomment to get values printed to console
#Plotting:
fig, ax = plt.subplots(2,2)

ax[0][0].plot(t, L, label="Lenght of Springdisp.")
ax[0][0].plot(t, v, label="Change-rate of Spring")
ax[0][1].plot(t, phi, label="Angle")
ax[0][1].plot(t, w, label="Angular Velocity")
ax[1][0].plot(x, y, label="x-y Plane")
ax[1][1].plot(t, x, label="x-t")
ax[1][1].plot(t, y, label="y-t")

for i in range(2):
    for k in range(2):
        ax[i][k].grid()
        ax[i][k].legend()
        ax[i][k].set_xlabel("time")
ax[1][0].set_xlabel("x")
ax[1][0].set_ylabel("y")

plt.tight_layout()
plt.show()

