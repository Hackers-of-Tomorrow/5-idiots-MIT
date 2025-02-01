"""
Background for the QAP problem

**CHANGES FROM QAP**

1. Introduce N simulations (we do N permutations) where N is the number of time steps
2. Between each simulation, add a penalty factor that penalize the closets if they move closets and departments
3. Two types of facilities, one that needs a supply and one that gives supplies
    - Two permutations, one that needs supplies and another that gets supplies, but they can't overlap locations
"""

# Create necessary imports
import numpy as np
# from dimod.generators import and_gate, combinations
from dwave.system import LeapHybridNLSampler
from dwave.optimization import Model
import helper

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
