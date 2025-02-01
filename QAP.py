"""
Background for the QAP problem

**WORKFLOW**

1. Formulate the non linear problem with flow and distance symmetric matrices
2. Create variables for each facility (binary variable)
3. Create the objective function using the binary variables (facilities)
4. Use penalties to enforce the constraint that only one facility can be at each location and each facility can be at only one location
5. Add all the constraints into a BQM (binary quantum model)
6. Plot a feasible solution
"""

# Create necessary imports
import numpy as np
# from dimod.generators import and_gate, combinations
from dwave.system import LeapHybridSampler
from dwave.optimization import Model
import helper

# Initialize state variables
N = 3
max_flow = 100
min_flow = -100
max_distance = 1


facilities = range(N)

# Generate the binary quantum model
model = Model()

flow = model.constant(helper.random_symmetric_matrix(N, min_flow, max_flow))
distance = model.constant(helper.random_symmetric_matrix(N, 0, max_distance))

permutation = model.list(N)
one = model.constant(1)
print('abc')
objective_function = (flow[permutation] * distance[:]).sum()

model.minimize(objective_function)

print(objective_function)
