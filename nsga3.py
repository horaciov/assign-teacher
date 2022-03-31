from numpy import random
from math import factorial
from deap import base, creator, tools, algorithms
from data import C,D
from objetivefunctions import f1,f2,f3
from constraint import validateConstraints

#Parameters
CLASS_SIZE=len(C)
TEACHER_SIZE=len(D)
NOBJ=3 #Number of objectives
P=12 #Number of partitions
H = factorial(NOBJ + P - 1) / (factorial(P) * factorial(NOBJ - 1))
MU = int(H + (4 - H % 4)) #Population size
NGEN = 10 # Number of generations
CXPB = 1.0 #crossover probability
MUTPB = 1.0 #chance to mutate

ref_points = tools.uniform_reference_points(NOBJ, P)

#Min Min Max multi objetice and individual
creator.create("FitnessMulti", base.Fitness, weights=(-1.0,-1.0,1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register("teacher", random.randint, 0, TEACHER_SIZE-1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.teacher, n=CLASS_SIZE)


#Operators
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=TEACHER_SIZE-1, indpb=0.1)
toolbox.register("select", tools.selNSGA3, ref_points=ref_points)

def evaluate(X):
    return [f1(X),f2(X),f3(X)]

toolbox.register("evaluate", evaluate)


#Generate and evaluate the entire population
pop = []
while(len(pop)<MU):
    ind=toolbox.individual()
    if validateConstraints(ind):
        ind.fitness.values=evaluate(ind)
        pop.append(ind)

 # Begin the generational process
for gen in range(1, NGEN):
    offspring = algorithms.varAnd(pop, toolbox, CXPB, MUTPB)
    
    #Discard invalid individual
    offspring=list(filter(validateConstraints,offspring))
    
    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    
    # Select the next generation population from parents and offspring
    pop = toolbox.select(pop + offspring, MU)

#Non-dominated solutions
ND=[]

#Search Non-dominated Solutions
for i1 in range(len(pop)):
    isNonDominated = True
    for i2 in range(len(pop)):
        if i1!=i2:
            if pop[i1].fitness.values[0]>pop[i2].fitness.values[0] or pop[i1].fitness.values[1]>pop[i2].fitness.values[1] or pop[i1].fitness.values[2]<pop[i2].fitness.values[2]: # Min f1, Min f2, Max f3
                isNonDominated=False
    if isNonDominated:
        ND.append(pop[i1])

print("Población: "+str(len(pop)))
print("Cantidad de soluciones no dominadas: "+str(len(ND)))
for i in ND:
    print(str(i) + " "+str(i.fitness.values))