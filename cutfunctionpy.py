import numpy as np

def cut(xx,threshold,E):
    mysum=[]
    mymul=[]
    myvar=[]
    index1=[]
    x=xx
    
    
    for i in range(0,x.shape[0]):

        
        Tobesum=np.where(x[i][:(x.shape[1]-1)] < threshold, 0, x[i][:(x.shape[1]-1)])
        x[i][:(x.shape[1]-1)]=np.where(x[i][:(x.shape[1]-1)] < threshold, 0, x[i][:(x.shape[1]-1)])
        compare=Tobesum > 55
        localsum=np.sum(Tobesum)
        if True in compare or localsum < E:
            index1.append(i)
            
        elif True in compare and localsum < E:
            index1.append(i)
        
        else:
            
            mysum.append(localsum)        
            mymul.append(np.count_nonzero(Tobesum))
            myvar.append((np.std(Tobesum))**2.0)
    newx=np.delete(x,index1,axis=0)
    return (mysum,mymul,newx,myvar)