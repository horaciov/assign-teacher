from deap import algorithms
from math import factorial
from deap import base, creator, tools

#Parameters
NOBJ=3 #Number of objectives
P=12 #Number of partitions
H = factorial(NOBJ + P - 1) / (factorial(P) * factorial(NOBJ - 1))
MU = int(H + (4 - H % 4)) #Population size
NGEN = 400 # Number of generations
CXPB = 1.0 #crossover probability
MUTPB = 1.0 #chance to mutate

ref_points = tools.uniform_reference_points(NOBJ, P)



print(H)