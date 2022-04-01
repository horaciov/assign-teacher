from matplotlib import markers
from numpy import random,mean,std,min,max
from math import factorial
from deap import base, creator, tools, algorithms
from data import C,D
from objetivefunctions import f1,f2,f3
from constraint import validateConstraints
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

#Parameters
CLASS_SIZE=len(C)
TEACHER_SIZE=len(D)
NOBJ=3 #Number of objectives
P=12 #Number of partitions
H = factorial(NOBJ + P - 1) / (factorial(P) * factorial(NOBJ - 1))
MU = int(H + (4 - H % 4)) #Population size
NGEN = 40 # Number of generations
CXPB = 1.0 #crossover probability
MUTPB = 1.0 #chance to mutate

pop = []

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


# Initialize statistics object
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", mean, axis=0)
stats.register("std", std, axis=0)
stats.register("min", min, axis=0)
stats.register("max", max, axis=0)

logbook = tools.Logbook()
logbook.header = "gen", "evals", "std", "min", "avg", "max"


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlabel('X Average Distance')
ax.set_ylabel('Y Average Estableshment')
ax.set_zlabel('Z Average Course')

def init():
    global fig
    print(0)
    #Generate and evaluate the entire population
 
    while(len(pop)<MU):
        ind=toolbox.individual()
        if validateConstraints(ind):
            ind.fitness.values=evaluate(ind)
            pop.append(ind)

    for i1 in range(len(pop)):
        xs=pop[i1].fitness.values[0]
        ys=pop[i1].fitness.values[1]
        zs=pop[i1].fitness.values[2]
        ax.scatter(xs,ys,zs)    



# Begin the generational process
def animate(i):
    print(i)
    global pop, ax
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

     



#anim = FuncAnimation(fig, animate, init_func = init,
 #                   frames = NGEN, interval = 20)
  
   
#anim.save('continuousSineWave.mp4', writer = 'ffmpeg', fps = 2)

init()
animate(0)
animate(0)
animate(0)
animate(0)
animate(0)
animate(0)
animate(0)
animate(0)
animate(0)
animate(0)
animate(0)
animate(0)
animate(0)


plt.clf()
ax = fig.add_subplot(projection='3d')
ax.set_xlabel('X Average Distance')
ax.set_ylabel('Y Average Estableshment')
ax.set_zlabel('Z Average Course')
    
for i1 in range(len(pop)):
    xs = pop[i1].fitness.values[0]
    ys = pop[i1].fitness.values[1]
    zs = pop[i1].fitness.values[2]   
    ax.scatter(xs,ys,zs)   

plt.show()

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