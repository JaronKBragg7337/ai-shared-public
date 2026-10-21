# Cabin air model for the sim scenes. Simple, honest, labelled as a simulation.
# 3 m3 sealed pod, 1 atm, 20 C, one person at NASA average metabolic rates. No humidity/heat/pressure effects.
import numpy as np
R=8.314; T=293.15; V=3.0
N0=101325*V/(R*T)                      # mol of gas in pod
CO2_PROD=1.00e3/44.01/86400            # mol/s  (NASA avg 1.00 kg/person-day)
O2_USE  =0.84e3/32.00/86400            # mol/s  (NASA avg 0.84 kg/person-day)
K=1/1200.0                             # 1/s  scrubber flow constant (assumed: pod air cycled through canister, ~20 min e-fold)
KO2_RATIO=0.9                          # mol O2 released per mol CO2 absorbed (assumed mix of the two routes, range 0.75..1.5)
F_CARB=0.2                             # share via carbonate route -> KO2 per CO2 = (1-F)+2F
HOURS=6.0
def run(mode, dt=5.0):
    n=int(HOURS*3600/dt)+1
    o2=0.2095*N0; co2=0.0004*N0; n2=N0-o2-co2
    out=[]; used=0.0
    for i in range(n):
        tot=o2+co2+n2
        out.append((i*dt/3600, 100*co2/tot, 100*o2/tot, used))
        rem = K*co2 if mode!='none' else 0.0
        rel = KO2_RATIO*rem if mode=='ko2' else 0.0
        co2 += (CO2_PROD-rem)*dt; o2 += (-O2_USE+rel)*dt
        if mode=='ko2': used += rem*((1-F_CARB)+2*F_CARB)*71.10*dt
        if mode=='lioh': used += rem*2*23.95*dt
    return np.array(out)
if __name__=='__main__':
    print('N0',N0)
    for m in ('none','lioh','ko2'):
        a=run(m)
        def at(h): return a[int(h*720)]
        print(m,[ (h,round(at(h)[1],3),round(at(h)[2],2),round(at(h)[3],0)) for h in (1,2,3,4,6)])
        c=a[:,1]; 
        for lim in (0.5,4.0):
            idx=np.argmax(c>=lim) if (c>=lim).any() else None
            print('  reaches',lim,'% at', None if idx is None else round(a[idx][0],2),'h')
