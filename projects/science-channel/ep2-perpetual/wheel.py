# Overbalanced wheel, simulated.  N weights (1 kg) on arms; arm swings OUT on the right (descending) half, folds IN on the left.
# Weight radius depends only on its lab-frame position -> gravity is a conservative force -> zero net work per turn.
import math, numpy as np
N=8; M=1.0; G=9.81; R_IN=0.15; R_OUT=0.45; RIM=0.30   # metres (illustrative desk-size wheel)
def rho(x):                       # x = cos(alpha) of the pivot (right side > 0)
    s = 0.5 + 0.5*math.tanh(x*5.0)
    return R_IN + (R_OUT-R_IN)*s
def pos(theta):
    out=[]
    for i in range(N):
        a = theta + 2*math.pi*i/N
        r = rho(math.cos(a)); out.append((r*math.cos(a), r*math.sin(a), r))
    return out
def U(theta): return sum(M*G*p[1] for p in pos(theta))
def I(theta): return sum(M*p[2]**2 for p in pos(theta))
TC=0.0
def _acc(th, om, b):
    h=1e-5
    dU=(U(th+h)-U(th-h))/(2*h); dI=(I(th+h)-I(th-h))/(2*h)
    return (-dU - 0.5*dI*om*om - b*om - TC*math.tanh(om/0.05))/I(th)
def simulate(theta0, omega0, b, T, dt=0.002):
    th, om = theta0, omega0; heat = 0.0; out=[]
    U0 = min(U(0.01*k) for k in range(0, 800))
    n = int(T/dt)
    for k in range(n+1):
        if k % 5 == 0:
            out.append((k*dt, th, om, 0.5*I(th)*om*om, U(th)-U0, heat))
        k1t, k1o = om, _acc(th, om, b)
        k2t, k2o = om+0.5*dt*k1o, _acc(th+0.5*dt*k1t, om+0.5*dt*k1o, b)
        k3t, k3o = om+0.5*dt*k2o, _acc(th+0.5*dt*k2t, om+0.5*dt*k2o, b)
        k4t, k4o = om+dt*k3o, _acc(th+dt*k3t, om+dt*k3o, b)
        heat += (b*om*om + TC*math.tanh(om/0.05)*om)*dt
        th += dt/6*(k1t+2*k2t+2*k3t+k4t); om += dt/6*(k1o+2*k2o+2*k3o+k4o)
    return np.array(out)
if __name__=='__main__':
    for b in (0.0, 0.05):
        s=simulate(0.3, 2.6, b, 40)
        tot=s[:,3]+s[:,4]+s[:,5]
        print('b',b,'turns',(s[-1,1]-s[0,1])/(2*math.pi),'E range',tot.min(),tot.max(),'KE0',s[0,3],'end om',s[-1,2],'heat',s[-1,5])
        for k in range(0,len(s),200): print(round(s[k,0],1),round(s[k,2],2),round(s[k,3],2),round(s[k,4],2),round(s[k,5],2))
