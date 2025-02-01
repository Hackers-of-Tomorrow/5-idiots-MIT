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
time_steps = 10

facilities = range(N_rooms + N_supply)

# Generate the non linear quantum model
model = Model()

flow = helper.random_time_matrix(time_steps, N_supply, N_rooms, max_flow)
room_supply_distance = helper.random_matrix(N_supply, N_rooms, max_distance)
room_room_distance = helper.random_symmetric_matrix(N_rooms, 0, max_distance)
supply_supply_distance = helper.random_symmetric_matrix(N_supply, 0, max_distance)

model_flow = model.constant(flow)
model_rs_distance = model.constant(room_supply_distance)
model_rr_distance = model.constant(room_room_distance)
model_ss_distance = model.constant(supply_supply_distance)

permutation_rooms = model.list(N_rooms)
permutation_supply = model.list(N_supply)

# Create the objective function
old_room_permutation = model.list(N_rooms)
old_supply_permutation = model.list(N_supply)

sampler = LeapHybridNLSampler()

# Output the results

for i in range(time_steps):

    cost = (model_flow[i][permutation_supply][:, permutation_rooms] * model_rs_distance).sum()
    room_penalty = (model_rr_distance[permutation_rooms][old_room_permutation]).sum()
    supply_penalty = (model_ss_distance[permutation_supply][old_supply_permutation]).sum()
    model.minimize(cost + room_penalty + supply_penalty)
    sampler.sample(model)
    with model.lock():
        print(list(sym.state(0) for sym in model.iter_decisions()))
        states = list(sym for sym in model.iter_decisions())
        old_supply_permutation = states[3]
        old_room_permutation = states[2]
        print(model.objective.state(0))


# Sample the model to see the output
