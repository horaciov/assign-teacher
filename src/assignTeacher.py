import data
from objetivefunctions import f1, f2, f3
from constraint import validateConstraints
from multiprocessing.pool import ThreadPool
from pymoo.core.problem import ElementwiseProblem, starmap_parallelized_eval
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_crossover, get_mutation,get_sampling
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from pymoo.core.population import Population
from random import randrange
from geopy import distance
from multiprocessing import Process, Manager
import numpy as np
from pymoo.core.repair import Repair

#Initialize
data.init(maxDistance=40)

#Define the Teacher Assign Problem 
CLASS_SIZE = len(data.C)
TEACHER_SIZE = len(data.D)
N_OBJ = 3
N_CONSTR = 3

class ADEEProblem(ElementwiseProblem):

    def __init__(self, **kwargs):
        super().__init__(n_var=CLASS_SIZE, n_obj=N_OBJ,
                         n_constr=N_CONSTR, xl=0, xu=TEACHER_SIZE-1, type_var=int,**kwargs)

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = [f1(x), f2(x), f3(x)*-1] #For minimization context, with multiply *-1 the max f3
        out["G"] = validateConstraints(x)


def generate_ind(name,q): 
    print("Start generate ind "+str(name))
    ind=[-1]*CLASS_SIZE
    teachers=[]
    for i in range(TEACHER_SIZE):
        teachers.append(i)
    c=0
    while(c<CLASS_SIZE and len(teachers)>0):
        indx=randrange(len(teachers)) #Select a Teacher randomly
        i=teachers[indx]        
        teachers.remove(i)
        #print("Asignando docente: "+str(i)+" en hilo "+str(name)+". Disponibles: "+str(len(teachers)))
        dist_min=999999
        pos_min=-1
        for j in range(CLASS_SIZE):
            if ind[j]==-1:
                e=data.C[j][4]-1
                dist=distance.distance((data.E[e][1],data.E[e][2]),(data.D[i][1],data.D[i][2])).kilometers
                if dist<dist_min and dist<=data.Dmax:
                    dist_min=dist
                    pos_min=j
        if pos_min==-1:
            continue
        ind[pos_min]=i
        c=c+1
        print("Asignado por proceso "+str(name)+" "+str(c))
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
                            if e1==e2:
                                break
        if pos2_min!=-1:
            ind[pos2_min]=i
            c=c+1   
    print("Individuo agregado por proceso: "+str(name))
    q.put(ind)

