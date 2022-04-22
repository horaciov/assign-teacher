from pymoo.algorithms.moo.nsga2 import NSGA2
from select import select
import numpy as np

from pymoo.factory import get_algorithm, get_crossover, get_mutation, get_sampling, get_reference_directions
from pymoo.optimize import minimize
from pymoo.core.problem import Problem, ElementwiseProblem
from constraint import validateConstraints2

from data import C, D
from objetivefunctions import f1, f2, f3

from pymoo.visualization.scatter import Scatter

from pymoo.core.problem import starmap_parallelized_eval
from multiprocessing.pool import ThreadPool



CLASS_SIZE = len(C)
TEACHER_SIZE = len(D)
N_OBJ = 3
N_CONSTR = 3


class MyProblem(ElementwiseProblem):

    def __init__(self, **kwargs):
        super().__init__(n_var=CLASS_SIZE, n_obj=N_OBJ,
                         n_constr=N_CONSTR, xl=0, xu=TEACHER_SIZE-1, type_var=int,**kwargs)

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = [f1(x), f2(x), f3(x)*-1]
        out["G"] = validateConstraints2(x)

# the number of threads to be used
n_threads = 8

# initialize the pool
pool = ThreadPool(n_threads)

# define the problem by passing the starmap interface of the thread pool
problem = MyProblem(runner=pool.starmap, func_eval=starmap_parallelized_eval)


algorithm = NSGA2(pop_size=50,sampling=get_sampling("int_random"),
               crossover=get_crossover("int_sbx", prob=1.0, eta=3.0),
               mutation=get_mutation("int_pm", eta=3.0)
               ,eliminate_duplicates=True)

res = minimize(problem,
               algorithm,
               ('n_gen', 40),
               seed=1,
               verbose=False)



print('Threads:', res.exec_time)

print("Best solution found: %s" % res.X)
print("Function value: %s" % res.F)
print("Constraint violation: %s" % res.CV)

pool.close()

plot = Scatter()
plot.add(problem.pareto_front(), plot_type="line", color="black", alpha=0.7)
plot.add(res.F, facecolor="none", edgecolor="red")
plot.show()