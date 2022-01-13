from scipy.constants import *
import matplotlib.pyplot as plt
import numpy
from fractions import Fraction

totalIt = 0

def sim(x_max=0, W= -3.39418966425,  r_start=1e-14, psi_start=0, psi1_start=1,  n=1000):
    R = r_start
   
    C= 2.62E19  #2*electron_mass / (hbar*hbar)
    K= 1.44E-9 #elementary_charge*elementary_charge / (4 * pi *epsilon_0)
    DR=1E-13
    #W= -3.39418966425 #-1.50873324/4 #-1.50873324; -3,4; -13.6 
        
    psi = psi_start
    psi1 = psi1_start
    psi2 = 0
    
    
    data_x = numpy.empty((n))
    data_psi = numpy.empty((n))

    for i in range(n):
        WP = -K/R
        psi2 = -C*(W-WP)*psi
        psi1 = psi1 + psi2 * DR
        psi = psi + psi1 * DR
        R += DR
        data_psi[i] = psi
        data_x[i] = R

    return data_x, data_psi

def coulomb(x):
    if x == 0:
        raise Exception('Coulomb potential cannot be determinted for x=0')
    return - elementary_charge**2 / (4 * pi * epsilon_0 * x)
    
radius_proton=0.88e-12    

#x, psi = sim(n=3000)

def approx(startW, nStart, targetN=3000, NStep=10000, targetD=1e-12, dw=0.1):
    global totalIt
    DW = Fraction(dw)
    W= Fraction(startW)
    n = nStart
    D = 1
    last = "n"
    #plt.ion()
    while (n < targetN or D > targetD):
        totalIt+=1
        x, y = sim(n=n, W = float(W))
        Dold = D
        D =  y[n-1]
        plt.clf()
        plt.plot(x,y, label="Potential=" + str(float(W)))
        plt.legend()
        
        plt.pause(0.0001)
        if D < -targetD:
            if last == "above":
                DW /= 2
            W -= DW
            last = "below"
        elif D > targetD:
            if last == "below":
                DW /=2
            W += DW
            last = "above"
        else:
            n += NStep
            last = "none"
        print("n: ", n, "W: ", float(W), "DW: ", float(DW), "last:", last, "D:", D)
    return float(W)

def single(Wstart):
    n = 20000
    W = approx(startW=Wstart, nStart=1000, targetN=n, NStep=100)
    print(W)
    plt.show()

def all():
    Wstart = [(-1.5,0.1,30000), (-3.4,-0.1,30000), (-13.6,0.1,22000)]
    #n= 30000
    plots = []
    for w, dw, n in Wstart:
        W = approx(startW=w, nStart=10000, targetN=n, NStep=2000, dw=dw)
        print(W)
        plots.append((*sim(W=W, n=n), W))

    print("Iteration performed: ", totalIt)
    plt.clf()
    for x,y, w in plots:
        plt.plot(x,y, label="Potential=" + str(w))
    plt.legend()
    plt.show()

all()

#single(-3.4)
