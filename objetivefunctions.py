from itertools import count
from data import C,D,U

#Calculate f1(X) - Average distance between Teacher Home and Establishment
def f1(X):
    result=0
    for classId in range(len(C)):
        teacherId=X[classId]
        establishmentId=C[classId][4]-1
        result=result+U[teacherId][establishmentId] #Add distance between Teacher Home and Establishment
    result=result/len(C)
    return result

#Calculate f2(X) - Average establishment per teacher
def f2(X):
    result=0
    countTeacherAssigned=len(D)
    assign1=-1
    assign2=-1
    for i in range(len(D)):
        assign1=-1
        assign2=-1
        for j in range(len(X)):
            if i==X[j]:
                if assign1==-1:
                    assign1=j
                else:
                    assign2=j
        if(assign1!=-1): #Assigned
            if(assign2!=-1): #Two assigned
                if(C[assign1][4]==C[assign2][4]): #Same Establishment
                    result=result+1
                else: #Diferent Establishment
                    result=result+2
            else: #One assigned
                result=result+1
        else: #Not Assigned
            countTeacherAssigned=countTeacherAssigned-1
    result=result/countTeacherAssigned
    return result

#Calculate f3(X) - Average class per teacher
def f3(X):
    result=0
    countTeacherAssigned=len(D)
    assign1=-1
    assign2=-1
    for i in range(len(D)):
        assign1=-1
        assign2=-1
        for j in range(len(X)):
            if i==X[j]:
                if assign1==-1:
                    assign1=j
                else:
                    assign2=j
        if(assign1!=-1): #Assigned
            if(assign2!=-1): #Two assigned
                result=result+2
            else: #One assigned
                result=result+1
        else: #Not Assigned
            countTeacherAssigned=countTeacherAssigned-1
    result=result/countTeacherAssigned
    return result

def f1_c(X):
    r=[]
    for x in X:
        r.append(f1(x))
    return r

def f2_c(X):
    r=[]
    for x in X:
        r.append(f2(x))
    return r

def f3_c(X):
    r=[]
    for x in X:
        r.append(f3(x))
    return r

def f3_c_min(X):
    r=[]
    for x in X:
        r.append(f3(x)*-1)
    return r