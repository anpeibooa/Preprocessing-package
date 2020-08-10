import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from textwrap import wrap
import io,os,glob
from scipy.optimize import curve_fit
import sys

def Quench(txt1, txt2, txt3):
    #txt1 is EM
    #txt2 is Na nuclear recoil
    #txt3 is I nuclear recoil
    newtxt1=np.zeros((txt1.shape[0],txt1.shape[1]))
    newtxt2=np.zeros((txt2.shape[0],txt2.shape[1]))
    newtxt3=np.zeros((txt3.shape[0],txt3.shape[1]))
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
    
    
   

    
    popt, pcov = curve_fit(myf, RecoilEJoo, QJoo)
    popt2, pcov2 = curve_fit(myf, RecoilEJoo2, QJoo2)
    #print("a =", popt[0], "+/-", pcov[0,0]**0.5)
    #print("b =", popt[1], "+/-", pcov[1,1]**0.5)
    
    for i in range(0, txt1.shape[0]):
        end=txt1.shape[1]-1
        newtxt1[i][0:end]=np.where(txt1[i][0:end] < 0, 0, txt1[i][0:end])
        newtxt2[i][0:end]=np.where(txt2[i][0:end] < 0, 0, txt2[i][0:end])
        newtxt3[i][0:end]=np.where(txt3[i][0:end] < 0, 0, txt3[i][0:end])
        
        localsum_Na=np.sum(newtxt2[i][0:end])
        localsum_I=np.sum(newtxt3[i][0:end])
        
        myQ_Na=myf(localsum_Na*1000,popt[0],popt[1])
        myQ_I=myf(localsum_I*1000,popt2[0],popt2[1])
        
        newtxt2[i][0:end]=newtxt2[i][0:end]*myQ_Na
        newtxt3[i][0:end]=newtxt3[i][0:end]*myQ_I
        
        newtxt1[i][0:end]=newtxt2[i][0:end]+newtxt1[i][0:end]+newtxt3[i][0:end]
        
        newtxt1[i][end]=txt1[i][end]
        newtxt2[i][end]=txt2[i][end]
        newtxt3[i][end]=txt3[i][end]
        
        if newtxt1[i][end] < 10**308:
            newtxt1[i][end]=np.max([newtxt1[i][end],newtxt2[i][end],newtxt3[i][end]])
        
    return newtxt1, newtxt2, newtxt3