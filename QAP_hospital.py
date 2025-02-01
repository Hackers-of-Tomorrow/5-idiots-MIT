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
N_rooms = 3
N_supply = 2
max_flow = 100
max_distance = 1


facilities = range(N_rooms + N_supply)

# Generate the non linear quantum model
model = Model()

flow = helper.random_matrix(N_rooms, N_supply, max_flow)
distance = helper.random_matrix(N_rooms + N_supply, N_rooms + N_supply, max_distance)

model_flow = model.constant(flow)
model_distance = model.constant(distance)

permutation_rooms = model.list(N_rooms)
permutation_supply = model.list(N_supply)

print(flow)
print(distance)

# Create the objective function

objective_function = (model_flow[permutation_rooms][:, permutation_supply] * model_distance).sum()

# Minimize the model using the objective function

model.minimize(objective_function)

# Sample the model to see the output

sampler = LeapHybridNLSampler()
sampler.sample(model)

# Output the results
with model.lock():
    print(list(sym.state(0) for sym in model.iter_decisions()))
    print(model.objective.state(0))
