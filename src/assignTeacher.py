import data
from objetivefunctions import f1, f2, f3
from constraint import validateConstraints
from multiprocessing.pool import ThreadPool
from pymoo.core.problem import ElementwiseProblem, starmap_parallelized_eval
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.factory import get_crossover, get_mutation, get_sampling
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

#Initialize
data.init(maxDistance=30)

#Define the Teacher Assign Problem 
#With use a string of integers
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

# the number of threads to be used
n_threads = 8

# initialize the pool
pool = ThreadPool(n_threads)

# define the problem by passing the starmap interface of the thread pool
problem = ADEEProblem(runner=pool.starmap, func_eval=starmap_parallelized_eval)

# Configure NSGA2 
algorithm = NSGA2(pop_size=100,sampling=get_sampling("int_random"),
               crossover=get_crossover("int_sbx", prob=1.0, eta=3.0),
               mutation=get_mutation("int_pm", eta=3.0)
               ,eliminate_duplicates=True)

#Optimize
res = minimize(problem,
               algorithm,
               ('n_gen', 100),
               seed=1,
               verbose=False)

print('Time:', res.exec_time)

print("Best solution found: %s" % res.X)
print("Function value: %s" % res.F)
print("Constraint violation: %s" % res.CV)

pool.close()

plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()