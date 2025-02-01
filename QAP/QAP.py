"""
Background for the QAP problem

**WORKFLOW**

1. Formulate the non linear problem with flow and distance symmetric matrices
2. Create variables for each facility (binary variable)
3. Create the objective function using the binary variables (facilities)
4. Use penalties to enforce the constraint that only one facility can be at each location and each facility can be at only one location
5. Add all the constraints into a non linear (non linear model)
6. Plot a feasible solution
"""

# Create necessary imports
import numpy as np
# from dimod.generators import and_gate, combinations
from dwave.system import LeapHybridNLSampler
from dwave.optimization import Model
import QAP.helper as helper

# Initialize state variables
N = 3
max_flow = 100
min_flow = -100
max_distance = 1


facilities = range(N)

# Generate the non linear quantum model
model = Model()

flow = helper.random_symmetric_matrix(N, min_flow, max_flow)
distance = helper.random_symmetric_matrix(N, 0, max_distance)


model_flow = model.constant(flow)
model_distance = model.constant(distance)

permutation = model.list(N)
one = model.constant(1)

print(flow)
print(distance)

# Create the objective function

objective_function = (model_flow[permutation][:, permutation] * model_distance).sum()

# Minimize the model using the objective function

model.minimize(objective_function)

# Sample the model to see the output

sampler = LeapHybridNLSampler()
sampler.sample(model)

# Output the results
with model.lock():
    print(list(sym.state(0) for sym in model.iter_decisions()))
    print(model.objective.state(0))
