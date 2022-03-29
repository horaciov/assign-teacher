import random
from deap import base, creator, tools
from constraint import validateConstraints
from objetivefunctions import f1,f2,f3
from data import C,D

CLASS_SIZE=len(C)
TEACHER_SIZE=len(D)
CXPB, MUTPB, NGEN = 0.5, 0.2,40

#Min Min Max multi objetice
creator.create("FitnessMulti", base.Fitness, weights=(-1.0,-1.0,1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register("teacher", random.randint, 0, TEACHER_SIZE-1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.teacher, n=CLASS_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#Operators
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=TEACHER_SIZE-1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

def evaluate(X):
    return [f1(X),f2(X),f3(X)]

toolbox.register("evaluate", evaluate)

#Generate and evaluate the entire population
pop = []
while(len(pop)<50):
    ind=toolbox.individual()
    if validateConstraints(ind):
        ind.fitness.values=evaluate(ind)
        pop.append(ind)

for g in range(NGEN):
     # Select the next generation individuals
    offspring = toolbox.select(pop, len(pop))

    # Clone the selected individuals
    offspring = list(map(toolbox.clone, offspring))

    # Apply crossover and mutation on the offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    #Discard invalid individual
    offspring=list(filter(validateConstraints,offspring))

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(map(toolbox.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    
    # The population is entirely replaced by the offspring
    pop[:] = offspring

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

