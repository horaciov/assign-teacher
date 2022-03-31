from data import C,V,Dmax

#Compute all restrictions
def validateConstraints(X):
    #One teacher with up to two classes with different shifts 
    valid=True
    for index1 in range(len(C)):
        c=1
        for index2 in range(len(C)):
            if(index1!=index2 and X[index1]==X[index2]):
                c=c+1
                if(c>2):#More than 2 assigs
                    valid=False
                    break
                if(C[index1][1]==C[index2][1]):#Same shifts
                    valid=False
                    break
                if(V[C[index1][4]-1][C[index2][4]-1]>Dmax):#Maximun distances exceeded
                    valid=False
                    break
                
    return valid