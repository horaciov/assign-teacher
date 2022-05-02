import data
from objetivefunctions import f1, f2, f3
from constraint import validateConstraints
from multiprocessing.pool import ThreadPool
from pymoo.core.problem import ElementwiseProblem, starmap_parallelized_eval
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_crossover, get_mutation
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.core.population import Population
from random import randrange
from geopy import distance

#Initialize
data.init(maxDistance=50)

#Define the Teacher Assign Problem 
CLASS_SIZE = len(data.C)
TEACHER_SIZE = len(data.D)
N_OBJ = 3
N_CONSTR = 3

def generate_ind():
    ind=[-1]*CLASS_SIZE
    teachers=[]
    for i in range(TEACHER_SIZE):
        teachers.append(i)
    c=0
    while(c<CLASS_SIZE):
        print("Cantidad de docentes: "+str(len(teachers)))
        print("Clases asignadas: "+str(c))
        indx=randrange(len(teachers)) #Select a Teacher randomly
        i=teachers[indx]
        teachers.remove(i)
        dist_min=999999
        pos_min=-1
        for j in range(CLASS_SIZE):
            if ind[j]==-1:
                e=data.C[j][4]-1
                dist=distance.distance((data.E[e][1],data.E[e][2]),(data.D[i][1],data.D[i][2])).kilometers
                if dist<dist_min:
                    dist_min=dist
                    pos_min=j
        ind[pos_min]=i
        c=c+1
        if(c==CLASS_SIZE):
            break

        #Search another class for the same teacher that match all constraints with dist min between estableshment
        dist2_min=999999
        pos2_min=-1
        for j in range(CLASS_SIZE): 
            if ind[j]==-1:
                if data.C[j][1]!=data.C[pos_min][1]:
                    e1=data.C[j][4]-1
                    e2=data.C[pos_min][4]-1
                    dist=distance.distance((data.E[e1][1],data.E[e1][2]),(data.E[e2][1],data.E[e2][2])).kilometers
                    if dist<=data.Dmax:
                        if dist<dist2_min:
                            dist2_min=dist    
                            pos2_min=j
        if pos2_min!=-1:
            ind[pos2_min]=i
            c=c+1   
    return ind

pop_0=[]
for i in range(1):    
    pop_0.append(generate_ind())
    print(i)

pop_0 = Population.new("X", pop_0)



class ADEEProblem(ElementwiseProblem):

    def __init__(self, **kwargs):
        super().__init__(n_var=CLASS_SIZE, n_obj=N_OBJ,
                         n_constr=N_CONSTR, xl=0, xu=TEACHER_SIZE-1, type_var=int,**kwargs)

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = [f1(x), f2(x), f3(x)*-1] #For minimization context, with multiply *-1 the max f3
        out["G"] = validateConstraints(x)

# the number of threads to be used
n_threads = 8

# initialize the pool
pool = ThreadPool(n_threads)

# define the problem by passing the starmap interface of the thread pool
problem = ADEEProblem(runner=pool.starmap, func_eval=starmap_parallelized_eval)

# Configure NSGA2 
algorithm = NSGA2(pop_size=100,sampling=pop_0,
               crossover=get_crossover("int_sbx", prob=1.0, eta=3.0),
               mutation=get_mutation("int_pm",  prob=1.0,eta=3.0)
               ,eliminate_duplicates=True)

#Optimize
res = minimize(problem,
               algorithm,
               ('n_gen', 10),
               seed=1,
               verbose=True)

print('Time:', res.exec_time)

print("Best solution found: %s" % res.X)
print("Function value: %s" % res.F)
print("Constraint violation: %s" % res.CV)

pool.close()

plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()