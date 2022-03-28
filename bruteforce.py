from data import C,E,D,U,V
from constraint import validateConstraints
from objetivefunctions import f1,f2,f3

#All valid Solutions
P=[]

#Non-dominated solutions
ND=[]
      
#Generate all possible solutions
for class1 in range(len(D)):
    for class2 in range(len(D)):
        for class3 in range(len(D)):
            for class4 in range(len(D)):
                for class5 in range(len(D)):
                    for class6 in range(len(D)):
                        X=[class1,class2,class3,class4,class5,class6]
                        if(validateConstraints(X)):
                            P.append([X,f1(X),f2(X),f3(X)])

#Search Non-dominated Solutions
for i1 in range(len(P)):
    isNonDominated = True
    for i2 in range(len(P)):
        if i1!=i2:
            if P[i1][1]>P[i2][1] or P[i1][2]>P[i2][2] or P[i1][3]<P[i2][3]: # Min f1, Min f2, Max f3
                isNonDominated=False
    if isNonDominated:
        ND.append(P[i1])

print("Cantidad de posibles soluciones: "+str(len(P)))
print("Cantidad de soluciones no dominadas: "+str(len(ND)))
print("Conjunto de soluciones no dominadas: "+str(ND))