class AEEEFeacible(Repair):

    def _do(self, problem, pop, **kwargs):

        print("Start repair")

        # the packing plan for the whole population (each row one individual)
        Z = pop.get("X")

        # now repair each indvidiual i
        for zi in range(len(Z)):
            # the packing plan for i
            z = Z[zi]
            valid=validateConstraints(z)
            
            if valid[0]==0 and valid[1]==0 and valid[2]==0:
                continue            
            
            teachersOne=[]
            teachersZero=[]
            c=CLASS_SIZE
            for i in range(len(data.D)):                
                assign1=-1                
                assign2=-1            
                for j in range(len(z)):
                    if i==z[j]:
                        if assign1==-1:                           
                            assign1=j
                        elif assign2==-1:
                            if data.C[assign1][1]==data.C[j][1]:
                                z[j]=-1
                                c=c-1
                                continue
                            d=distance.distance((data.E[data.C[assign1][4]-1][1],data.E[data.C[assign1][4]-1][2]),
                                    (data.E[data.C[j][4]-1][1],data.E[data.C[j][4]-1][2])).kilometers       
                            if(d>data.Dmax):#Maximun distances exceeded
                                z[j]=-1
                                c=c-1
                                continue
                            assign2=j
                        else:
                            c=c-1    
                            z[j]=-1
                if assign1>-1 and assign2==-1: #Teacher with one assign
                    teachersOne.append({"pos":assign1,"teacher":i})
                elif assign1==-1:#Teacher don't assigned
                    teachersZero.append(i)

            for dOne in range(len(teachersOne)):
                indx=randrange(len(teachersOne)) #Select a Teacher randomly
                i=teachersOne[indx]   
                teachersOne.remove(i)    
                #Search another class for the same teacher that match all constraints with dist min between estableshment
                dist2_min=999999
                pos2_min=-1
                for j in range(CLASS_SIZE): 
                    if z[j]==-1:
                        if data.C[j][1]!=data.C[i['pos']][1]:
                            e1=data.C[j][4]-1
                            e2=data.C[i['pos']][4]-1
                            dist=distance.distance((data.E[e1][1],data.E[e1][2]),(data.E[e2][1],data.E[e2][2])).kilometers
                            if dist<=data.Dmax:
                                if dist<dist2_min:
                                    dist2_min=dist    
                                    pos2_min=j
                    if pos2_min!=-1:
                        z[pos2_min]=i['teacher']
                        c=c+1 
                        break
                if c==CLASS_SIZE:
                    break
            
            while(c<CLASS_SIZE):
                indx=randrange(len(teachersZero)) #Select a Teacher randomly
                i=teachersZero[indx]   
                teachersZero.remove(i)                   
                dist_min=999999
                pos_min=-1
                for j in range(CLASS_SIZE):
                    if z[j]==-1:
                        e=data.C[j][4]-1
                        dist=distance.distance((data.E[e][1],data.E[e][2]),(data.D[i][1],data.D[i][2])).kilometers
                        if dist<dist_min:
                            dist_min=dist
                            pos_min=j
                z[pos_min]=i
                c=c+1
                if(c==CLASS_SIZE):
                    break

                #Search another class for the same teacher that match all constraints with dist min between estableshment
                dist2_min=999999
                pos2_min=-1
                for j in range(CLASS_SIZE): 
                    if z[j]==-1:
                        if data.C[j][1]!=data.C[pos_min][1]:
                            e1=data.C[j][4]-1
                            e2=data.C[pos_min][4]-1
                            dist=distance.distance((data.E[e1][1],data.E[e1][2]),(data.E[e2][1],data.E[e2][2])).kilometers
                            if dist<=data.Dmax:
                                if dist<dist2_min:
                                    dist2_min=dist    
                                    pos2_min=j
                if pos2_min!=-1:
                    z[pos2_min]=i
                    c=c+1   

        # set the design variables for the population
        pop.set("X", Z)
        print("End repair")
        return pop

if __name__ == '__main__':
    mananger = Manager()
    q = mananger.Queue()
    process=[]
    cp=12
    for index in range(cp):
        print("Main    : create and start process %d." % index)
        p = Process(target=generate_ind, args=(index,q))
        process.append(p) 
        p.start()     
          

    for p in process:
        p.join()

    print("Terminaron")

    pop_0=[]
    while not q.empty():
        pop_0.append(q.get())
    pop_0 = Population.new("X", pop_0)

    # the number of threads to be used
    n_threads = 8

    # initialize the pool
    pool = ThreadPool(n_threads)

    # define the problem by passing the starmap interface of the thread pool
    problem = ADEEProblem(runner=pool.starmap, func_eval=starmap_parallelized_eval)

    # Configure NSGA2 
    algorithm = NSGA2(pop_size=10,sampling=pop_0,
                crossover=get_crossover("int_k_point", n_points=4),
                mutation=get_mutation("int_pm"),
                repair=AEEEFeacible(),
                eliminate_duplicates=True)

    #Optimize
    res = minimize(problem,
                algorithm,
                ('n_gen', 40),
                seed=1,
                verbose=True)


    f = open("result.txt", "w")
    f.write("Time: %s" % res.exec_time)
    f.write("Best solution found:")
    f.write(str(res.X))
    f.write("Function value: %s" % res.F)
    f.write("Constraint violation: %s" % res.CV)
    f.close()

    print('Time:', res.exec_time)


    print("Best solution found:" % res.X)
    print("Function value: %s" % res.F)
    print("Constraint violation: %s" % res.CV)

    pool.close()

    plot = Scatter()
    plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
    plot.add(res.F, facecolor="none", edgecolor="red")
    plot.show()