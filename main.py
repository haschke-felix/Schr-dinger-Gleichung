from scipy.constants import *
import matplotlib.pyplot as plt
import numpy
from fractions import Fraction

C=Fraction(2.62E19)
K=Fraction(1.44E-9)

def sim( W, DR_ =1E-14,   r_start=1e-14, psi_start=0, psi1_start=1,  n=1000):
    R = Fraction(r_start)
   
    DR=Fraction(DR_)
    #W= -3.39418966425 #-1.50873324/4 #-1.50873324; -3,4; -13.6 
    psi = Fraction(psi_start)
    psi1 = Fraction(psi1_start)
    psi2 = Fraction(0)
    
    
    data_x = []
    data_psi =  []

    for i in range(n):
        WP = Fraction(-K/R)
        psi2 = -C*(W-WP)*psi
        psi1 = psi1 + psi2 * DR
        psi = psi + psi1 * DR
        R += DR
        data_psi.append(psi)
        data_x.append( R)

    return data_x, data_psi

def coulomb(x):
    if x == 0:
        raise Exception('Coulomb potential cannot be determinted for x=0')
    return - elementary_charge**2 / (4 * pi * epsilon_0 * x)
    
radius_proton=0.88e-12    

#x, psi = sim(n=3000)

def approx(startW, nStart, targetN=3000, DN=1000, targetD=1e-12):
    DW = Fraction(0.01)
    W= Fraction(startW)
    n = nStart
    D = 1
    last = "n"
    #plt.ion()
    while (n < targetN or D > targetD):
        x, y = sim(n=n, W = float(W))
        D =  y[n-1]
        plt.clf()
        plt.plot(x,y)
        plt.pause(0.0001)
        if D < -targetD:
            if last == "above":
                DW /= 1.5
            W += DW
            last = "below"
        elif D > targetD:
            if last == "below":
                DW /=2
            W -= DW
            last = "above"
        else:
            n += DN
            last = "none"
        print("n: ", n, "W: ", float(W), "DW: ", float(DW), "last:", last, "D:", D)
    return float(W)

n= 1000000
W = approx(startW=-3.4, nStart=100000, targetN=n, DN=1000)
print(W)
x, psi = sim(n=n, W=W)

#plt.plot(x,psi)
#plt.plot(s[0], numpy.square(s[1])*3e10)

plt.show()
