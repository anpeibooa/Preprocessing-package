import numpy as np


def cut(xx,threshold,E):
    mysum=[]
    mymul=[]
    myvar=[]
    index1=[]
    
    x=np.zeros((xx.shape[0],xx.shape[1]))
    
    for i in range(0,x.shape[0]):

        
        x[i][:(xx.shape[1]-1)]=np.where(xx[i][:(xx.shape[1]-1)] < threshold, 0, xx[i][:(xx.shape[1]-1)])
        x[i][xx.shape[1]-1]=xx[i][xx.shape[1]-1]
        compare=x[i][:(xx.shape[1]-1)] > 55
        localsum=np.sum(x[i][:(xx.shape[1]-1)])
        if True in compare or localsum < E:
            index1.append(i)
            
        elif True in compare and localsum < E:
            index1.append(i)
        
        else:
            
            mysum.append(localsum)        
            mymul.append(np.count_nonzero(x[i][:(xx.shape[1]-1)]))
            myvar.append((np.std(x[i][:(xx.shape[1]-1)]))**2.0)
    newx=np.delete(x,index1,axis=0)
    return (mysum,mymul,newx,myvar)
