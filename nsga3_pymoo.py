from pymoo.algorithms.moo.nsga3 import NSGA3
from select import select
import numpy as np

from pymoo.factory import get_algorithm, get_crossover, get_mutation, get_sampling, get_reference_directions
from pymoo.optimize import minimize
from pymoo.core.problem import Problem, ElementwiseProblem
from constraint import validateConstraints2

from data import C, D
from objetivefunctions import f1, f2, f3

from pymoo.visualization.scatter import Scatter

CLASS_SIZE = len(C)
TEACHER_SIZE = len(D)
N_OBJ = 3
N_CONSTR = 3


class MyProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=CLASS_SIZE, n_obj=N_OBJ,
                         n_constr=N_CONSTR, xl=0, xu=TEACHER_SIZE-1, type_var=int)

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = [f1(x), f2(x), f3(x)*-1]
        out["G"] = validateConstraints2(x)


# create the reference directions to be used for the optimization
ref_dirs = get_reference_directions("das-dennis", 3, n_partitions=12)

method = NSGA3(pop_size=100,
               sampling=get_sampling("int_random"),
               crossover=get_crossover("int_sbx", prob=1.0, eta=3.0),
               mutation=get_mutation("int_pm", eta=3.0),
               eliminate_duplicates=True,
               ref_dirs=ref_dirs
               )


res = minimize(MyProblem(),
               method,
               termination=('n_gen', 40),
               seed=1,
               save_history=True
               )

print("Best solution found: %s" % res.X)
print("Function value: %s" % res.F)
print("Constraint violation: %s" % res.CV)

Scatter().add(res.F).show()
