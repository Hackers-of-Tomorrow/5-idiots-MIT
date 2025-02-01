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

flow = helper.random_symmetric_matrix(N, min_flow, max_flow)
distance = helper.random_symmetric_matrix(N, 0, max_distance)
facilities = range(N)

# Generate the binary quantum model
model = Model()
permutation = model.list(N)
one = model.constant(1)
model.add_constraint(permutation.sum() == one)


# Add all the variables to the model
for facility in facilities:
    bqm.add_variable()


bqm = and_gate('x1', 'x2', 'y1')
sampler = LeapHybridSampler()    
answer = sampler.sample(bqm)   
print(answer) 