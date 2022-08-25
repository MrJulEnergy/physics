#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

print("VERSION 1.0")
print("In the current setup, the Vehicle mustn't need more than 35s to reach 100km/h")
print("The Green Line indicates the time, where 100km/s is reached. A more precise Value is also printed into the terminal")
print("Please enter floats with a \".\" instead of \",\" (e.g 0.5)")
print("To accept the default, press ENTER")
print("----")

#Starting Parameters:
T = 35 #s
dt = 10**(-3) # Versuch hier mal -5 statt -3

x0 = 1 #m Sarting position
v0 = 0.2 #m/s starting velocity
g = 9.81 #m/s**2 gravity

#Car Specific Parameters:


P = float(input("Power of Vehicle (in kW) (DEFAULT=100) ") or 100) #kW Power
P = P*10**(3)
eta = float(input("Motor Efficiency (DEFAULT=0.4) ") or 0.4)# efficiency
m = float(input("Mass of Vehicle (in kg) (DEFAULT=1000) ") or 1000) #kg Mass of Car
A = float(input("Face Area of Vehicle (in m^2) (DEFAULT=2) ") or 2) #m**2 Front Area of Car
cw = float(input("c_w Value of Vehicle (DEFAULT=0.3) ") or 0.3) #c_w Value
rho = 1.225 #kg/m**3 Air density
mu = float(input("Rolling Friction Coefficient (DEFAULT=0.015) ") or 0.015) #Rolling Friction Coefficient
#print(P, eta, m, A, cw, mu)

#Calculate Konstants:
alpha = (P/m)*eta
beta = (1/(2*m))*A*cw*rho
gamma = mu*g

#EOM:
def vdot(v):
    return alpha/v - beta*(v**2) - gamma 

def xdot(v):
    return v

#Euler
n = int(round(T/dt))

x = np.zeros(n+1)
v = np.zeros(n+1)
t = np.zeros(n+1)

x[0] = x0
v[0] = v0
t[0] = 0

for k in range(n):
    t[k+1] = t[k] + dt
    v[k+1] = v[k] + dt*vdot(v[k])
    x[k+1] = x[k] + dt*xdot(v[k])


#find time of 100km/h
speed = 100/3.6
closest = min(list(v), key=lambda x:abs(x-speed)) #finds closest Element to 100km/h in list
index = list(v).index(closest)
time = t[index]
print("----")
print(f"==>  The Car Accelerated to 100km/h in {round(time, 3)}s  <==")

#Plotting
fig, ax = plt.subplots(1)
ax.plot(t, v, label="v in m/s")
ax.plot([0, T],[27.7, 27.7], lw=2)
ax.plot([time, time], [27.7, 0], lw=2)
ax.set_xlim(0, T)
ax.legend()
ax.grid()
ax.set_xlabel("time in s")
ax.set_ylabel("Velocity in m/s")
plt.show()
