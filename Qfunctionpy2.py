import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from textwrap import wrap
import io,os,glob
from scipy.optimize import curve_fit
import sys



def JustQuench(txt2, pid):
    #txt1 is EM
    #txt2 is nuclear recoil
    newtxt=np.zeros((txt2.shape[0],txt2.shape[1]))
    
    #add Sodium quenching 
    RecoilEJoo=[8.7,14.8,22.7,30.1,46.1,62.6,78.9,102.7,151.6]
    QJoo=[0.096,0.113,0.141,0.172,0.173,0.181,0.213,0.221,0.229]
    
    #add Iodine quenching 0.08
    RecoilEJoo2=[18.9,28.7,62.2,74.9]
    QJoo2=[4.3/100,4.7/100,5.6/100,5.9/100]

    
    #define Quenching curve_fit
    def myf(x,a,b):
        e=b*x
        g=3*(e**0.15)+0.7*(e**0.6)+e
        return a*g/(1+a*g)
    
    
    if pid==1000110230:
        RecoilE=RecoilEJoo
        Q=QJoo
        
    elif pid==1000531270:
        RecoilE=RecoilEJoo2
        Q=QJoo2       
    
    else:
        print ("no quenching for this pid")
        sys.exit()
    
    popt, pcov = curve_fit(myf, RecoilE, Q)
    print("a =", popt[0], "+/-", pcov[0,0]**0.5)
    print("b =", popt[1], "+/-", pcov[1,1]**0.5)
    
    for i in range(0, txt2.shape[0]):
        end=txt2.shape[1]-1
        newtxt[i][0:end]=np.where(txt2[i][0:end] < 0, 0, txt2[i][0:end])
        localsum=np.sum(newtxt[i][0:end])
        myQ=myf(localsum*1000,popt[0],popt[1])
        newtxt[i][0:end]=newtxt[i][0:end]*myQ
        newtxt[i][end]=txt2[i][end]

    return newtxt