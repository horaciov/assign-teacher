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
                            P.append(X)


for X in P:
    XT=[3,0,2,3,0,2]
    if(X==XT):
        print(f1(X))
        print(f2(X))
        print(f3(X))







