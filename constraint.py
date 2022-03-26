from data import C

#Compute all restrictions
def validateConstraints(X):
    #One teacher with up to two classes with different shifts 
    valid=True
    for index1 in range(len(C)):
        c=1
        for index2 in range(len(C)):
            if(index1!=index2 and X[index1]==X[index2]):
                c=c+1
                if(C[index1][1]==C[index2][1]):
                    valid=False
                    break
        if(c>2):
            valid=False
            break
    return valid