"""
Background for the QAP problem

**WORKFLOW**

1. Formulate the problem with flow and distance symmetric matrices
2. Create variables for each facility (binary variable)
3. Create the objective function using the binary variables (facilities)
4. Use penalties to enforce the constraint that only one facility can be at each location and each facility can be at only one location
5. Add all the constraints into a BQM (binary quantum model)
6. Plot a feasible solution
"""

import numpy as np
from dimod.generators import and_gate
from dwave.system import LeapHybridSampler

N = 3
max_flow = 100
min_flow = -100

f = np.random.uniform(min_flow, max_flow, size=(N, N))
d = np.random.rand(N,N)



bqm = and_gate('x1', 'x2', 'y1')
sampler = LeapHybridSampler()    
answer = sampler.sample(bqm)   
print(answer) 